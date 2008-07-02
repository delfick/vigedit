from binding_base import *
class cmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(None, gtk.keysyms.a, False, False)
        self.register(self.handle_w, gtk.keysyms.w, False, False, "insert")
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.acc = []     
        
    def handle_w(self):
        """overwrite next word"""
        if base.vigtk.acc == ['a']:
            base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_WORDS, -1, base.vigtk.select)
            vibase.set_mode("visual")
            base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_WORDS, 1, base.vigtk.select)
            text.cut_selection()
