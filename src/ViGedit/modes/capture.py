from binding_base import *
class capture_Mode(binding_base):
            
            
    """
        TODO :
                Ability to save the saved capture into a specific name (maybe even accessable across all tabs)
                Ability to load saved capture from a specific name
    """
    
    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(self.capture_next_events, gtk.keysyms.a, True, False, "command")
        self.register(self.clear_captured_events, gtk.keysyms.c, True, False, "command")
        self.register(self.emit_captured_events, gtk.keysyms.e, True, True)
                
    def handle_mode(self, event):
        return True
        
    def select_mode(self, option=None):
        base.acc = []
        
    def capture_next_events(self):
        base.vigtk.captureNum = base.vigtk.number
        
    def emit_captured_events(self):
        vibase.set_mode(base.vigtk.initialCaptureMode)
        message = "captured keys : ["
        for nextEvent in base.vigtk.capturedEvents:
            keyName = gtk.gdk.keyval_name(nextEvent.keyval)
            emit.event(nextEvent)
            message += "%s " % keyName
                
        print "%s]" % message
            
    def clear_captured_events(self):
        base.vigtk.capturedEvents = []
        base.vigtk.captureNum = 0
