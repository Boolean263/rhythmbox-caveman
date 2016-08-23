# Unless I'm reading the docs wrong, there's no easy way to do
# common operations on playlists (such as finding one) without
# iterating over the entire list. So this class is here to
# abstract that part out of the real plugin code.

from gi.repository import GObject, RB, Peas, GLib

class RBPlaylists:
    def __init__(self, pl_man):
        self.manager = pl_man

    def get(self, name, kind=RB.StaticPlaylistSource):
        pl_list = self.manager.get_playlists()
        for p in pl_list:
            if isinstance(p, kind) and p.props.name == name:
                return p
        return None

    def getSelected(self):
        pl_list = self.manager.get_playlists()
        for p in pl_list:
            if p.props.selected:
                return p
        return None

    def remove(self, name, kind=RB.StaticPlaylistSource):
        # XXX How to ensure we're deleting the playlist of the right kind?
        try:
            self.manager.delete_playlist(name)
        except GLib.GError as ex:
            if str(ex)[0:44] != 'rb_playlist_manager_error: Unknown playlist:':
                raise ex

    def add(self, name, kind=RB.StaticPlaylistSource):
        if kind == RB.StaticPlaylistSource:
            self.manager.create_static_playlist(name)
        else:
            raise NotImplementedError()
        return self.get(name, kind)


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
