from binding_base import *
class change_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
    	#need a better way of specifying a command that is a collection of characters before I reimplement the 
    	#caw command that used to exist in cmode.
    	self.register(text.cut_till_end_of_word, gtk.keysyms.w, True, True, "insert")
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.acc = []
