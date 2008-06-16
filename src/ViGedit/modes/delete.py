from binding_base import *
class delete_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(self.delete_whole_line, gtk.keysyms.d, True, True)
        self.register(self.delete_to_line_end, gtk.keysyms.dollar)
        self.register(self.delete_words, gtk.keysyms.w)
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        """Switches to 'delete' mode"""
        base.select = False
        base.vigtk.mode = base.vigtk.DELETE_MODE
        vibase.update()
        return "hi"

    def delete_whole_line(self):
        print "trying to delete the whole line"
        text.delete_whole_line()
        vibase.set_mode("command")
        
    def delete_to_line_end(self):
        vibase.set_mode("visual")
        pos.move_line_end()
        text.cut_selection()
        vibase.set_mode("command")
        
    def delete_words(self):
        if base.vigtk.acc == []:
            print "Deleting first word. (%s)" % base.vigtk.acc
            text.cut_next_word()
            vibase.set_mode("command")
        else:
            print "Delete %s words." % int("".join(base.vigtk.acc()))
            for x in range(sum([int(x) for x in base.vigtk.acc()])):
                text.cut_next_word()
            vibase.set_mode("command")
