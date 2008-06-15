import gtk
from binding_base import *
from ..actions import text
from ..actions import position as pos
class delete_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        self.register(self.delete_whole_line, gtk.keysyms.d, True, True)
        self.register(self.delete_to_line_end, gtk.keysyms.dollar)
        self.register(self.delete_words, gtk.keysyms.w)
        
    def handle_mode(self, event):
        message = "this mode doesn't need to be handled"
        
    def select_mode(self):
        """Switches to 'delete' mode"""
        base.set_element("select", False)
        base.set_element("mode", self.DELETE_MODE)

    def delete_whole_line(self):
        text.delete_whole_line()
        self.bindings.select_mode("command")
        
    def delete_to_line_end(self):
        self.bindings.select_mode("visual")
        pos.move_line_end()
        text.cut_selection()
        self.bindings.select_mode("command")
        
    def delete_words(self):
        if base.acc() == []:
            print "Deleting first word. (%s)" % base.acc()
            text.cut_next_word()
            self.bindings.select_mode("command")
        else:
            print "Delete %s words." % int("".join(self.acc))
            for x in range(sum([int(x) for x in base.acc()])):
                text.cut_next_word()
            self.bindings.select_mode("command")
