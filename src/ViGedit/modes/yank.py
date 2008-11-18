from binding_base import *
class yank_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(None, gtk.keysyms.a, False, False)
        self.register(None, gtk.keysyms.t, False, False)

        self.register(lambda : vibase.set_mode("tmode", ["copy", base.vigtk.numLines, "f"]), gtk.keysyms.t)
        self.register_ppos(text.yank_line, gtk.keysyms.y, True, True, "command")
        self.register_ppos(text.yank_to_line_end, gtk.keysyms.dollar, True, False, "command")
        self.register_ppos(text.yank_till_end_of_word, gtk.keysyms.w, True, True, "command")
        self.register_ppos_acc(text.yank_next_word, "a", gtk.keysyms.w, True, True, "command")
        
        
        self.register_ppos_acc(lambda : blocks.yank_whole("braceleft", "braceright"),   "a", gtk.keysyms.braceleft, True, True)
        self.register_ppos_acc(lambda : blocks.yank_whole("parenleft", "parenright"),   "a", gtk.keysyms.parenleft, True, True)
        self.register_ppos_acc(lambda : blocks.yank_whole("quotedbl", "quotedbl"),      "a", gtk.keysyms.quotedbl, True, True)
        self.register_ppos_acc(lambda : blocks.yank_whole("apostrophe", "apostrophe"),  "a", gtk.keysyms.apostrophe, True, True)

        self.register_ppos_acc(lambda : blocks.yank_till("braceleft"),   "t", gtk.keysyms.braceleft, True, True)
        self.register_ppos_acc(lambda : blocks.yank_till("parenleft"),   "t", gtk.keysyms.parenleft, True, True)
        self.register_ppos_acc(lambda : blocks.yank_till("braceright"),  "t", gtk.keysyms.braceright, True, True)
        self.register_ppos_acc(lambda : blocks.yank_till("parenright"),  "t", gtk.keysyms.parenright, True, True)
        self.register_ppos_acc(lambda : blocks.yank_till("quotedbl"),    "t", gtk.keysyms.quotedbl, True, True)
        self.register_ppos_acc(lambda : blocks.yank_till("apostrophe"),  "t", gtk.keysyms.apostrophe, True, True)
        
    def handle_mode(self, event):
        return True
            
    def select_mode(self, option=None):
        base.vigtk.select = False
        
