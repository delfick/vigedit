from contextlib import contextmanager
from gi.repository import Gedit
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
    def bounds(self):
        return self.document.get_bounds()
    
    @contextmanager
    def grouped_action(self):
        doc = self.document
        doc.begin_user_action()
        try:
            yield doc
        finally:
            doc.end_user_action()
     
    @property
    def text(self):
        doc = self.document
        start, end = self.bounds
        return unicode(doc.get_text(start, end, True), 'utf-8')
    
    @text.setter
    def text(self, txt):
        self.document.set_text(txt)

class GeditTestCase(TestCase):
    def setUp(self):
        self.gedit = GeditHelper(Gedit.App.get_default())
