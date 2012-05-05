'''
    The Gedit plugin itself.
'''
from gi.repository import GObject, Gedit
from vig import VigApp
import sys
import os

########################
###   DEFINE ACTIONS
########################

class AppMethods(object):
    def do_activate(self):
        """App was created"""
        self.app.vig = VigApp()
        print 'create', self.app

class WindowMethods(object):
    @property
    def app(self):
        return Gedit.App.get_default()
    
    def do_activate(self):
        """Window was created"""
        print os.path.abspath(os.curdir)
        print self.app.vig
        print '\tcreate', self.window
    
    def do_deactivate(self):
        """Window was closed"""
        print '\tdestroy', self.window
    
    def do_update_state(self):
        """Window was updated"""
        print '\tupdate', self.window

class ViewMethods(object):
    @property
    def app(self):
        return Gedit.App.get_default()
    
    def do_activate(self):
        """View was created"""
        print '\t\tcreate', self.view
    
    def do_deactivate(self):
        """View was destroyed"""
        print '\t\tdestroy', self.view
    
    def do_update_state(self):
        """View was updated"""
        print '\t\tupdate', self.view

########################
###   CREATE ACTIVATABLES
########################

def create_activatables(*specs):
    """
        Convenience for creating activatables
        Each spec is a (kls, extending) tuple:
            * kls: ordinary class that impliments desired methods for activatable
            * extending: Either "App", "Window" or "View"
    """    
    def init(self):
        """
            __init__ given to the created activatables
            Unless overidden by kls.__init__
        """
        GObject.Object.__init__(self)
    
    # Dictionary of {name : activable}
    # Where name is "ViGedit<extending>Activatable"
    created = {}
    
    for kls, extending in specs:
        activatable = "%sActivatable" % extending
        name = "ViGedit%s" % activatable
        
        attrs = {
              '__init__' : init
            , '__gtype_name__' : name
            , extending.lower() : GObject.property(type=getattr(Gedit, extending))
            }
        
        # It would seem it doesn't work if I give kls as another class to inherit from...
        attrs.update(kls.__dict__)
        
        created[name] = type(name, (GObject.Object, getattr(Gedit, activatable)), attrs)
    
    return created

# Create and add activatables to this file
# So that they may be imported
if 'nose' not in sys.modules:
    activatables = create_activatables(
          (AppMethods, "App")
        , (ViewMethods, "View")
        , (WindowMethods, "Window")
        )

    locals().update(**activatables)
