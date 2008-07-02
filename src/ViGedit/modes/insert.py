from binding_base import *
class insert_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        return False

    def select_mode(self):
        """Switches to insert mode."""
        vibase.set_overwrite(False)
        base.vigtk.view.emit("select-all", False)
        base.vigtk.select = False
        
