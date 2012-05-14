from contextlib import contextmanager
from gi.repository import Gedit, Gtk
from unittest import TestCase

class GeditHelper(object):
    def __init__(self, app):
        self.app = app
   
    @property
    def window(self):
        return self.app.get_active_window()
        
    @property
    def view(self):
        return self.window.get_active_view()
    
    @property
    def document(self):
        return self.window.get_active_document()
    
    @property
    def tabs(self):
        return self.window.get_views()
    
    @property
    def bounds(self):
        return self.document.get_bounds()
     
    @property
    def text(self):
        doc = self.document
        start, end = self.bounds
        return unicode(doc.get_text(start, end, True), 'utf-8')
    
    @text.setter
    def text(self, txt):
        self.document.set_text(txt)
        self.update()
    
    def add_tab(self, jump_to=True):
        self.window.create_tab(jump_to)
        self.update()
    
    def update(self):
        """Make gedit run the main iteration"""
        while Gtk.events_pending():
            Gtk.main_iteration()

class GeditTestCase(TestCase):
    def setUp(self):
        self.gedit = GeditHelper(Gedit.App.get_default())
        # Remove all current tabs and replace with new one
        self.gedit.window.close_all_tabs()
        self.gedit.add_tab()
