from binding_base import *
class tmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        """ moves cursor to next occurance of the next key to be pressed """
        cursor = pos.get_cursor_iter()
        while True:
            cursor.forward_char()
            print cursor.get_char(), gtk.gdk.keyval_name(event.keyval)
            if cursor.get_char() == gtk.gdk.keyval_name(event.keyval):
                break
            if cursor.is_end():
                break
        if not cursor.is_end():
            base.vigtk.doc.place_cursor(cursor)
        print base.vigtk.acc
        if base.vigtk.old_mode == base.vigtk.VISUAL_MODE:
            vibase.set_mode("visual")
        else:
            vibase.set_mode("command")
        return True
        
    def select_mode(self):
        base.vigtk.acc =[]
        base.vigtk.old_mode = base.vigtk.mode
