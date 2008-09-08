from binding_base import *
class capture_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
    	pass
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.acc = []
