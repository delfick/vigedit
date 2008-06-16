from binding_base import *
class visual_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        message = "not much here"
        self.register(lambda : vibase.get_menu("cut").activate, gtk.keysyms.x)
        self.register(lambda : vibase.get_menu("copy").activate, gtk.keysyms.y)
        self.register(lambda : vibase.get_menu("paste").activate, gtk.keysyms.p)
        self.register(lambda : vibase.get_menu("select_all").activate, gtk.keysyms.a)
        self.register(pos.move_line_end, gtk.keysyms.dollar)
      
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.vigtk.mode = base.vigtk.VISUAL_MODE
        base.vigtk.select = True
        vibase.update()
        
