from binding_base import *
class command_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)       
        

    def init_bindings(self):  
        self.register(lambda : vibase.set_mode("cmode"), gtk.keysyms.c)
        self.register(lambda : vibase.set_mode("delete"), gtk.keysyms.d, False, False)
        self.register(others.redo, gtk.keysyms.r, True, True, True)
        self.register(others.undo, gtk.keysyms.u, True, True)
        self.register(text.delete_char, gtk.keysyms.Delete, True, True)
        self.register(lambda : vibase.set_mode("rmode"), gtk.keysyms.r)
        self.register(text.delete_char, gtk.keysyms.Delete)
        self.register(lines.select_line, gtk.keysyms.V)
        self.register(text.cut_until_end_of_line, gtk.keysyms.D)
        self.register(text.paste_clipboard_above, gtk.keysyms.P)
        self.register(text.paste_clipboard_below, gtk.keysyms.p)
        self.register(lambda : vibase.set_mode("yank"), gtk.keysyms.y)
        self.register(others.next_search_item, gtk.keysyms.n)
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        """Switches to command mode."""
        base.vigtk.acc = []
        vibase.set_overwrite(True)
        base.vigtk.view.emit("select-all", False)
        base.vigtk.mode = base.vigtk.COMMAND_MODE
        base.vigtk.number = 0
        base.vigtk.select = False
        vibase.update()
