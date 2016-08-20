#!/usr/bin/env python3

from gi.repository import GObject, RB, Peas, Gio

import configparser
import os
import xml.etree.ElementTree as ET
import datetime

# These ones are from this directory
import iDict
import RhythmUIHelper
import RBSong

# I'll add a config UI later
#from config import CavemanConfig

prop = RB.RhythmDBPropType

class Caveman (RhythmUIHelper.RhythmUIHelper):

    import_queue = []
    export_queue = []
    rb2it = {
        prop.ALBUM: 'Album',
        prop.ALBUM_ARTIST: 'Album Artist',
        #prop.ALBUM_ARTIST_FOLDED
        #prop.ALBUM_ARTIST_SORTNAME
        #prop.ALBUM_ARTIST_SORTNAME_FOLDED
        #prop.ALBUM_ARTIST_SORTNAME_SORT_KEY
        #prop.ALBUM_ARTIST_SORT_KEY
        #prop.ALBUM_FOLDED
        #prop.ALBUM_SORTNAME
        #prop.ALBUM_SORTNAME_FOLDED
        #prop.ALBUM_SORTNAME_SORT_KEY
        #prop.ALBUM_SORT_KEY
        prop.ARTIST: 'Artist',
        #prop.ARTIST_FOLDED
        #prop.ARTIST_SORTNAME_FOLDED
        #prop.ARTIST_SORTNAME_SORT_KEY
        #prop.ARTIST_SORT_KEY
        prop.BEATS_PER_MINUTE: 'BPM',
        prop.BITRATE: 'Bit Rate',
        prop.COMMENT: 'Comments',
        prop.COMPOSER: 'Composer',
        #prop.COMPOSER_FOLDED
        #prop.COMPOSER_SORTNAME
        #prop.COMPOSER_SORTNAME_FOLDED
        #prop.COMPOSER_SORTNAME_SORT_KEY
        #prop.COMPOSER_SORT_KEY
        #prop.COPYRIGHT
        #prop.DATE: 'Date Added',
        #prop.DESCRIPTION: 'Comments',
        prop.DISC_NUMBER: 'Disc Number',
        #prop.DISC_TOTAL
        prop.DURATION: 'Total Time',
        #prop.ENTRY_ID # Can't be set
        prop.FILE_SIZE: 'Size',
        prop.FIRST_SEEN: 'Date Added',
        #prop.FIRST_SEEN_STR
        prop.GENRE: 'Genre',
        #prop.GENRE_FOLDED
        #prop.GENRE_SORT_KEY
        #prop.HIDDEN
        #prop.IMAGE
        #prop.KEYWORD
        #prop.LANG
        prop.LAST_PLAYED: 'Play Date UTC',
        #prop.LAST_PLAYED_STR
        #prop.LAST_SEEN
        #prop.LAST_SEEN_STR
        #prop.LOCATION # Special
        #prop.MB_ALBUMARTISTID
        #prop.MB_ALBUMID
        #prop.MB_ARTISTID
        #prop.MB_ARTISTSORTNAME
        #prop.MB_TRACKID
        #prop.MEDIA_TYPE: 'Kind',
        #prop.MOUNTPOINT
        #prop.MTIME: 'Date Modified',
        #prop.PLAYBACK_ERROR
        prop.PLAY_COUNT: 'Play Count',
        #prop.POST_TIME
        prop.RATING: 'Rating',
        #prop.REPLAYGAIN_ALBUM_GAIN
        #prop.REPLAYGAIN_ALBUM_PEAK
        #prop.REPLAYGAIN_TRACK_GAIN
        #prop.REPLAYGAIN_TRACK_PEAK
        #prop.SEARCH_MATCH
        #prop.STATUS # Can't be set
        #prop.SUBTITLE
        #prop.SUMMARY # Can't be set
        prop.TITLE: 'Name',
        #prop.TITLE_FOLDED
        #prop.TITLE_SORT_KEY
        prop.TRACK_NUMBER: 'Track Number',
        #prop.TRACK_TOTAL
        #prop.TYPE: 'Track Type',
        prop.YEAR: 'Year',
    }

    def __init__(self):
        """
        Constructor
        """
        super(Caveman, self).__init__()
        self.foreign_prefix = None
        self.our_prefix = None

    def do_activate(self):
        """
        Called by rhythmbox when the plugin is activated
        """
        super(Caveman, self).do_activate()
        app = self.object.props.application

        self.config = configparser.RawConfigParser()
        self.config_file = os.path.join(os.environ['HOME'], '.local/share/rhythmbox/cavemanrc')
        if os.path.isfile(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config.read(os.path.join(os.environ['HOME'], '.local/share/rhythmbox/caveman/defaults.cavemanrc'))

        if self.config.get('DEFAULT', 'music_root_dir') == "XDG_MUSIC_DIR":
            self.config.set('DEFAULT', 'music_root_dir', self.get_xdg_music_dir())
        self.our_prefix = 'file://'+self.config.get('DEFAULT', 'music_root_dir')
        if self.our_prefix[-1] != '/':
            self.our_prefix = self.our_prefix+"/"

        self.add_action('import-from-itunes', self.import_from_itunes,
            parentMenu='tools', menuName='Import from iTunes')
        self.add_action('export-to-itunes', self.export_to_itunes,
            parentMenu='tools', menuName='Export to iTunes')

        if self.config.getboolean('DEFAULT', 'auto_import'):
            self.import_from_itunes();

    def do_deactivate(self):
        """
        Called by rhythmbox when the plugin is deactivated
        """
        super(Caveman, self).do_deactivate()
        app = self.object.props.application

        if self.config.getboolean('DEFAULT', 'auto_export'):
            self.export_to_itunes();

        self.foreign_prefix = None
        self.our_prefix = None

    def get_xdg_music_dir(self):
        """
        Get the user's music directory
        """
        try:
            config_file = os.path.expanduser("~/.config/user-dirs.dirs")
            f = open(config_file, 'r')

            for line in f:
                if line.strip().startswith("XDG_MUSIC_DIR"):
                    # get part after = , remove " and \n
                    dir = line.split("=")[1].replace("\"", "").replace("\n", "")
                    # replace $HOME with ~ (os.path.expanduser compability)
                    dir = dir.replace("$HOME", os.path.expanduser("~"))
        except:
            # default dir if we dont find music dir
            dir = os.path.expanduser("~")
        return dir

    def import_callback(self, data=None):
        if len(self.import_queue) == 0: return False
        next_song = self.import_queue.pop(0)
        self.import_update_song(next_song)
        return len(self.import_queue) > 0

    def import_from_itunes(self, action=None, parameter=None, shell=None):
        xml_file = self.config.get('DEFAULT', 'itunes_xml_file')
        if not os.path.isfile(xml_file): return

        print("Loading iTunes library")
        root_dict = iDict.iDict(ET.parse(xml_file).getroot()[0])
        print("Queueing import")
        self.foreign_prefix = root_dict['Music Folder']

        self.import_queue = list(root_dict['Tracks'].values())

        print("Triggering import of {} tracks".format(len(self.import_queue)))
        self.add_idle_callback(self.import_callback)

    def export_to_itunes(self, action=None, parameter=None, shell=None):
        pass

    def import_update_song(self, new_song):
        db = self.object.props.db

        try:
            song_uri = new_song["Location"]
        except KeyError:
            # Song type without a location, typically a cloud-stored song
            return

        prefix_len = len(self.foreign_prefix)
        if song_uri[0:prefix_len] == self.foreign_prefix:
            song_uri = self.our_prefix+song_uri[prefix_len:]
        elif song_uri[0:7] == 'file://':
            # Song with a file:// prefix we don't recognize
            return
        else:
            # Song without a file:// prefix, maybe a radio station or sth.
            pass

        song = RBSong.RBSong.findByURI(db, song_uri)
        if song:
            # Song exists, see if we need to update it
            print("Updating: "+song[prop.TITLE])
            if song[prop.LAST_PLAYED] < new_song['Play Date UTC']:
                song[prop.RATING] = int(new_song['Rating'] / 20)
                song[prop.PLAY_COUNT] = new_song['Play Count']
                song[prop.LAST_PLAYED] = new_song['Play Date UTC']
                #song[prop.DESCRIPTION] = "(Caveman:TID={},PID={})".format(new_song['Track ID'], new_song['Persistent ID']);
                song.commit()

        else:
            # Song doesn't exist, we need to add it
            print("Adding: "+new_song['Name'])
            song = RBSong.RBSong.add(db, song_uri)
            #song[prop.DESCRIPTION] = "(Caveman:TID={},PID={})".format(new_song['Track ID'], new_song['Persistent ID']);
            for k, v in self.rb2it.items():
                try:
                    if v == 'Total Time':
                        song[k] = int(new_song[v] / 1000)
                    elif v == 'Rating':
                        song[k] = int(new_song[v] / 20)
                    elif v == 'BPM':
                        song[k] = int(new_song[v] / 100)
                    else:
                        song[k] = new_song[v]
                except KeyError:
                    #print("Warning: KeyError:"+v)
                    pass
            song.commit()


#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf8
# mode: python
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf8 filetype=python:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf8:mode=python:
#
