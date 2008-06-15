import gtk
from binding_base import *
from ..actions import others, text, lines
class command_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):  
        self.register(self.bindings.cmode_mode, gtk.keysyms.c)
        self.register(self.bindings.delete_mode, gtk.keysyms.d, False, False)
        self.register(others.redo, gtk.keysyms.r, True, True, True)
        self.register(others.undo, gtk.keysyms.u, True, True)
        self.register(text.delete_char, gtk.keysyms.Delete, True, True)
        self.register(self.bindings.rmode_mode, gtk.keysyms.r)
       # self.register(text.delete_char, gtk.keysyms.x)
        self.register(lines.select_line, gtk.keysyms.V)
        self.register(text.cut_until_end_of_line, gtk.keysyms.D)
        self.register(text.paste_clipboard_above, gtk.keysyms.P)
        self.register(text.paste_clipboard_below, gtk.keysyms.p)
        self.register(self.bindings.yank_mode, gtk.keysyms.y)
        self.register(others.next_search_item, gtk.keysyms.n)
        
    def handle_mode(self):
        message = "command mode doesn't need to be handled"
        
    def select_mode(self):
        """Switches to command mode."""
        base.set_element("acc",[])
        base.set_overwrite(True)
        base.view().emit("select-all", False)
        base.set_element("mode", self.COMMAND_MODE)
        base.update()
        base.set_element("number", 0)
        base.set_element("select", False)
