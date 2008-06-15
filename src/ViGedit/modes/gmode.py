import gtk
from binding_base import *
from ..actions import position as pos
from ..actions import lines
class gmode_Mode(binding_base):

    def __init__(self, bindings):
        binding_base.__init__(self, bindings)
        

    def init_bindings(self):
        self.register(pos.move_buffer_top, gtk.keysyms.g)
        self.register(self.next_tab, gtk.keysyms.t)
        self.register(self.append_q, gtk.keysyms.q)
        
    def handle_mode(self, event):
        print "handle_g_mode"
        if event.keyval in (gtk.keysyms.Shift_L, gtk.keysyms.Shift_R):
            return True
        elif (event.keyval == gtk.keysyms.braceright) and (self.acc == ["q"]):
            print "hit gq}"
            lines.split_lines()
        self.bindings.select_mode("command")
        return True  
        
    def select_mode(self):
        base.set_element("acc", [])
        base.set_element("mode",self.GMODE)
        
    def next_tab(self):
        documents = base.window().get_documents()
        this_document = base.window().get_active_document()
        i = None
        for iterator, document in enumerate(documents):
            print this_document, document
            if document == this_document:
                i = iterator + 1
            elif iterator == i:
                print "active tab %s" % i
                base.window().set_active_tab(base.window().get_tab_from_uri(documents[i].get_uri()))
            elif i == None:
                base.window().set_active_tab(base.window().get_tab_from_uri(documents[0].get_uri()))
                
    def append_q(self):
        self.increment_accumulator('q')
    
      
