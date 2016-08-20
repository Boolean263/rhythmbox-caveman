from gi.repository import Gtk, Gio, GObject, PeasGtk
from gi.repository import RB

class CavemanConfig(GObject.Object, PeasGtk.Configurable):
    object = GObject.property(type=GObject.Object)

    def do_create_configure_widget(self):
        self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.caveman")

        ui_file = rb.find_plugin_file(self, "caveman-prefs.ui")
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ui_file)

        content = self.builder.get_object("caveman-prefs")

        label = self.builder.get_object("headerlabel")
        label.set_markup("<b>%s</b>" % label.get_text())
        label.set_use_markup(True)

        autoimport = self.builder.get_object("autoimport")
        self.settings.bind("autoimport", autoimport, "active", Gio.SettingsBindFlags.DEFAULT)
        autoexport = self.builder.get_object("autoexport")
        self.settings.bind("autoexport", autoexport, "active", Gio.SettingsBindFlags.DEFAULT)

        return content


GObject.type_register(CavemanConfig)

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
