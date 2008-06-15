# -*- coding: utf-8 -*-

#  vigtk.py - Vi Keybindings for gtk.TextView.
#  
#  Copyright (C) 2008 - Joseph Method
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
import gobject
import gedit
import re
import os
from gettext import gettext as _
from modes import BindingRegistry
from actions.menus import menus
from actions import keys
from actions import actions_base as base

class ViGtk(object):
    (COMMAND_MODE, VISUAL_MODE, DELETE_MODE, 
    INSERT_MODE, EX_MODE, YANK_MODE, GMODE, 
    CMODE, RMODE, TMODE, SELECTION_MODE) = range(11)
    
   
    
    def __init__(self, statusbar, view, window):
        self.vigtk = {}
        self.vigtk["window"] = window
        self.vigtk["view"] = view
        self.vigtk["doc"] = view.get_buffer()
        self.vigtk["statusbar"] = statusbar
        self.vigtk["last_search"] = None
        self.vigtk["ignored_keys"] = map( gtk.gdk.keyval_from_name, \
                ['Up', 'Down', 'Left', 'Right', 'Page_Up', 'Page_Down', 'Home', 'End']) # + \
#                ["F%d" % n for n in range(1,13)] )
        self.vigtk["handler_ids"] = [
                self.vigtk["view"].connect("key-press-event", self.on_key_press_event),
                self.vigtk["view"].connect("button-release-event", self.on_button_release_event),
                self.vigtk["doc"].connect("saved", lambda document,view: self.update()),
                self.vigtk["doc"].connect("loaded", lambda document, view: self.update()),
                self.vigtk["window"].connect("active-tab-changed", self.on_active_tab_changed), 
                ]
        self.vigtk["selection_start"] = None
        self.vigtk["selection_end"] = None
        self.vigtk["menus"] = menus(self.vigtk["window"])
        self.vigtk["mode"] = self.COMMAND_MODE
        self.vigtk["update"] = getattr(self, "update")
        self.vigtk["select"] = True
        self.vigtk["acc"] = []
        self.vigtk["number"] = 1
        self.vigtk["set_overwrite"] = self.set_overwrite  
        self.vigtk["increment_accumulator"] = self.increment_accumulator
        self.vigtk["old_mode"] = self.COMMAND_MODE
           
        base.vigtk = self
        
        self.bindings = BindingRegistry()
        self.bindings.select_mode("command")
        
        base.bindings = self.bindings
        
        
        print "__init__:     %s in %s" % (self, base.view())
        
    def get_element(self, key):
        if self.vigtk[key] != None:
            return self.vigtk[key]
        return None
        
    def set_element(self, key, data):
        self.vigtk[key] = data
        
    def on_active_tab_changed(self, window, tab):
        #self.deactivate()        
        pass
    
    def on_button_release_event(self, event, user_data):
        if (base.mode() is self.COMMAND_MODE) or (base.mode() is self.SELECTION_MODE):
            if base.doc().get_selection_bounds() != ():
                self.bindings.select_mode("selection")
                self.vigtk["selection_start"], self.vigtk["selection_end"] = base.doc().get_selection_bounds()
            else:
                self.bindings.select_mode("command")

    def deactivate(self):
        base.view().disconnect(base.handler_ids()[0])
        base.view().disconnect(base.handler_ids()[1])
        base.doc().disconnect(base.handler_ids()[2])
        base.doc().disconnect(base.handler_ids()[3])
        base.window().disconnect(base.handler_ids()[4])
        self.bindings.select_mode("insert")
        base.get_element("statusbar").update(None)
        base.set_element("view", None)
        base.set_element("statusbar", None)

    def update(self):
     #   print "update:       %s in %s" % (self, base.view())
        self.get_element("statusbar").update(self.get_mode())

    def on_key_press_event(self, view, event):
        if (len(base.acc()) == 1) and (base.mode() == self.RMODE): 
            self.bindings.select_mode("command")
        if (base.mode() == self.SELECTION_MODE):
            return self.bindings.handle_mode("selection", event)
        if (base.mode() == self.EX_MODE):
            return self.bindings.handle_mode("ex", event)
        if (base.mode() == self.RMODE):
            return self.bindings.handle_mode("rmode", event)
        if (base.mode() == self.TMODE):
            return self.bindings.handle_mode("tmode", event)
        if view.get_buffer() != base.doc(): 
            return False
        elif view != base.view():
            return False
        else:
            print "Key pressed was %s : %s" % (event.keyval, gtk.gdk.keyval_name(event.keyval))
            # Always return to command mode when Escape is pressed.
            if (event.keyval == gtk.keysyms.Escape):
                self.bindings.select_mode("command")
                return True
            # Ignored keys.  
            elif (base.mode() is self.INSERT_MODE) \
                or (event.keyval in self.get_element("ignored_keys")):
                    return False
            # Process keypress
            else:
                return self.process_keypress(event)


    def process_keypress(self, event):
        modifiers = keys.isControlPressed(event), keys.isAltPressed(event)
        print "%s %s %s" % (base.mode(), event.keyval, modifiers)
        should_print = base.mode() != self.INSERT_MODE
        acc = base.acc()
        number = base.number()
        
            
        f = self.bindings.retrieve(base.mode(), event.keyval, modifiers[0], modifiers[1])
        if f is None: 
            print "\tBindings don't exist"
        else:
            function = f["function"]
            isFinal = f["Final"]
            isRepeatable = f["Repeatable"]
            if callable(function) is True:
                print "\tfunction is callable"
                if isRepeatable:
                    print "\tfunction is repeatable"
                    [function() for ignore in range(number)]
                    number = 0
                    acc = []
                else:
                    function()
                    if isFinal:
                        print "\tfunction is final"
                        number = 0
                        acc = []
            else:
                print "\tfunction is not callable"
                        
        if event.keyval > 47 and event.keyval < 58:
            number = number *10 + event.keyval-48
            
        if event.keyval > 65455 and event.keyval < 65465:
            number = number * 10 + event.keyval-65456
            
        self.set_element("number", number)
        self.set_element("acc", acc)
        print
        return should_print
        
    def get_mode(self):
        """Get mode text"""
        return { 
                self.INSERT_MODE:_("Insert Mode"),
                self.COMMAND_MODE: _("Command Mode"),
                self.VISUAL_MODE: _("Visual Mode"),
                self.EX_MODE: _(": "),
                self.SELECTION_MODE: _("Selection Mode")
                }.get(base.mode())
                
    def set_overwrite(self, boolean):
        base.view().set_overwrite(boolean)    
        if base.view().get_overwrite() != boolean:
            print "Setting overwrite to %s, currently %s" % (boolean, base.view().get_overwrite())
            base.doc().emit("toggle-overwrite")
        
        
    def is_visual_mode(self):
        return base.mode() is self.VISUAL_MODE
                

    def increment_accumulator(self, event):
        if event.keyval in range(256):
            self.vigtk["acc"] +=chr(event.keyval)      
        
        
        
        
        
        
        
        
