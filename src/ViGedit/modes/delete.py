from binding_base import *
class delete_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(None, gtk.keysyms.a, False, False)
        self.register(None, gtk.keysyms.t, False, False)

        self.register(lambda : vibase.set_mode("tmode", ["delete", base.vigtk.numLines, "f"]), gtk.keysyms.t)
        self.register(text.delete_whole_lines, gtk.keysyms.d, True, True, "command")
        self.register(text.delete_to_line_end, gtk.keysyms.dollar, True, False, "command")
        self.register(text.cut_till_end_of_word, gtk.keysyms.w, True, True, "command")
        self.register_acc(text.cut_next_word, "a", gtk.keysyms.w, True, True, "command")
        
        
        self.register_acc(lambda : blocks.delete_whole("braceleft", "braceright"),   "a", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.delete_whole("parenleft", "parenright"),   "a", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.delete_whole("quotedbl", "quotedbl"),      "a", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.delete_whole("apostrophe", "apostrophe"),  "a", gtk.keysyms.apostrophe, True, True)

        self.register_acc(lambda : blocks.delete_till("braceleft"),   "t", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.delete_till("parenleft"),   "t", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.delete_till("braceright"),  "t", gtk.keysyms.braceright, True, True)
        self.register_acc(lambda : blocks.delete_till("parenright"),  "t", gtk.keysyms.parenright, True, True)
        self.register_acc(lambda : blocks.delete_till("quotedbl"),    "t", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.delete_till("apostrophe"),  "t", gtk.keysyms.apostrophe, True, True)
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self, option=None):
        """Switches to 'delete' mode"""
        base.select = False

