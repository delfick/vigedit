"""
    Hacky Gedit plugin that lets me have access to gi.repository when running vigedit tests
    
    It is recommended this plugin is used via test.sh
    After putting vigedit_specs.plugin and vigedit_specs.py into ~/.local/share/gedit/plugins
"""
from gi.repository import GObject, Gedit
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
    __gsignals__= {
          'run_tests' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
        }
    
    app = GObject.property(type=Gedit.App)
    
    def do_activate(self):
        """Make start function available on Gedit.App Singleton"""
        self.connect("run_tests", self.run_tests.im_func)
        GObject.idle_add(self.emit, "run_tests")
    
    def run_tests(self):
        """Run the tests"""
        argv = shlex.split(os.environ.get('NOSE_ARGS', ""))
        exit_code = nose.run(argv=["%stests" % sys.argv[0]] + argv)
        sys.exit(exit_code)
