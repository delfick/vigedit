from binding_base import *
class selection_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        if vibase.isModifierPressed(event) == False:
            start = base.vigtk.selection_start
            end = base.vigtk.selection_end
            vibase.increment_accumulator(event)
            base.vigtk.doc.delete(start, end)
            vibase.set_mode("insert")
            if (event.keyval == gtk.keysyms.BackSpace) or (event.keyval == gtk.keysyms.Delete):
                return True
            else:
                return False
        else:
            return False
        
    def select_mode(self):
        """Switches to selection mode."""
        base.vigtk.acc = []
        base.vigtk.mode = base.vigtk.SELECTION_MODE
        vibase.update()
