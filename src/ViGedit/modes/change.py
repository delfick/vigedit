from binding_base import *
class change_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(None, gtk.keysyms.a, False, False)
        self.register(None, gtk.keysyms.t, False, False)

        self.register(lambda : vibase.set_mode("tmode", ["change", base.vigtk.numLines, "f"]), gtk.keysyms.t)
        self.register(text.cut_till_end_of_word, gtk.keysyms.w, True, True, "insert")
        self.register_acc(text.cut_next_word, "a", gtk.keysyms.w, True, True, "insert")
        self.register_acc(text.cut_line, "a", gtk.keysyms.l, True, True, "insert")

        self.register_acc(lambda : blocks.change_whole("braceleft", "braceright"),   "a", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.change_whole("parenleft", "parenright"),   "a", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.change_whole("quotedbl", "quotedbl"),      "a", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.change_whole("apostrophe", "apostrophe"),  "a", gtk.keysyms.apostrophe, True, True)

        self.register_acc(lambda : blocks.change_till("braceleft"),   "t", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.change_till("parenleft"),   "t", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.change_till("braceright"),  "t", gtk.keysyms.braceright, True, True)
        self.register_acc(lambda : blocks.change_till("parenright"),  "t", gtk.keysyms.parenright, True, True)
        self.register_acc(lambda : blocks.change_till("quotedbl"),    "t", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.change_till("apostrophe"),  "t", gtk.keysyms.apostrophe, True, True)
        
        
    def handle_mode(self, event):
        
        return True
        
    def select_mode(self, option=None):
        base.acc = []
