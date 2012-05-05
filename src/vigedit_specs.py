"""
    Hacky Gedit plugin that lets me have access to gi.repository when running vigedit tests
    It does this by registering <Ctrl><Alt>U to start tests.
    This command must be called when gedit has begun.
    
    I would do it via a signal, but I can't figure out how to make it work :(
    
    It is recommended this plugin is used via test.py
    After putting vigedit_specs.plugin and vigedit_specs.py into ~/.local/share/gedit/plugins
"""
from gi.repository import GObject, Gedit, Gtk
from textwrap import dedent
import shlex
import nose
import sys
import os

class ViGeditTestAppActivatable(GObject.Object, Gedit.AppActivatable):
    """
        App holds code to start tests.
        It makes sure tests are only run once
    """
    __gtype_name__ = "ViGeditTestAppActivatable"
    app = GObject.property(type=Gedit.App)
    
    def do_activate(self):
        """Make start function available on Gedit.App Singleton"""
        self.app.start = self.start
    
    def start(self):
        """Make sure this doesn't get re-executed when new windows are made"""
        if not hasattr(self, "_started"):
            self._started = True
            argv = shlex.split(os.environ.get('NOSE_ARGS', ""))
            exit_code = nose.run(argv=["%stests" % sys.argv[0]] + argv)
            sys.exit(exit_code)

class ViGeditTestWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    """
        Creates shortcut for each new window so that they all have the oppurtunity to start the tests
    """
    __gtype_name__ = "ViGeditTestWindowActivatable"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self.ui_str= dedent("""
            <ui>
                <menubar name="MenuBar">
                    <menu name="ToolsMenu" action="Tools">
                        <placeholder name="ToolOps_2">
                            <menuitem name="TestVigedit" action="TestVigedit"/>
                        </placeholder>
                    </menu>
                </menubar>
                </ui>
            """
        )

    def do_activate(self):
        """Create menu item/shortcut to start the tests"""
        # Create action
        test_action = Gtk.Action("TestVigedit", None, None, None)
        test_action.connect("activate", lambda event : Gedit.App.get_default().start())
        
        # Add action to an action group
        action_group = Gtk.ActionGroup("TestVigeditActions")
        action_group.add_action_with_accel(test_action, '<Ctrl><Alt>U')
        
        # Add to manager and keep references for deactivation
        manager = self.window.get_ui_manager()
        manager.insert_action_group(action_group)
        self.ui_id = manager.add_ui_from_string(self.ui_str)
        self.action_group = action_group
    
    def do_deactivate(self):
        """Cleanup menuitem/shortcut"""
        manager = self.window.get_ui_manager()
        manager.remove_ui(self.ui_id)
        manager.remove_action_group(self.action_group)
        manager.ensure_update()        
