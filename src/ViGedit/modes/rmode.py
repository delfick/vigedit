import gtk
from binding_base import *
class rmode_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "rmode has no bindings"
        
    def handle_mode(self, event):
        base.increment_accumulator(event)
        base.set_overwrite(True)
        return False
        
    def select_mode(self):
        base.set_element("acc", [])
        base.set_element("mode", self.RMODE)
