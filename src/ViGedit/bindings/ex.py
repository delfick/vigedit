from base import VIG_ModeBase
import os
import glob
import re

class MODE_options(object):
    """Options object for this mode"""
    def __init__(self, act, options=None):
        self.history = []
        self.index = 0

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(self.evaluateEx,            act.gtk.keysyms.Return,   ignoreStack=True)
        self.reg(self.evaluateEx,            act.gtk.keysyms.KP_Enter, ignoreStack=True)
        self.reg(self.cycleCompletions,      act.gtk.keysyms.Tab)
        self.reg(self.cyleHistoryBackward,   act.gtk.keysyms.Up)
        self.reg(self.cyleHistoryForward,    act.gtk.keysyms.Down)
    
    def status(self, act):
        if act.vibase.stack:
            return ":" + "".join(act.vibase.stack)
        else:
            return "%s (start typing command)" % VIG_ModeBase.status(self, act)
            
    def intro(self, act, options=None):
        VIG_ModeBase.intro(self, act, options)
        #I want the history to survive for the entire window
        if not hasattr(act.vigtk, "exOptions"):
            #we want the options object to only be initialised once
            act.vigtk.exOptions = MODE_options(act, options)
        
    def handle(self, act, event):
        options = act.vigtk.exOptions
        if event.keyval == act.gtk.keysyms.BackSpace:
            if act.vibase.stack:
                act.vibase.stack.pop()
                
        if event.keyval == act.gtk.keysyms.Escape:
            act.bindings.mode = act.modes.command
            
        elif event.keyval not in (act.gtk.keysyms.Return, act.gtk.keysyms.BackSpace):
            act.vibase.addToStack(event)
        return True      
    
    def cyleHistoryBackward(self, act):
        options = act.vigtk.exOptions
        options.history.append("".join(act.vibase.stack))
        if len(options.history) < options.index:
            options.index -= 1
            act.vibase.stack = list(options.history[options.index])
            
    def cyleHistoryForward(self, act):
        options = act.vigtk.exOptions
        if len(options.history) > options.index:
            options.index += 1
            act.vibase.stack = list(options.history[options.index])

    def cycleCompletions(self, act, up = True): 
        act.trace.info(1, "TODO : make tab completion work")
        #I didn't like the previous code for this and removed it
        #At some point I'll come back and reimplement tab completion
        #unless someone else does it for me :p   
        
    def evaluateEx(self, act):
        command = "".join(act.vibase.stack)
        act.trace.info(1, "evaluating expression %s" % command)
        act.ex.evaluate(act, command)
            
              
