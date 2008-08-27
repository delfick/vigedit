from binding_base import *
class indent_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)       
        

    def init_bindings(self):  
        self.register_ppos(lines.indent_left, gtk.keysyms.less, True, True, "command")
        self.register_ppos(lines.indent_right, gtk.keysyms.greater, True, True, "command")
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        """Switches to insert mode."""
        base.vigtk.select = False
