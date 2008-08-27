from binding_base import *
class yank_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register_ppos(text.yank_line, gtk.keysyms.y, True, True, "command")
        
    def handle_mode(self, event):
        return True
            
    def select_mode(self):
        base.vigtk.select = False
        
