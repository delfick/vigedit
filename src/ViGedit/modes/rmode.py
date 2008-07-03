from binding_base import *
class rmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
    	if vibase.isModifierPressed(event) == False:
		    vibase.increment_accumulator(event)
		    vibase.set_overwrite(True)
		    base.vigtk.returnToMode = "command"
		    return False
        
    def select_mode(self):
        base.vigtk.acc = []
