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

class Caveman (RhythmUIHelper.RhythmUIHelper):

    rb2it = {
        RB.RhythmDBPropType.ALBUM: 'Album',
        #RB.RhythmDBPropType.ALBUM_ARTIST
        #RB.RhythmDBPropType.ALBUM_ARTIST_FOLDED
        #RB.RhythmDBPropType.ALBUM_ARTIST_SORTNAME
        #RB.RhythmDBPropType.ALBUM_ARTIST_SORTNAME_FOLDED
        #RB.RhythmDBPropType.ALBUM_ARTIST_SORTNAME_SORT_KEY
        #RB.RhythmDBPropType.ALBUM_ARTIST_SORT_KEY
        #RB.RhythmDBPropType.ALBUM_FOLDED
        #RB.RhythmDBPropType.ALBUM_SORTNAME
        #RB.RhythmDBPropType.ALBUM_SORTNAME_FOLDED
        #RB.RhythmDBPropType.ALBUM_SORTNAME_SORT_KEY
        #RB.RhythmDBPropType.ALBUM_SORT_KEY
        RB.RhythmDBPropType.ARTIST: 'Artist',
        #RB.RhythmDBPropType.ARTIST_FOLDED
        #RB.RhythmDBPropType.ARTIST_SORTNAME_FOLDED
        #RB.RhythmDBPropType.ARTIST_SORTNAME_SORT_KEY
        #RB.RhythmDBPropType.ARTIST_SORT_KEY
        #RB.RhythmDBPropType.BEATS_PER_MINUTE
        RB.RhythmDBPropType.BITRATE: 'Bit Rate',
        #RB.RhythmDBPropType.COMMENT: 'Comments',
        RB.RhythmDBPropType.COMPOSER: 'Composer',
        #RB.RhythmDBPropType.COMPOSER_FOLDED
        #RB.RhythmDBPropType.COMPOSER_SORTNAME
        #RB.RhythmDBPropType.COMPOSER_SORTNAME_FOLDED
        #RB.RhythmDBPropType.COMPOSER_SORTNAME_SORT_KEY
        #RB.RhythmDBPropType.COMPOSER_SORT_KEY
        #RB.RhythmDBPropType.COPYRIGHT
        RB.RhythmDBPropType.DATE: 'Date Added',
        RB.RhythmDBPropType.DESCRIPTION: 'Comments',
        #RB.RhythmDBPropType.DISC_NUMBER
        #RB.RhythmDBPropType.DISC_TOTAL
        #RB.RhythmDBPropType.DURATION
        #RB.RhythmDBPropType.ENTRY_ID
        RB.RhythmDBPropType.FILE_SIZE: 'Size',
        #RB.RhythmDBPropType.FIRST_SEEN
        #RB.RhythmDBPropType.FIRST_SEEN_STR
        RB.RhythmDBPropType.GENRE: 'Genre',
        #RB.RhythmDBPropType.GENRE_FOLDED
        #RB.RhythmDBPropType.GENRE_SORT_KEY
        #RB.RhythmDBPropType.HIDDEN
        #RB.RhythmDBPropType.IMAGE
        #RB.RhythmDBPropType.KEYWORD
        #RB.RhythmDBPropType.LANG
        RB.RhythmDBPropType.LAST_PLAYED: 'Play Date',
        #RB.RhythmDBPropType.LAST_PLAYED_STR
        #RB.RhythmDBPropType.LAST_SEEN
        #RB.RhythmDBPropType.LAST_SEEN_STR
        #RB.RhythmDBPropType.LOCATION
        #RB.RhythmDBPropType.MB_ALBUMARTISTID
        #RB.RhythmDBPropType.MB_ALBUMID
        #RB.RhythmDBPropType.MB_ARTISTID
        #RB.RhythmDBPropType.MB_ARTISTSORTNAME
        #RB.RhythmDBPropType.MB_TRACKID
        RB.RhythmDBPropType.MEDIA_TYPE: 'Kind',
        #RB.RhythmDBPropType.MOUNTPOINT
        RB.RhythmDBPropType.MTIME: 'Date Modified',
        #RB.RhythmDBPropType.PLAYBACK_ERROR
        RB.RhythmDBPropType.PLAY_COUNT: 'Play Count',
        #RB.RhythmDBPropType.POST_TIME
        #RB.RhythmDBPropType.RATING: 'Rating',
        #RB.RhythmDBPropType.REPLAYGAIN_ALBUM_GAIN
        #RB.RhythmDBPropType.REPLAYGAIN_ALBUM_PEAK
        #RB.RhythmDBPropType.REPLAYGAIN_TRACK_GAIN
        #RB.RhythmDBPropType.REPLAYGAIN_TRACK_PEAK
        #RB.RhythmDBPropType.SEARCH_MATCH
        #RB.RhythmDBPropType.STATUS
        #RB.RhythmDBPropType.SUBTITLE
        #RB.RhythmDBPropType.SUMMARY
        RB.RhythmDBPropType.TITLE: 'Name',
        #RB.RhythmDBPropType.TITLE_FOLDED
        #RB.RhythmDBPropType.TITLE_SORT_KEY
        RB.RhythmDBPropType.TRACK_NUMBER: 'Track Number',
        #RB.RhythmDBPropType.TRACK_TOTAL
        RB.RhythmDBPropType.TYPE: 'Track Type',
        RB.RhythmDBPropType.YEAR: 'Year',
    }
    it2rb = {v: k for k, v in rb2it.items()}

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

    def import_from_itunes(self, action=None, parameter=None, shell=None):
        xml_file = self.config.get('DEFAULT', 'itunes_xml_file')
        if not os.path.isfile(xml_file): return

        print("Commencing import")

        root_dict = iDict.iDict(ET.parse(xml_file).getroot()[0])
        self.foreign_prefix = root_dict['Music Folder']

        for k, v in root_dict['Tracks'].items():
            self.import_update_song(v)

        print("Completing import")



    def export_to_itunes(self, action=None, parameter=None, shell=None):
        pass

    def import_update_song(self, new_song):
        db = self.object.props.db
        prop = RB.RhythmDBPropType

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
            if song[prop.LAST_PLAYED] < new_song['Play Date UTC']:
                song[prop.LAST_SEEN] = datetime.datetime.now()
                song[prop.RATING] = new_song['Rating']
                song[prop.PLAY_COUNT] = new_song['Play Count']
                song[prop.LAST_PLAYED] = new_song['Play Date UTC']
                song.commit()

        else:
            # Song doesn't exist, we need to add it
            #print("Didn't find song for "+song_uri)
            pass

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
