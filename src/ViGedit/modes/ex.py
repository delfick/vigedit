from binding_base import *
class ex_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
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
        elif (base.vigtk.mode is base.vigtk.EX_MODE) and (event.keyval == gtk.keysyms.Return):
            others.evaluate_ex(base.vigtk.acc())
            print base.vigtk.window.get_views()
            if base.vigtk.window.get_views != []:
                vibase.set_mode("command")
        return True
        
       
        
    def select_mode(self):
        base.vigtk.acc = []
        base.vigtk.view.emit("select-all", False)
        base.vigtk.mode = base.vigtk.EX_MODE
        base.vigtk.select = False
        vibase.update()
