from binding_base import *
class change_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
    	self.register(None, gtk.keysyms.a, False, False)
        self.register(lambda : vibase.set_mode("tmode", ["change", base.vigtk.numLines]), gtk.keysyms.t)
    	self.register(text.cut_till_end_of_word, gtk.keysyms.w, True, True, "insert")
    	self.register_acc(text.cut_next_word, "a", gtk.keysyms.w, True, True, "insert")
    	
        
    def handle_mode(self, event):
    	
        return True
        
    def select_mode(self, option=None):
        base.acc = []
