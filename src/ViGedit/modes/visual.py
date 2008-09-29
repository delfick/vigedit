from binding_base import *
class visual_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        
    def init_bindings(self):
        self.register(lambda : vibase.set_mode("insert"), gtk.keysyms.i)
        
        self.register(lambda : vibase.activate_menu("cut"), gtk.keysyms.x, True)
        self.register(lambda : vibase.activate_menu("copy"), gtk.keysyms.y, True)
        self.register(lambda : vibase.activate_menu("paste"), gtk.keysyms.p, True, True)
        self.register(lambda : vibase.activate_menu("select_all"), gtk.keysyms.a, True)
        
        self.register(lambda : vibase.set_mode("tmode", ["select", base.vigtk.number, "f"]), gtk.keysyms.t)
        
        self.register(text.delete_prev_char, gtk.keysyms.X, True, True)
        self.register(pos.move_forward, gtk.keysyms.l, True, True)
        self.register(pos.move_backward, gtk.keysyms.h, True, True)
        self.register(pos.move_down, gtk.keysyms.j, True, True)
        self.register(pos.move_up, gtk.keysyms.k, True, True)
        self.register(pos.move_word_forward, gtk.keysyms.w, True, True)
        self.register(pos.move_word_backward, gtk.keysyms.b, True, True)
        self.register(pos.move_buffer_end, gtk.keysyms.G, True)
        self.register(pos.move_line_end, gtk.keysyms.dollar, True)
        self.register(pos.move_line_begin, gtk.keysyms.percent, True)        

        self.register(insert.insert_end_line, gtk.keysyms.A, True, False, "insert")
        self.register(insert.insert_begin_line, gtk.keysyms.I, True, False, "insert")
        self.register(insert.open_line_below, gtk.keysyms.o, True, True, "visual")
        self.register(insert.open_line_above, gtk.keysyms.O, True, True, "visual")

        self.register(others.undo, gtk.keysyms.u, True, True)
        self.register(others.search, gtk.keysyms.slash, True)
        
        self.register(None, gtk.keysyms.a, False, False)
        self.register(None, gtk.keysyms.t, False, False)

        self.register_acc(text.select_next_word, "a", gtk.keysyms.w, True, True)

        self.register_acc(lambda : blocks.select_whole("braceleft", "braceright"),   "a", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.select_whole("parenleft", "parenright"),   "a", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.select_whole("quotedbl", "quotedbl"),      "a", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.select_whole("apostrophe", "apostrophe"),  "a", gtk.keysyms.apostrophe, True, True)

        self.register_acc(lambda : blocks.select_till("braceleft"),   "t", gtk.keysyms.braceleft, True, True)
        self.register_acc(lambda : blocks.select_till("parenleft"),   "t", gtk.keysyms.parenleft, True, True)
        self.register_acc(lambda : blocks.select_till("braceright"),  "t", gtk.keysyms.braceright, True, True)
        self.register_acc(lambda : blocks.select_till("parenright"),  "t", gtk.keysyms.parenright, True, True)
        self.register_acc(lambda : blocks.select_till("quotedbl"),    "t", gtk.keysyms.quotedbl, True, True)
        self.register_acc(lambda : blocks.select_till("apostrophe"),  "t", gtk.keysyms.apostrophe, True, True)
        
        
        self.register_acc(lambda : lines.select_lines(base.vigtk.number), "a", gtk.keysyms.l, True, False)
      
    def handle_mode(self, event):
        """ if a modifier is pressed, let it pass through so it can be registered by gedit 
        (so you can still use ordinary shortcuts in visual mode if they haven't been overwritten in init_bindings) """
        if vibase.isModifierPressed(event) == True:
            return False
        else:
            return True
        
    def select_mode(self, option=None):
        base.vigtk.select = True
        
