from binding_base import *
class yank_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(self.yank_lines, gtk.keysyms.y)
        
    def handle_mode(self, event):
        return True
            
    def select_mode(self):
        base.vigtk.select = False
        base.vigtk.mode = base.vigtk.YANK_MODE
        vibase.update()
        
    def yank_lines(self):
        lines.yank_line()
        vibase.set_mode("command")
        
