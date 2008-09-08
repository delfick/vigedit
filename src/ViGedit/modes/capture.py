from binding_base import *
class capture_Mode(binding_base):

    """I don't have enough time to implement this atm, but my idea for the moment 
        (and it's a quick idea, so there may exist better ideas :p) is to :
    
        have keybindings to :
            add the next key to the current capture (where a number typed before this keybinding says how many keys to capture before accepting more capture.py keybindings.) and it would show you in the statusbar how many more keys will be captured
            
            delete the last key from the capture, and same rule for number before this keybinding as for adding.
            
            save the capture to a particular name. And maybe have an external file where we can have already defined captures (similar to say the snippets plugin, where snippets are stored externally to application)
            
            and of course a keybinding to execute a particular capture
            
        Implementation :
            have a flag that is checked by vibase->key_press_event() and determines wether it should add the key event to the current capture.
            
            then when envoking a specific capture, find a way of making gedit think each event in the capture is being envoked by the user.
            
            """
            
    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        pass
        
    def handle_mode(self, event):
        return True
        
    def select_mode(self):
        base.acc = []
