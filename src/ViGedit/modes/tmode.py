from binding_base import *
class tmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        self.option = None

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        """ moves cursor to next occurance of the next key to be pressed """
        cursor = pos.get_cursor_iter()
        count = 0
        
        while True:
            count+=1
            
            if cursor.is_end():
                break
            
            cursor.forward_char()
            
            #print cursor.get_char(), gtk.gdk.keyval_name(event.keyval)
            if cursor.get_char() == gtk.gdk.keyval_name(event.keyval):
            	if self.numTimes > 1 :
            		self.numTimes -= 1
            	else :
            		break
                    
        if self.option == "find" :
            if not cursor.is_end():
                base.vigtk.doc.place_cursor(cursor)
            vibase.set_mode("command")
        else :
            vibase.set_mode("visual")
            pos.move_forward(count)
            
            if self.option == "change" :
                text.cut_selection()
                vibase.set_mode("insert")
            elif self.option == "delete" :
                text.cut_selection()
                vibase.set_mode("command")
            
        return True
        
    def select_mode(self, option=None):
        self.option = option[0]
        self.numTimes = option[1]
        base.vigtk.acc =[]
