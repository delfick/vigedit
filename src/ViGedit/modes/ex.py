import gtk
from binding_base import *
from ..actions import others

class ex_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "this mode doesn't have handlers"  
        
    def handle_mode(self, event):
        if event.keyval == gtk.keysyms.BackSpace:
            if self.acc:
                base.acc().pop()
                others.update_ex_bar()
        if event.keyval == gtk.keysyms.Escape:
            self.Bindings.select_mode("command")
        elif (event.keyval != gtk.keysyms.Return) and (event.keyval != gtk.keysyms.BackSpace):
            base.increment_accumulator(event)
            others.update_ex_bar()
        elif (base.mode() is self.EX_MODE) and (event.keyval == gtk.keysyms.Return):
            others.evaluate_ex(base.acc())
            print base.window().get_views()
            if base.window().get_views != []:
                self.bindings.select_mode("command")
        return True
        
       
        
    def select_mode(self):
        base.set_element("acc", [])
        base.view().emit("select-all", False)
        base.set_element("mode",self.EX_MODE)
        base.update()
        base.set_element("select", False)
