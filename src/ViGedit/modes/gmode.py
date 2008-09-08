from binding_base import *
class gmode_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)
        

    def init_bindings(self):
        self.register(pos.move_buffer_top, gtk.keysyms.g, True, False, "command")
        self.register(self.next_tab, gtk.keysyms.t, True, True, "command")
        self.register(None, gtk.keysyms.q, True)
        self.register_acc(lines.split_lines, "q", gtk.keysyms.braceright, True, False, "command")
        
    def handle_mode(self, event):
        return True  
        
    def select_mode(self):
        base.vigtk.acc = []
        
    def next_tab(self):
        documents = base.vigtk.window.get_documents()
        this_document = base.vigtk.window.get_active_document()
        i = None
        for iterator, document in enumerate(documents):
            print this_document, document
            if document == this_document:
                i = iterator + 1
            elif iterator == i:
                print "active tab %s" % i
                base.vigtk.window.set_active_tab(base.vigtk.window.get_tab_from_uri(documents[i].get_uri()))
            elif i == None:
                base.vigtk.window.set_active_tab(base.vigtk.window.get_tab_from_uri(documents[0].get_uri()))
      
