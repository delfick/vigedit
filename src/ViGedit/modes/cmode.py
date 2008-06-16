from binding_base import *
class cmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(self.append_a, gtk.keysyms.a, False, False)
        self.register(self.handle_w, gtk.keysyms.w, False, False)
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.acc = []
        base.set_mode("cmode")
        vibase.update()
        
    def append_a(self):
        self.increment_accumulator('a')
        
    def handle_w(self):
        #what does this actually do?
        base.view.emit("move-cursor", gtk.MOVEMENT_WORDS, -1, base.select)
        vibase.set_mode("visual")
        base.view.emit("move-cursor", gtk.MOVEMENT_WORDS, 1, base.select)
        text.cut_selection()
        vibase.set_mode("insert")
