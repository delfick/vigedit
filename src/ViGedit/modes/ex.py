from binding_base import *
class ex_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(self.evaluate_ex, gtk.keysyms.Return, True)
        self.register(self.evaluate_ex, gtk.keysyms.KP_Enter, True)
        
    def handle_mode(self, event):
        if event.keyval == gtk.keysyms.BackSpace:
            if base.vigtk.acc:
                base.vigtk.acc.pop()
                others.update_ex_bar()
                
        if event.keyval == gtk.keysyms.Escape:
            vibase.set_mode("command")
            
        elif (event.keyval != gtk.keysyms.Return) and (event.keyval != gtk.keysyms.BackSpace):
            vibase.increment_accumulator(event)
            others.update_ex_bar()
            
        return True
        
    def evaluate_ex(self):
        others.evaluate_ex(base.vigtk.acc)
        if base.vigtk.window.get_views != []:
            vibase.set_mode("command")       
       
        
    def select_mode(self):
        base.vigtk.acc = []
        base.vigtk.view.emit("select-all", False)
        base.vigtk.select = False
        
        
        
        
        
