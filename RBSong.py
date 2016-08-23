from gi.repository import GObject, RB, Peas, Gio
import datetime

prop = RB.RhythmDBPropType
datetime_type = type(datetime.datetime.now())

class RBSong:
    # You'd think there'd be some way of getting this from rhythmbox
    propTypes = {
        prop.ALBUM: str,
        prop.ALBUM_ARTIST: str,
        prop.ALBUM_ARTIST_FOLDED: str,
        prop.ALBUM_ARTIST_SORTNAME: str,
        prop.ALBUM_ARTIST_SORTNAME_FOLDED: str,
        prop.ALBUM_ARTIST_SORTNAME_SORT_KEY: str,
        prop.ALBUM_ARTIST_SORT_KEY: str,
        prop.ALBUM_FOLDED: str,
        prop.ALBUM_SORTNAME: str,
        prop.ALBUM_SORTNAME_FOLDED: str,
        prop.ALBUM_SORTNAME_SORT_KEY: str,
        prop.ALBUM_SORT_KEY: str,
        prop.ARTIST: str,
        prop.ARTIST_FOLDED: str,
        prop.ARTIST_SORTNAME_FOLDED: str,
        prop.ARTIST_SORTNAME_SORT_KEY: str,
        prop.ARTIST_SORT_KEY: str,
        prop.BEATS_PER_MINUTE: int,
        prop.BITRATE: int,
        prop.COMMENT: str,
        prop.COMPOSER: str,
        prop.COMPOSER_FOLDED: str,
        prop.COMPOSER_SORTNAME: str,
        prop.COMPOSER_SORTNAME_FOLDED: str,
        prop.COMPOSER_SORTNAME_SORT_KEY: str,
        prop.COMPOSER_SORT_KEY: str,
        prop.COPYRIGHT: str,
        prop.DATE: datetime_type,
        prop.DESCRIPTION: str,
        prop.DISC_NUMBER: int,
        prop.DISC_TOTAL: int,
        prop.DURATION: int,
        #prop.ENTRY_ID
        prop.FILE_SIZE: int,
        prop.FIRST_SEEN: datetime_type,
        prop.FIRST_SEEN_STR: str,
        prop.GENRE: str,
        prop.GENRE_FOLDED: str,
        prop.GENRE_SORT_KEY: str,
        #prop.HIDDEN
        #prop.IMAGE
        prop.KEYWORD: str,
        prop.LANG: str,
        prop.LAST_PLAYED: datetime_type,
        prop.LAST_PLAYED_STR: str,
        prop.LAST_SEEN: datetime_type,
        prop.LAST_SEEN_STR: str,
        prop.LOCATION: str,
        #prop.MB_ALBUMARTISTID
        #prop.MB_ALBUMID
        #prop.MB_ARTISTID
        #prop.MB_ARTISTSORTNAME
        #prop.MB_TRACKID
        prop.MEDIA_TYPE: str,
        prop.MOUNTPOINT: str,
        prop.MTIME: datetime_type,
        #prop.PLAYBACK_ERROR
        prop.PLAY_COUNT: int,
        prop.POST_TIME: datetime_type,
        prop.RATING: int,
        prop.REPLAYGAIN_ALBUM_GAIN: float,
        prop.REPLAYGAIN_ALBUM_PEAK: float,
        prop.REPLAYGAIN_TRACK_GAIN: float,
        prop.REPLAYGAIN_TRACK_PEAK: float,
        prop.SEARCH_MATCH: str,
        #prop.STATUS
        prop.SUBTITLE: str,
        prop.SUMMARY: str,
        prop.TITLE: str,
        prop.TITLE_FOLDED: str,
        prop.TITLE_SORT_KEY: str,
        prop.TRACK_NUMBER: str,
        prop.TRACK_TOTAL: str,
        prop.TYPE: str,
        prop.YEAR: int,
    }

    def __init__(self, db, uri):
        self.db = db
        self.entry = db.entry_lookup_by_location(uri)
        if self.entry:
            self.isNew = False
        else:
            if uri[0:7] == 'file://':
                entry_type = db.entry_type_get_by_name('song')
            else:
                entry_type = db.entry_type_get_by_name('iradio')
            self.entry = RB.RhythmDBEntry.new(db, entry_type, uri)
            self.isNew = True

    def __getitem__(self, prop_id):
        prop_type = self.propTypes[prop_id]
        if prop_type == bool:
            return self.entry.get_boolean(prop_id)
        if prop_type == str:
            return self.entry.get_string(prop_id)
        elif prop_type == int:
            return self.entry.get_ulong(prop_id)
        elif prop_type == float:
            return self.entry.get_double(prop_id)
        elif prop_type == datetime_type:
            n = self.entry.get_ulong(prop_id)
            return datetime.datetime.fromtimestamp(n, tz=datetime.timezone.utc)

    def __setitem__(self, prop_id, val):
        if val is None: return
        if type(val) == datetime_type:
            val = int(val.timestamp())
        if prop_id == prop.RATING and val > 5:
            # iTunes rates from 0-100, RB from 0-5
            val = int(val / 20)
        self.db.entry_set(self.entry, prop_id, val)
        return val

    def commit(self):
        self.db.commit()
        self.isNew = False

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
