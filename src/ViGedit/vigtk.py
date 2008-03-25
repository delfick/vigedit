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

# Implemented:
#   h, j, k, l              --directional
#   v-stroke, v-stroke-d    --visual selection
#   dd, d$, dw              --deletion
#   y, yy                   --copying
#   :w, :wq, :q, q! :sav    --saving
#   :e name, tabnew, 
#   :tabnew name            --open document
#   /                       --searching
#   i, a, I, A, o, O        --insertion
#   caw                     --change
#
# Todo:
#
#   :num, :vsplit, :sp
#   t, r, , gq}, <, w, yw
#   -- (autoindent), (comment) 
#   Vim-like last char behavior
#   Ability to delete last line
#   readline support in ex console
#   help dialog button (embed in statusbar)
#   contextual help (tells what you can do next)
#   access to all menu shortcuts
#   refactor into smaller files
#   fix ctrl+r clash

import gtk
import gobject
import gedit
import re
import os
from gettext import gettext as _
from binding import *
from actions import *

class ViGtk(ActionsMixin):
    (COMMAND_MODE, VISUAL_MODE, DELETE_MODE, INSERT_MODE, EX_MODE, YANK_MODE, GMODE, CMODE) = range(8)
    def __init__(self, statusbar, view, window):
        self.window = window
        self.view = view
        print "__init__:     %s in %s" % (self, self.view)
        self.doc = view.get_buffer()
        self.load_menu_items()
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
        self.bindings.register_common(self.append_after, gtk.keysyms.a)
        self.bindings.register_common(self.visual_mode, gtk.keysyms.v)
        self.bindings.register_common(self.move_forward, gtk.keysyms.l)
        self.bindings.register_common(self.move_backward, gtk.keysyms.h)
        self.bindings.register_common(self.move_down, gtk.keysyms.j)
        self.bindings.register_common(self.move_up, gtk.keysyms.k)
        self.bindings.register_common(self.move_word_forward, gtk.keysyms.w)
        self.bindings.register_common(self.move_word_backward, gtk.keysyms.b)
        self.bindings.register_common(self.g_mode, gtk.keysyms.g)
        self.bindings.register_common(self.move_buffer_end, gtk.keysyms.G)
        self.bindings.register_common(self.insert_end_line, gtk.keysyms.A)
        self.bindings.register_common(self.insert_begin_line, gtk.keysyms.I)
        self.bindings.register_common(self.open_line_below, gtk.keysyms.o)
        self.bindings.register_common(self.open_line_above, gtk.keysyms.O)
        self.bindings.register_common(self.undo, gtk.keysyms.u)
        self.bindings.register_common(self.search, gtk.keysyms.slash)

        self.bindings.register('command', self.ex_mode, gtk.keysyms.colon)
        self.bindings.register('command', self.c_mode, gtk.keysyms.c)
        self.bindings.register('command', self.delete_mode, gtk.keysyms.d)
        self.bindings.register('command', self.redo_or_replace, gtk.keysyms.r)
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
        if self.doc.get_can_search_again():
            self.search_next_menu.activate()

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

    def redo_or_replace(self):
        """Does undo.""" 
        if isControlPressed(event):
            self.do_redo()
        else:
            self.replace()
        return True

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

    def g_mode(self):
        self.mode = self.GMODE

    def c_mode(self):
        self.acc = []
        self.mode = self.CMODE

    def yank_mode(self):
        self.select = False
        self.mode = self.YANK_MODE

    def visual_mode(self):
        self.mode = self.VISUAL_MODE
        self.update()
        self.select = True

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

    def evaluate_ex(self, acc):
        command = "".join(acc)
        print "ex command is %s" % command
        if command == "w":
            self.save_file()
        elif command == "wq":
            # Need to wait for file to finish saving
            self.save_file()
            gobject.timeout_add(100, self.close_quit)
        elif re.compile("sav (.+)$").match(command):
            result = re.compile("sav (.+)$").match(command).group(1)
            self.doc.save_as(result, gedit.encoding_get_current(), gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
        elif command == "q":
            self.close_tab()
        elif command == "q!":
            self.close_tab(False)
        elif command == "tabnew":
            self.window.create_tab(True)
        elif re.compile("tabnew (.+)$").match(command):
            file_name = "file://" + os.getcwd() + "/"+ re.compile("tabnew (.+)$").match(command).group(1)
            print file_name
            if not self.window.get_active_document().get_uri():
                self.window.close_tab(self.window.get_active_tab())
            self.window.create_tab_from_uri(file_name, gedit.encoding_get_utf8(), 1, True, True)
        elif re.compile("e (.+)$").match(command):
            file_name = "file://" + os.getcwd() + "/"+ re.compile("e (.+)$").match(command).group(1)
            self.window.close_tab(self.window.get_active_tab())
            self.window.create_tab_from_uri(file_name, gedit.encoding_get_utf8(), 1, True, True)

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
            elif (self.mode is self.GMODE):
                return self.handle_g_mode(event)
            elif (self.mode is self.CMODE):
                return self.handle_c_mode(event)
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
        elif event.keyval == gtk.keysyms.dollar:
            self.visual_mode()
            self.move_line_end()
            self.cut_selection()
            self.command_mode()
        elif event.keyval == gtk.keysyms.w:
            if self.acc == []:
                print "Deleting first word. (%s)" % self.acc
                self.cut_next_word()
                self.command_mode()
            else:
                print "Delete %s words." % int("".join(self.acc))
                for x in range(sum([int(x) for x in self.acc])):
                    self.cut_next_word()
                self.command_mode()    
        elif self.keyval_is_number(event):
            self.increment_accumulator(event)
        self.command_mode()
        return True

    def handle_yank_mode(self, event):
        if event.keyval == gtk.keysyms.y:
            self.yank_line()
            self.command_mode()
            return True
        self.command_mode()
        return True

    def handle_g_mode(self, event):
        if event.keyval == gtk.keysyms.g:
            self.move_buffer_top()
        # Wordy way to get_next_tab()
        elif event.keyval == gtk.keysyms.t:
            documents = self.window.get_documents()
            this_document = self.window.get_active_document()
            i = None
            for iterator, document in enumerate(documents):
                print this_document, document
                if document == this_document:
                    i = iterator + 1
                elif iterator == i:
                    print "active tab %s" % i
                    self.window.set_active_tab(self.window.get_tab_from_uri(documents[i].get_uri()))
                elif i == None:
                    self.window.set_active_tab(self.window.get_tab_from_uri(documents[0].get_uri()))
        self.command_mode()
        return True

    def handle_c_mode(self, event):
        if event.keyval == gtk.keysyms.a:
            self.acc.append('a')
        elif (event.keyval == gtk.keysyms.w) and (self.acc == ['a']):
            self.view.emit("move-cursor", gtk.MOVEMENT_WORDS, -1, self.select)
            self.visual_mode()
            self.view.emit("move-cursor", gtk.MOVEMENT_WORDS, 1, self.select)
            self.cut_selection()
            self.insert_mode()
        return True

    def handle_ex_mode(self, event):
        if (event.keyval != gtk.keysyms.Return) and (event.keyval != gtk.keysyms.BackSpace):
            self.increment_accumulator(event)
            self.update_ex_bar()
        elif event.keyval == gtk.keysyms.BackSpace:
            if self.acc:
                self.acc.pop()
                self.update_ex_bar()
        elif (self.mode is self.EX_MODE) and (event.keyval == gtk.keysyms.Return):
            self.evaluate_ex(self.acc)
            print self.window.get_views()
            if self.window.get_views != []:
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
        
# vim: ai ts=4 sts=4 et sw=4

