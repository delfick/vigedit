from binding_base import *
class selection_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        print vibase.isControlPressed(event)
        if vibase.isControlPressed(event) == False:
            start = base.vigtk.selection_start
            end = base.vigtk.selection_end
            vibase.increment_accumulator(event)
            print "handle_selection_mode"
            base.vigtk.doc.delete(start, end)
            vibase.set_mode("insert")
        return False
        
    def select_mode(self):
        """Switches to selection mode."""
        base.vigtk.acc = []
        base.vigtk.mode = base.vigtk.SELECTION_MODE
        vibase.update()
