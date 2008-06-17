# -*- coding: utf-8 -*-

#  vibase.py - provides functions for managing the plugin
#  
#  Copyright (C) 2008 - Joseph Method
#  Copyright (C) 2008 - Stephen Moore
#  Copyright (C) 2006 - Trond Danielsen
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#   
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _
from vigtk import ViGtk

""" functions to determine if certain modifiers have been pressed """

def isControlPressed(event):
    ctrl = event.state & gtk.gdk.CONTROL_MASK
    if ctrl:
        return True 
    else:
        # necessary if control has been pressed on it's own
        if event.keyval == 65507:
            return True
        elif event.keyval == 65508:
            return True
        else:
            return False
            
def isAltPressed(event):
    alt = event.state & gtk.gdk.MOD1_MASK
    if alt:
        return True
    else:
        # necessary if control has been pressed on it's own
        if event.keyval == 65513:
            return True
        elif event.keyval == 65514:
            return True
        else: 
            return False
            
            
def isShiftPressed(event):
    if (event.keyval == 65505) or (event.keyval == 65506):
        return True
    else:
        return False
        
def isModifierPressed(event):
    if isControlPressed(event) == True:
        return True
    if isAltPressed(event) == True:
        return True
    if isShiftPressed(event) == True:
        return True
    return False
    
""" update/deactivate """

def update():
    ViGtk.statusbar.update(get_mode_desc())
    
def deactivate():
    ViBase.vigtk.view.disconnect(ViBase.vigtk.handler_ids[0])
    ViBase.vigtk.view.disconnect(ViBase.vigtk.handler_ids[1])
    ViBase.vigtk.view.disconnect(ViBase.vigtk.handler_ids[2])
    ViBase.vigtk.doc.disconnect(ViBase.vigtk.handler_ids[3])
    ViBase.vigtk.doc.disconnect(ViBase.vigtk.handler_ids[4])
    ViBase.vigtk.bindings.set_mode("insert")
    ViBase.vigtk.statusbar.update(None)
    ViBase.vigtk.view = None
    ViBase.vigtk.statusbar = None
    
    
""" dealing with modes """

def get_mode_desc():
    return ViBase.vigtk.get_mode_desc(ViBase.vigtk.mode)                
    
def set_mode(mode):
    ViBase.vigtk.bindings.set_mode(mode)
    
def get_mode_name():
    return ViBase.vigtk.modes[ViBase.vigtk.mode]
    
def handle_mode(mode, event):
    return ViBase.vigtk.bindings.handle_mode(mode, event)
    
    
""" dealing with menus """

def get_menu(menu):
    return ViBase.vigtk.menus.get_menu(menu)
    
def activate_menu(menu):
    return ViBase.vigtk.menus.activate_menu(menu)
    
    
""" other functions """
    
def set_overwrite(boolean):
    ViBase.vigtk.set_overwrite(boolean)
    
def increment_accumulator(event):
    ViBase.vigtk.increment_accumulator(event)
    
def set_overwrite(boolean):
    ViBase.vigtk.view.set_overwrite(boolean)    
    if ViBase.vigtk.view.get_overwrite() != boolean:
        print "Setting overwrite to %s, currently %s" % (boolean, ViBase.vigtk.view.get_overwrite())
        ViBase.vigtk.doc.emit("toggle-overwrite")
    
def is_visual_mode():
    return ViBase.vigtk.mode is ViBase.vigtk.VISUAL_MODE

def increment_accumulator(event):
    if event.keyval in range(256):
        ViBase.vigtk.acc +=chr(event.keyval) 
        
""" nice function I found here http://diveintopython.org/power_of_introspection/index.html#apihelper.divein """    
    
def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])

class ViBase:
    """ class that holds an instance of vitgk and processes certain events (see handler_ids below) """
    vigtk = None
    statusbar = None
    bindings = None
    
    def __init__(self, statusbar, view, window, bindings):
        """ iniitalise vigtk """
        ViBase.statusbar = statusbar
        ViBase.bindings = bindings
        ViBase.vigtk = ViGtk(statusbar, view, window, bindings)
        ViBase.vigtk.handler_ids = [
            ViGtk.view.connect("key-press-event", self.on_key_press_event),
            ViGtk.view.connect("button-release-event", self.on_button_release_event),
            ViGtk.view.connect("button-press-event", self.on_button_press_event),
            ViGtk.doc.connect("saved", lambda document,view: self.update()),
            ViGtk.doc.connect("loaded", lambda document, view: self.update())
            ]
        
    def update_vigtk(self, statusbar, view, window):
        """ update vigtk when the tab or window changes """
        ViBase.vigtk.update_vigtk(view, window, ViBase.bindings, statusbar)
        set_mode("command")
        
    def update(self):
        update()
        
    def deactivate(self):
        deactivate()

    def on_key_press_event(self, view, event):
        """ initial key press processing """
        
        if (len(ViBase.vigtk.acc) == 1) and (ViBase.vigtk.mode == ViBase.vigtk.RMODE): 
            set_mode("command")
            
        if view.get_buffer() != ViGtk.doc: 
            return False
            
        elif view != ViGtk.view:
            return False
            
        else:
            print "Key pressed was %s : %s" % (event.keyval, gtk.gdk.keyval_name(event.keyval))
            # Always return to command mode when Escape is pressed.
            if (event.keyval == gtk.keysyms.Escape):
                set_mode("command")
                return True
                
            # Ignored keys.  
            elif (ViBase.vigtk.mode is ViBase.vigtk.INSERT_MODE) \
                or (event.keyval in ViGtk.ignored_keys):
                    return False
                    
            # Process keypress
            else:
                return self.process_keypress(event)

    def process_keypress(self, event):
        """ second level of keypress processing
        this checks to see if the current mode has a binding that corresponds to the key combination
        if there isn't, then two things happen :
            if a number, it will add it to the end of the ViBase.vigtk.number variable
            the current mode's handle_mode function is called
        If there is a binding, then it will check if the function is callable
            if it isn't and the function is None, then the key pressed is added to the ViBase.vigtk.acc variable
            if it is callable, then it checks if it's repeatable
                if it's repeatable, then it will call the function the specified number of times (held by ViBase.vigtk.number)
                if it's not repeatable, then it calls the function, sets numLines to number and resets number and acc
                    resets ViBase.vigtk.number and ViBase.vigtk.acc
                    it then checks if it's final, 
                        if it is, then it resets numLines, number and acc
        Finally, it checks if ViBase.vigtk.returnToMode is set to something, if it is, then that mode is set        
        """
        modifiers = isControlPressed(event), isAltPressed(event)
        print "%s %s %s" % (ViBase.vigtk.mode, event.keyval, modifiers)
        should_print = ViBase.vigtk.mode != ViBase.vigtk.INSERT_MODE
        f = ViBase.vigtk.bindings.retrieve(ViBase.vigtk.mode, event.keyval, modifiers[0], modifiers[1])
        if f is None: 
            print "\tBindings don't exist"
            if event.keyval > 47 and event.keyval < 58:
                ViBase.vigtk.number = ViBase.vigtk.number *10 + event.keyval-48
            
            if event.keyval > 65455 and event.keyval < 65465:
                ViBase.vigtk.number = ViBase.vigtk.number * 10 + event.keyval-65456
                
            
            should_print = handle_mode(get_mode_name(), event)
        else:
            function = f["function"]
            isFinal = f["Final"]
            isRepeatable = f["Repeatable"]
            returnToMode = f["ReturnToMode"]
            if callable(function) is True:
                print "\tfunction is callable"
                if isRepeatable:
                    print "\tfunction is repeatable"
                    [function() for ignore in range(ViBase.vigtk.number or 1)]
                    print "resetting numbers"
                    ViBase.vigtk.number = 0
                    ViBase.vigtk.numLines = 0
                    ViBase.vigtk.acc = []
                else:
                    function()
                    ViBase.vigtk.numLines = ViBase.vigtk.number
                    ViBase.vigtk.number = 0
                    if isFinal:
                        print "\tfunction is final"
                        ViBase.vigtk.number = 0
                        ViBase.vigtk.numLines = 0
                        ViBase.vigtk.acc = []
                        
                set_mode(returnToMode)
            else:
                print "\tfunction is not callable"
                if function is None: increment_accumulator(event)
                    
        if ViBase.vigtk.returnToMode is not None:
            set_mode(ViBase.vigtk.returnToMode)
            ViBase.vigtk.returnToMode = None
        return should_print
    
    def on_button_release_event(self, event, user_data):
        """ if the user is in command mode and they select some text, 
        then they enter selection mode, if they then deselect that text, then they re-enter command mode """
        if (ViBase.vigtk.mode is ViBase.vigtk.COMMAND_MODE) or (ViBase.vigtk.mode is ViBase.vigtk.SELECTION_MODE):
            if ViBase.vigtk.doc.get_selection_bounds() != ():
                if ViBase.vigtk.already_selected:
                    set_mode("command")
                else:
                    ViBase.vigtk.selection_start, ViBase.vigtk.selection_end = ViBase.vigtk.doc.get_selection_bounds()
                    set_mode("selection")
            else:
                set_mode("command")
                
    def on_button_press_event(self, event, user_data):
        """ check if the user deselects text by clicking on already selected text, so it can be used by on_button_release_event
        to determine wether to change back to command mode or not if there is no selection """
        if ViBase.vigtk.doc.get_selection_bounds() != ():
            ViBase.vigtk.already_selected = True
        else:
            ViBase.vigtk.already_selected = False
