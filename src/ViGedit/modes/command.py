from binding_base import *
class command_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)       

    def init_bindings(self):
    	self.register(lambda : vibase.set_mode("example"), gtk.keysyms.E)
    	
        self.register(lambda : vibase.set_mode("cmode"), gtk.keysyms.c)
        self.register(lambda : vibase.set_mode("delete"), gtk.keysyms.d)
        self.register(lambda : vibase.set_mode("rmode"), gtk.keysyms.r)
        self.register(lambda : vibase.set_mode("yank"), gtk.keysyms.y)
        self.register(lambda : vibase.set_mode("insert"), gtk.keysyms.i)
        self.register(lambda : vibase.set_mode("visual"), gtk.keysyms.v)
        self.register(lambda : vibase.set_mode("gmode"), gtk.keysyms.g)
        self.register(lambda : vibase.set_mode("ex"), gtk.keysyms.colon)
        self.register(lambda : vibase.set_mode("tmode"), gtk.keysyms.t)
        self.register(lambda : vibase.set_mode("indent"), gtk.keysyms.less)
        self.register(lambda : vibase.set_mode("indent"), gtk.keysyms.greater)

        self.register(others.redo, gtk.keysyms.r, True, True, None, True)
        self.register(others.undo, gtk.keysyms.u, True, True)
        self.register(text.delete_char, gtk.keysyms.Delete, True, True)
        self.register(text.delete_char, gtk.keysyms.x, True, True)
        self.register(lines.select_one_line, gtk.keysyms.V, True, False, "selection")
        self.register(text.cut_until_end_of_line, gtk.keysyms.D, True, False, "command")
        self.register_ppos(text.paste_clipboard_above, gtk.keysyms.P, True, True, "command")
        self.register_ppos(text.paste_clipboard_below, gtk.keysyms.p, True, True, "command")
        self.register(others.next_search_item, gtk.keysyms.n, True, True)
        
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
        self.register(insert.open_line_below, gtk.keysyms.o, True, True, "command")
        self.register(insert.open_line_above, gtk.keysyms.O, True, True, "command")
        self.register(insert.append_after, gtk.keysyms.a, True, False, "insert")
        self.register(others.search, gtk.keysyms.slash, True)
        
    def handle_mode(self, event):
        """ if a modifier is pressed, let it pass through so it can be registered by gedit 
        (so you can still use ordinary shortcuts in command mode if they haven't been overwritten in init_bindings) """
        if vibase.isModifierPressed(event) == True:
            return False
        else:
            return True
        
    def select_mode(self):
        """Switches to command mode."""
        base.vigtk.acc = []
        vibase.set_overwrite(True)
        base.vigtk.view.emit("select-all", False)
        base.vigtk.number = 0
        base.vigtk.select = False
