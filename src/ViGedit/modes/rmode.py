from binding_base import *
class rmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        vibase.increment_accumulator(event)
        vibase.set_overwrite(True)
        return False
        
    def select_mode(self):
        base.vigtk.acc = []
        base.vigtk.mode = base.vigtk.RMODE
        vibase.update()