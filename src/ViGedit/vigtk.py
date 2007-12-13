# -*- coding: utf-8 -*-

#  vigtk.py - Vi Keybindings for gtk.TextView.
#  
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
import gedit
import re
from gettext import gettext as _

class BindingRegistry(object):
    modes = { 0 : 'command', 1 : 'visual', 2: 'delete', 3 : 'insert', 4: 'ex', 5: 'yank' }

    visual_mode = {}
    command_mode = {}
    ex_mode = {}

    def register_common(self, func, keycode, control=False, meta=False):
        self.register('visual', func, keycode, control, meta)
        self.register('command', func, keycode, control, meta)

    def register(self, mode, func, keycode, control=False, meta=False):
        binding_map = getattr(self, "%s_mode" % mode, None)
        if binding_map is None: return
        keycombo = keycode, control, meta
        binding_map[keycombo] = func

    def retrieve(self, mode, keycode, control=False, meta=False):
        binding_map = getattr(self, "%s_mode" % self.modes[mode], None)
        if binding_map is None: return
        return binding_map.get((keycode, control, meta), None)

class ViGtk:
    (COMMAND_MODE, VISUAL_MODE, DELETE_MODE, INSERT_MODE, EX_MODE, YANK_MODE) = range(6)

    def __init__(self, statusbar, view, window):
        self.window = window
        self.view = view # view is shared across documents!!!
        self.doc = view.get_buffer()
        print "__init__:     %s in %s" % (self, self.view)
        self.statusbar = statusbar
        self.last_search = None
        self.init_commands()
        self.init_bindings()
        self.ignored_keys = map( gtk.gdk.keyval_from_name, \
                ['Up', 'Down', 'Left', 'Right', 'Page_Up', 'Page_Down', 'Home', 'End'] + \
                ["F%d" % n for n in range(1,13)] )
        self.handler_ids = [
                self.view.connect("key-press-event", self.on_key_press_event),
                self.doc.connect("saved", lambda document,view: self.update()),
                self.doc.connect("loaded", lambda document, view: self.update()),
                self.window.connect("active-tab-changed", self.on_active_tab_changed), 
                ]
        self.command_mode()

    def on_active_tab_changed(self, window, tab):
        #self.deactivate()        
        pass
        
    def init_bindings(self):
        self.bindings = BindingRegistry()

        self.bindings.register_common(self.insert_mode, gtk.keysyms.i)
        self.bindings.register_common(self.insert_after, gtk.keysyms.a)
        self.bindings.register_common(self.visual_mode, gtk.keysyms.v)
        self.bindings.register_common(self.move_forward, gtk.keysyms.l)
        self.bindings.register_common(self.move_backward, gtk.keysyms.h)
        self.bindings.register_common(self.move_down, gtk.keysyms.j)
        self.bindings.register_common(self.move_up, gtk.keysyms.k)
        self.bindings.register_common(self.move_word_forward, gtk.keysyms.w)
        self.bindings.register_common(self.move_word_backward, gtk.keysyms.b)
        self.bindings.register_common(self.move_buffer_top, gtk.keysyms.g)
        self.bindings.register_common(self.move_buffer_end, gtk.keysyms.G)
        self.bindings.register_common(self.insert_end_line, gtk.keysyms.A)
        self.bindings.register_common(self.insert_begin_line, gtk.keysyms.I)
        self.bindings.register_common(self.open_line_below, gtk.keysyms.o)
        self.bindings.register_common(self.open_line_above, gtk.keysyms.O)
        self.bindings.register_common(self.undo, gtk.keysyms.u)
        self.bindings.register_common(self.search, gtk.keysyms.slash)

        self.bindings.register('command', self.ex_mode, gtk.keysyms.colon)
        self.bindings.register('command', self.delete_mode, gtk.keysyms.d)
        self.bindings.register('command', self.do_redo, gtk.keysyms.r, True, False)
        self.bindings.register('command', self.delete_char, gtk.keysyms.x)
        self.bindings.register('command', self.select_line, gtk.keysyms.V)
        self.bindings.register('command', self.cut_until_end_of_line, gtk.keysyms.D)
        self.bindings.register('command', self.paste_clipboard_above, gtk.keysyms.P)
        self.bindings.register('command', self.paste_clipboard_above, gtk.keysyms.p)
        self.bindings.register('command', self.yank_mode, gtk.keysyms.y)
        self.bindings.register('command', self.next_search_item, gtk.keysyms.n)

        self.bindings.register('visual', self.cut_selection, gtk.keysyms.x)
        self.bindings.register('visual', self.yank_selection, gtk.keysyms.y)
        self.bindings.register('visual', self.move_line_end, gtk.keysyms.dollar)

    def next_search_item(self):
        # TODO This doesn't work at all. How to use search_forward???
        if self.doc.get_can_search_again():
            start_iter, end_iter = self.doc.get_start_iter(), self.doc.get_end_iter()
            if self.last_search != None:
                start_selection, end_selection = self.last_search
            else:
                try:
                    start_selection, end_selection = self.doc.get_selection_bounds()
                    self.last_search = (start_selection, end_selection)
                except:
                    return
            print "Performing %s" % self.doc.search_forward(self.doc.get_start_iter(), self.doc.get_end_iter(), start_selection, end_selection)
            self.doc.emit("search-highlight-updated", start_selection, end_selection)
            print "Going to next search item between (%s, %s) and (%s, %s) after (%s, %s) and (%s, %s)" % \
                (start_iter.get_line(), start_iter.get_offset(), end_iter.get_line(), end_iter.get_offset(), start_selection.get_line(), start_selection.get_offset(), end_selection.get_line(),end_selection.get_offset())
        else:
            print "No more instances of search text."

    def deactivate(self):
        self.view.disconnect(self.handler_ids[0])
        doc = self.view.get_buffer()
        doc.disconnect(self.handler_ids[1])
        doc.disconnect(self.handler_ids[2])
        self.window.disconnect(self.handler_ids[3])
        self.insert_mode()
        self.statusbar.update(None)
        self.view = None
        #self.statusbar = None

    def update(self):
        print "update:       %s in %s" % (self, self.view) 
        self.statusbar.update(self.get_mode())

    def undo(self):
        """Does undo.""" 
        self.do_undo()

    def redo_or_replace(self, event):
        """Does undo.""" 
        if isControlPressed(event):
            self.do_redo()
        else:
            return False

    def insert_mode(self):
        """Switches to insert mode."""
        self.set_overwrite(False)
        self.view.emit("select-all", False)
        self.mode = self.INSERT_MODE
        self.update()
        self.select = False

    def ex_mode(self):
        self.acc = []
        self.view.emit("select-all", False)
        self.mode = self.EX_MODE
        self.update()
        self.select = False

    def command_mode(self):
        """Switches to command mode."""
        self.acc = []
        self.set_overwrite(True)
        self.view.emit("select-all", False)
        self.mode = self.COMMAND_MODE
        self.update()
        self.select = False

    def delete_mode(self):
        """Switches to 'delete' mode"""
        self.select = False
        self.mode = self.DELETE_MODE

    def yank_mode(self):
        self.select = False
        self.mode = self.YANK_MODE

    def visual_mode(self):
        self.mode = self.VISUAL_MODE
        self.update()
        self.select = True

    def set_overwrite(self, boolean):
        self.view.set_overwrite(boolean)
        if self.view.get_overwrite() != boolean:
            print "Setting overwrite to %s, currently %s" % (boolean, self.view.get_overwrite())
            self.doc.emit("toggle-overwrite")

    def get_mode(self):
        """Get mode text"""
        return { 
                self.INSERT_MODE:_("Insert Mode"),
                self.COMMAND_MODE: _("Command Mode"),
                self.VISUAL_MODE: _("Visual Mode"),
                self.EX_MODE: _(": ")
                }.get(self.mode)


    def is_visual_mode(self):
        return self.mode is self.VISUAL_MODE


    def init_commands(self):
        self.move_up = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, -1, self.select)
        self.move_down = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, 1, self.select)
        self.move_forward = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, self.select)
        self.move_backward = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, -1, self.select)
        self.move_word_forward = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_WORDS, 1, self.select)
        self.move_word_backward = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_WORDS, -1, self.select)
        self.move_buffer_top = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, -1, self.select)
        self.move_buffer_end = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, 1, self.select)
        self.move_line_end = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, 1, self.select)
        self.move_line_begin = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, -1, self.select)
        self.search = \
                lambda: self.view.emit("start_interactive_search")
        self.delete_char = \
                lambda: self.view.emit("delete-from-cursor", gtk.DELETE_CHARS, 1)
        self.do_undo = \
                lambda: self.view.emit("undo")
        self.do_redo = \
                lambda: self.view.emit("redo")

    def paste_clipboard_above(self):
        self.view.paste_clipboard()
        self.command_mode()

    def past_clipboard_below(self):
        pass

    def yank_selection(self):
        self.view.copy_clipboard()
        self.command_mode()

    def cut_selection(self):
        self.view.cut_clipboard()
        self.command_mode()

    def insert_after(self):
        self.move_forward()
        self.insert_mode()

    def insert_end_line(self):
        self.move_line_end()
        self.insert_mode()

    def insert_begin_line(self):
        self.move_line_begin()
        self.insert_mode()

    def open_line_above(self):
        print "Opening line above in %s" % self.view
        self.move_up()
        self.move_line_end()
        self.insert_mode()
        self.view.emit("insert-at-cursor", "\n")
        
    def open_line_below(self):
        print "Opening line below in %s" % self.view
        self.move_line_end()
        self.insert_mode()
        self.view.emit("insert-at-cursor", "\n")

    def select_line(self):
        self.move_line_begin()
        self.visual_mode()
        self.move_line_end()
        self.move_forward() # Select \n too.

    def cut_until_end_of_line(self):
        self.visual_mode()
        self.move_line_end()
        self.cut_selection()

    def cut_line(self):
        self.select_line()
        self.cut_selection()

    def evaluate_ex(self, acc):
        command = "".join(acc)
        if command == "w":
            if self.doc.get_uri() != None:
                self.doc.save(gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
            else:
                # TODO how to do this?
                # self.doc.emit("saving")
                pass
        elif command == "wq":
            if self.doc.get_uri() != None:
                self.doc.save(gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
                self.window.close_tab(self.window.get_active_tab())
            # TODO needs dialogs and stuff for the other case.
            # TODO investigate warnings for this
        elif re.compile("sav (.+)$").match(command):
            result = re.compile("sav (.+)$").match(command).group(1)
            self.doc.save_as(result, gedit.encoding_get_current(), gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
        elif command == "q":
            self.window.close_tab(self.window.get_active_tab())
        # elif command == "!q":
        # TODO handle force quit case

    def yank_line(self):
        self.select_line()
        self.yank_selection()

    def increment_accumulator(self, event):
        self.acc += chr(event.keyval)

    def keyval_in_directional_keys(self, event):
        event.keyval in range(gtk.keysyms._0, gtk.keysyms._9+1)

    def update_ex_bar(self):
        self.statusbar.update(":" + "".join(self.acc))

    def on_key_press_event(self, view, event):
        if view.get_buffer() != self.doc: 
            return False
        elif view != self.view:
            return False
        else:
            print "Key pressed was %s : %s" % (event.keyval, gtk.gdk.keyval_name(event.keyval))
            # Always return to command mode when Escape is pressed.
            if (event.keyval == gtk.keysyms.Escape):
                self.command_mode()
                return True
            # Ignored keys.  
            elif (self.mode is self.INSERT_MODE) \
                or (event.keyval in self.ignored_keys):
                    return False
            # Ex mode.
            elif (self.mode is self.EX_MODE):
                return self.handle_ex_mode(event)
            # Delete mode.
            elif (self.mode is self.DELETE_MODE):
                return self.handle_delete_mode(event)
            elif (self.mode is self.YANK_MODE):
                return self.handle_yank_mode(event)
            # Increment accumulator
            elif self.keyval_in_directional_keys(event):
                self.increment_accumulator(event)
                return True
            # Process keypress
            else:
                return self.process_keypress(event)

    def handle_delete_mode(self, event):
        if event.keyval == gtk.keysyms.d:
            self.delete_whole_line()
            self.command_mode()
            return True
        elif event.keyval == gtk.keysyms.dollar:
            self.visual_mode()
            self.move_line_end()
            self.cut_selection()
            self.command_mode()
            return True
        elif event.keyval == gtk.keysyms.w:
            if self.acc == []:
                print "Deleting first word. (%s)" % self.acc
                self.cut_next_word()
                self.command_mode()
                return True
            else:
                print "Delete %s words." % int("".join(self.acc))
                for x in range(sum([int(x) for x in self.acc])):
                    self.cut_next_word()
                self.command_mode()    
                return True
        elif self.keyval_is_number(event):
            self.increment_accumulator(event)
            return True
        self.command_mode()
        return True

    def handle_yank_mode(self, event):
        if event.keyval == gtk.keysyms.y:
            self.yank_line()
            self.command_mode()
            return True
        self.command_mode()
        return True

    def keyval_is_number(self, event):
        try:
            int(chr(event.keyval))
            print "Keyval %s is a number." % chr(event.keyval)
            return True
        except:
            print "Keyval %s is not a number." % chr(event.keyval)
            return False

    def cut_next_word(self):
        self.visual_mode()
        self.move_word_forward()
        self.cut_selection()

    def delete_whole_line(self):
        self.move_line_begin()
        self.visual_mode()
        self.move_line_end()
        self.move_forward()        
        self.cut_selection()

    def handle_ex_mode(self, event):
        if (event.keyval != gtk.keysyms.Return) and (event.keyval != gtk.keysyms.BackSpace):
            self.increment_accumulator(event)
            self.update_ex_bar()
            return True
        elif event.keyval == gtk.keysyms.BackSpace:
            if self.acc:
                self.acc.pop()
                self.update_ex_bar()
            return True
        elif (self.mode is self.EX_MODE) and (event.keyval == gtk.keysyms.Return):
            self.evaluate_ex(self.acc)
            self.command_mode()
            return True

    def process_keypress(self, event):
        modifiers = isControlPressed(event), isAltPressed(event)
        print "%s %s %s" % (self.mode, event.keyval, modifiers)
        f = self.bindings.retrieve(self.mode, event.keyval, modifiers[0], modifiers[1])
        if callable(f) is True:
            [f() for ignore in range((int(''.join( ['0'] + self.acc)) or 1))]
        self.acc = []
        return True
        
def isControlPressed(event):
    ctrl = event.state & gtk.gdk.CONTROL_MASK
    if ctrl:
        return True 
    else:
        return False

def isAltPressed(event):
    return False

# vim: ai ts=4 sts=4 et sw=4

