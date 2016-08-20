from gi.repository import GObject, RB, Peas, Gio
import datetime

prop = RB.RhythmDBPropType
datetime_type = type(datetime.datetime.now())

class RBSong:
    propNames = {
        prop.ALBUM: 'ALBUM',
        prop.ALBUM_ARTIST: 'ALBUM_ARTIST',
        prop.ALBUM_ARTIST_FOLDED: 'ALBUM_ARTIST_FOLDED',
        prop.ALBUM_ARTIST_SORTNAME: 'ALBUM_ARTIST_SORTNAME',
        prop.ALBUM_ARTIST_SORTNAME_FOLDED: 'ALBUM_ARTIST_SORTNAME_FOLDED',
        prop.ALBUM_ARTIST_SORTNAME_SORT_KEY: 'ALBUM_ARTIST_SORTNAME_SORT_KEY',
        prop.ALBUM_ARTIST_SORT_KEY: 'ALBUM_ARTIST_SORT_KEY',
        prop.ALBUM_FOLDED: 'ALBUM_FOLDED',
        prop.ALBUM_SORTNAME: 'ALBUM_SORTNAME',
        prop.ALBUM_SORTNAME_FOLDED: 'ALBUM_SORTNAME_FOLDED',
        prop.ALBUM_SORTNAME_SORT_KEY: 'ALBUM_SORTNAME_SORT_KEY',
        prop.ALBUM_SORT_KEY: 'ALBUM_SORT_KEY',
        prop.ARTIST: 'ARTIST',
        prop.ARTIST_FOLDED: 'ARTIST_FOLDED',
        prop.ARTIST_SORTNAME_FOLDED: 'ARTIST_SORTNAME_FOLDED',
        prop.ARTIST_SORTNAME_SORT_KEY: 'ARTIST_SORTNAME_SORT_KEY',
        prop.ARTIST_SORT_KEY: 'ARTIST_SORT_KEY',
        prop.BEATS_PER_MINUTE: 'BEATS_PER_MINUTE',
        prop.BITRATE: 'BITRATE',
        prop.COMMENT: 'COMMENT',
        prop.COMPOSER: 'COMPOSER',
        prop.COMPOSER_FOLDED: 'COMPOSER_FOLDED',
        prop.COMPOSER_SORTNAME: 'COMPOSER_SORTNAME',
        prop.COMPOSER_SORTNAME_FOLDED: 'COMPOSER_SORTNAME_FOLDED',
        prop.COMPOSER_SORTNAME_SORT_KEY: 'COMPOSER_SORTNAME_SORT_KEY',
        prop.COMPOSER_SORT_KEY: 'COMPOSER_SORT_KEY',
        prop.COPYRIGHT: 'COPYRIGHT',
        prop.DATE: 'DATE',
        prop.DESCRIPTION: 'DESCRIPTION',
        prop.DISC_NUMBER: 'DISC_NUMBER',
        prop.DISC_TOTAL: 'DISC_TOTAL',
        prop.DURATION: 'DURATION',
        prop.ENTRY_ID: 'ENTRY_ID',
        prop.FILE_SIZE: 'FILE_SIZE',
        prop.FIRST_SEEN: 'FIRST_SEEN',
        prop.FIRST_SEEN_STR: 'FIRST_SEEN_STR',
        prop.GENRE: 'GENRE',
        prop.GENRE_FOLDED: 'GENRE_FOLDED',
        prop.GENRE_SORT_KEY: 'GENRE_SORT_KEY',
        prop.HIDDEN: 'HIDDEN',
        prop.IMAGE: 'IMAGE',
        prop.KEYWORD: 'KEYWORD',
        prop.LANG: 'LANG',
        prop.LAST_PLAYED: 'LAST_PLAYED',
        prop.LAST_PLAYED_STR: 'LAST_PLAYED_STR',
        prop.LAST_SEEN: 'LAST_SEEN',
        prop.LAST_SEEN_STR: 'LAST_SEEN_STR',
        prop.LOCATION: 'LOCATION',
        prop.MB_ALBUMARTISTID: 'MB_ALBUMARTISTID',
        prop.MB_ALBUMID: 'MB_ALBUMID',
        prop.MB_ARTISTID: 'MB_ARTISTID',
        prop.MB_ARTISTSORTNAME: 'MB_ARTISTSORTNAME',
        prop.MB_TRACKID: 'MB_TRACKID',
        prop.MEDIA_TYPE: 'MEDIA_TYPE',
        prop.MOUNTPOINT: 'MOUNTPOINT',
        prop.MTIME: 'MTIME',
        prop.PLAYBACK_ERROR: 'PLAYBACK_ERROR',
        prop.PLAY_COUNT: 'PLAY_COUNT',
        prop.POST_TIME: 'POST_TIME',
        prop.RATING: 'RATING',
        prop.REPLAYGAIN_ALBUM_GAIN: 'REPLAYGAIN_ALBUM_GAIN',
        prop.REPLAYGAIN_ALBUM_PEAK: 'REPLAYGAIN_ALBUM_PEAK',
        prop.REPLAYGAIN_TRACK_GAIN: 'REPLAYGAIN_TRACK_GAIN',
        prop.REPLAYGAIN_TRACK_PEAK: 'REPLAYGAIN_TRACK_PEAK',
        prop.SEARCH_MATCH: 'SEARCH_MATCH',
        prop.STATUS: 'STATUS',
        prop.SUBTITLE: 'SUBTITLE',
        prop.SUMMARY: 'SUMMARY',
        prop.TITLE: 'TITLE',
        prop.TITLE_FOLDED: 'TITLE_FOLDED',
        prop.TITLE_SORT_KEY: 'TITLE_SORT_KEY',
        prop.TRACK_NUMBER: 'TRACK_NUMBER',
        prop.TRACK_TOTAL: 'TRACK_TOTAL',
        prop.TYPE: 'TYPE',
        prop.YEAR: 'YEAR',
    }
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

    def __init__(self, db, db_entry):
        self.db = db
        self.entry = db_entry

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

    @staticmethod
    def findByURI(db, uri):
        entry = db.entry_lookup_by_location(uri)
        if not entry: return entry
        return RBSong(db, entry)

    @staticmethod
    def add(db, uri):
        entry_type = None
        if uri[0:7] == 'file://':
            entry_type = db.entry_type_get_by_name('song')
        else:
            entry_type = db.entry_type_get_by_name('iradio')
        entry = RB.RhythmDBEntry.new(db, entry_type, uri)
        return RBSong(db, entry)




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
