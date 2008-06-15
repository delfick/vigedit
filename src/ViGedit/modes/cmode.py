import gtk
from binding_base import *
from ..actions import text
class cmode_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        self.register(self.append_a, gtk.keysyms.a, False, False)
        self.register(self.handle_w, gtk.keysyms.w, False, False)
        
    def handle_mode(self, event):
        message = "nothing to see here"
        
    def select_mode(self):
        self.acc = []
        self.mode = self.CMODE
        
        
    def append_a(self):
        self.increment_accumulator('a')
        
    def handle_w(self):
        #what does this actually do?
        self.get_element("view").emit("move-cursor", gtk.MOVEMENT_WORDS, -1, self.get_element("select"))
        self.visual_mode()
        self.get_element("view").emit("move-cursor", gtk.MOVEMENT_WORDS, 1, self.get_element("select"))
        text.cut_selection()
        self.select_mode("insert")
