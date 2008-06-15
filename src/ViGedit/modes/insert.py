import gtk
from binding_base import *
class insert_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "insert mode has no bindings yet"
        
    def handle_mode(self):
        message = "insert mode doesn't need to be handled"

    def select_mode(self):
        """Switches to insert mode."""
        base.set_overwrite(False)
        base.view().emit("select-all", False)
        base.set_element("mode", self.INSERT_MODE)
        base.update()
        base.set_element("select", False)
