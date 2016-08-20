
from gi.repository import GObject, RB, Peas, Gio

class RhythmUIHelper (GObject.Object, Peas.Activatable):
    """
    Separate out some of the rhythmbox boilerplate stuff
    from the code that actually does what I want the plugin to do.
    """

    # Every plugin gets this reference to the RhythmBox shell
    object = GObject.property(type=GObject.Object)

    # Queue of actions we should take when our plugin is deactivated
    todo_when_deactivated = []

    def __init__(self):
        """
        Constructor
        """
        super(RhythmUIHelper, self).__init__()

    def do_activate(self):
        """
        Called by rhythmbox when the plugin is activated.
        """
        pass

    def do_deactivate(self):
        """
        Called by rhythmbox when the plugin is deactivated.
        """

        # Perform all the actions we queued up
        while len(self.todo_when_deactivated):
            entry = self.todo_when_deactivated.pop(0)
            func = entry.pop(0)
            func(*entry)

    def when_deactivated(self, *args):
        self.todo_when_deactivated.append(list(args))

    def add_action(self, name, func, parentMenu=None, menuName=None):
        """
        Add an action with an optional menu trigger.
        To be called from self.do_activate().
        """
        app = self.object.props.application

        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', func, self.object)
        app.add_action(action)
        self.when_deactivated(app.remove_action, name)

        if parentMenu and menuName:
            app.add_plugin_menu_item(parentMenu, name,
                Gio.MenuItem.new(label=menuName, detailed_action="app."+name))
            self.when_deactivated(app.remove_plugin_menu_item, parentMenu, name)

        return action

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
