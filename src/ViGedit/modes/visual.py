import gtk
from binding_base import *
from ..actions import position as pos
from ..actions import menus
class visual_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "not much here"
        self.register(menus.cut_menu, gtk.keysyms.x)
        self.register(menus.copy_menu, gtk.keysyms.y)
        self.register(menus.paste_menu, gtk.keysyms.p)
        self.register(menus.select_all_menu, gtk.keysyms.a)
        self.register(pos.move_line_end, gtk.keysyms.dollar)
      
    def handle_mode(self):
        print "visual mode doesn't need to be handled"
        
    def select_mode(self):
        base.set_element("mode", self.VISUAL_MODE)
        base.update()
        base.set_element("select", True)
