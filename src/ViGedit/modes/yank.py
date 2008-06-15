import gtk
from binding_base import *
from ..actions import lines
class yank_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        self.register(self.yank_lines, gtk.keysyms.y)
        
    def handle_mode(self, event):
        message = "this mode doesn't need to be handled"
            
    def select_mode(self):
        base.set_element("select", False)
        base.set_element("mode", self.YANK_MODE)
        
    def yank_lines(self):
        lines.yank_line()
        self.bindings.select_mode("command")
        
