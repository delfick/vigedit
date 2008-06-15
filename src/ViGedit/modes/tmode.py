import gtk
from binding_base import *
from ..actions import position as pos

class tmode_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        message = "tmode has no bindings"
        
    def handle_mode(self, event):
        cursor = pos.get_cursor_iter()
        while True:
            cursor.forward_char()
            print cursor.get_char(), gtk.gdk.keyval_name(event.keyval)
            if cursor.get_char() == gtk.gdk.keyval_name(event.keyval):
                break
            if cursor.is_end():
                break
        if not cursor.is_end():
            base.doc().place_cursor(cursor)
        print base.acc()
        if base.old_mode() == self.VISUAL_MODE:
            self.bindings.select_mode("visual")
        else:
            self.bindings.select_mode("command")
        return True
        
    def select_mode(self):
        base.set_element("acc",[])
        base.set_element("old_mode", base.mode())
        base.set_element("mode", self.TMODE)
