from binding_base import *
class rmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(pos.move_backward, gtk.keysyms.BackSpace, True, False)
        
    def handle_mode(self, event):
    	if vibase.isModifierPressed(event) == False:
		    vibase.increment_accumulator(event)
		    vibase.set_overwrite(True)
		    base.vigtk.returnToMode = "command"
		    return False
        
    def select_mode(self, option=None):
        base.vigtk.acc = []
