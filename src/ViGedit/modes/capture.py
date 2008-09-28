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
        self.register(self.captureNextEvents, gtk.keysyms.a, True, False, "command")
        self.register(self.clearCapturedEvents, gtk.keysyms.c, True, False, "command")
        self.register(self.emitCapturedEvents, gtk.keysyms.e, True, True)
                
    def handle_mode(self, event):
        return True
        
    def select_mode(self, option=None):
        base.acc = []
        
    def captureNextEvents(self):
        base.vigtk.captureNum = base.vigtk.number
        
    def emitCapturedEvents(self):
        vibase.set_mode(base.vigtk.initialCaptureMode)
        message = "captured keys : ["
        for nextEvent in base.vigtk.capturedEvents:
            keyName = gtk.gdk.keyval_name(nextEvent.keyval)
            
            message += "%s " % keyName
            
            if keyName == "Left":
                pos.move_backward()
            elif keyName == "Right":
                pos.move_forward()
            elif keyName == "Up":
                pos.move_up()
            elif keyName == "Down" :
                pos.move_down()
            elif keyName == "End" :
                pos.move_line_end()
            elif keyName == "Home" :
                pos.move_line_begin()
            elif keyName == "Page_Down":
            	pos.move_page_down()
            elif keyName == "Page_Up":
            	pos.move_page_up()
            else:
                base.vigtk.view.emit("key-press-event", nextEvent)
                
        print "%s]" % message
            
    def clearCapturedEvents(self):
        base.vigtk.capturedEvents = []
        base.vigtk.captureNum = 0
