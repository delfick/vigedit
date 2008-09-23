from binding_base import *
class delete_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
    	self.register(None, gtk.keysyms.a, False, False)
        self.register(lambda : vibase.set_mode("tmode", ["delete", base.vigtk.numLines]), gtk.keysyms.t)
        self.register(text.delete_whole_lines, gtk.keysyms.d, True, True, "command")
        self.register(text.delete_to_line_end, gtk.keysyms.dollar, True, False, "command")
        self.register(text.cut_till_end_of_word, gtk.keysyms.w, True, True, "command")
        self.register_acc(text.cut_next_word, "a", gtk.keysyms.w, True, True, "command")
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self, option=None):
        """Switches to 'delete' mode"""
        base.select = False

