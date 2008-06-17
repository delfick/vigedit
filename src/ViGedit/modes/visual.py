from binding_base import *
class visual_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(lambda : vibase.set_mode("insert"), gtk.keysyms.i)
        self.register(lambda : vibase.set_mode("visual"), gtk.keysyms.v)
        self.register(lambda : vibase.set_mode("gmode"), gtk.keysyms.g)
        self.register(lambda : vibase.set_mode("exmode"), gtk.keysyms.colon)
        self.register(lambda : vibase.set_mode("tmode"), gtk.keysyms.t)
        self.register(lambda : vibase.set_mode("indent"), gtk.keysyms.less)
        self.register(lambda : vibase.set_mode("indent"), gtk.keysyms.greater)
        
        self.register(lambda : vibase.activate_menu("cut"), gtk.keysyms.x, True)
        self.register(lambda : vibase.activate_menu("copy"), gtk.keysyms.y, True)
        self.register(lambda : vibase.activate_menu("paste"), gtk.keysyms.p, True, True)
        self.register(lambda : vibase.activate_menu("select_all"), gtk.keysyms.a, True)
        self.register(pos.move_line_end, gtk.keysyms.dollar, True)
        
        
        self.register(pos.move_forward, gtk.keysyms.l, True, True)
        self.register(pos.move_backward, gtk.keysyms.h, True, True)
        self.register(pos.move_down, gtk.keysyms.j, True, True)
        self.register(pos.move_up, gtk.keysyms.k, True, True)
        self.register(pos.move_word_forward, gtk.keysyms.w, True, True)
        self.register(pos.move_word_backward, gtk.keysyms.b, True, True)
        self.register(pos.move_buffer_end, gtk.keysyms.G, True)        

        self.register(insert.insert_end_line, gtk.keysyms.A, True, False, "insert")
        self.register(insert.insert_begin_line, gtk.keysyms.I, True, False, "insert")
        self.register(insert.open_line_below, gtk.keysyms.o, True, True)
        self.register(insert.open_line_above, gtk.keysyms.O, True, True)
        self.register(insert.append_after, gtk.keysyms.a, True, False, "insert")

        self.register(others.undo, gtk.keysyms.u, True, True)
        self.register(others.search, gtk.keysyms.slash, True)
      
    def handle_mode(self, event):
        if vibase.isModifierPressed(event) == True:
            return False
        else:
            return True
        
    def select_mode(self):
        base.vigtk.mode = base.vigtk.VISUAL_MODE
        base.vigtk.select = True
        vibase.update()
        
