import gtk
from binding_base import *
class selection_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "this mode doesn't have bindings"
        
    def handle_mode(self, event):
        if keys.isControlPressed(event) == False:
            start=base.get_element("selection_start")
            end = base.get_element("selection_end")
           # self.increment_accumulator(event)
            print "handle_selection_mode"
            base.doc().delete(start, end)
            self.bindings.select_mode("insert")
        return False
        
    def select_mode(self):
        """Switches to selection mode."""
        base.set_element("acc", [])
        base.set_element("mode", self.SELECTION_MODE)
        base.update()
