import gtk
import gobject
import gedit

def isControlPressed(event):
    ctrl = event.state & gtk.gdk.CONTROL_MASK
    if ctrl:
        return True 
    else:
        return False

def isAltPressed(event):
    return False

class ActionsMixin(object):

    def load_menu_items(self):
        self.ui_manager = self.window.get_ui_manager()
        print self.ui_manager.get_ui()
        self.menubar = self.window.get_children()[0].get_children()[0]
        self.save_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveMenu")
        self.save_as_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveAsMenu")
        self.search_next_menu = self.ui_manager.get_action("/MenuBar/SearchMenu/SearchFindNextMenu")
        self.quit_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileQuitMenu")
        self.file_close_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileCloseMenu")
        self.indent_right_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Indent")
        self.indent_left_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Unindent")
        self.split_lines_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/SplitLines")
        self.join_lines_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/JoinLines")

    def set_overwrite(self, boolean):
        self.view.set_overwrite(boolean)
        if self.view.get_overwrite() != boolean:
            print "Setting overwrite to %s, currently %s" % (boolean, self.view.get_overwrite())
            self.doc.emit("toggle-overwrite")

    def go_to_line(self, line):
        cursor = self.get_cursor_iter()
        cursor.set_line(line - 1)
        self.doc.place_cursor(cursor)
        self.view.scroll_to_mark(self.doc.get_mark('insert'))
    
    def to_empty_line(self, forward = True):
        cursor = self.get_cursor_iter()
        while True:
            if forward:
                cursor.forward_line()
            else:
                cursor.backward_line()

            print "=======forward(%s)====%s" % (forward, cursor.get_line() + 1)

            while True:
                print cursor.get_line_offset()
                if cursor.starts_line():
                    break
                cursor.backward_char()

            end_cursor = cursor.copy()
            if not end_cursor.ends_line():
                end_cursor.forward_to_line_end()
            text = cursor.get_text(end_cursor)
            print text.__repr__()
            print "Is space: %s" % text.isspace()
            print "========================="
            if text.isspace() or (len(text) == 0):
                print "text is space"
                return cursor
            elif cursor.is_start():
                return cursor
            elif end_cursor.is_end():
                return end_cursor
                
    def split_lines(self):
        if self.split_lines_menu == None:
            return False
        begin = self.to_empty_line(False)
        end = self.to_empty_line(True)
        print begin, end
        if (begin != None) and (end != None):
            self.doc.select_range(begin, end)
            print "activate split_lines_menu"
            self.split_lines_menu.activate()
        self.command_mode()
        
    def get_cursor_iter(self):
        return self.doc.get_iter_at_mark(self.doc.get_mark('insert'))    

    def indent_left(self):
        if self.indent_left_menu:
            self.indent_left_menu.activate()

    def indent_right(self):
        if self.indent_right_menu:
            self.indent_right_menu.activate()

    def append_after(self):
        iter = self.get_cursor_iter()
        if iter.ends_line():
            print "insert ' '"
            self.doc.insert_at_cursor(" ")
        else:
            print "move forward cursor position" 
            self.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, self.select)
            #iter.forward_cursor_position() 
        self.insert_mode()
        return True

    def move_forward(self):
        self.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, self.select)

    def init_commands(self):
        self.move_up = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, -1, self.select)
        self.move_down = \
                lambda: self.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, 1, self.select)
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
        self.do_undo = \
                lambda: self.view.emit("undo")
        self.do_redo = \
                lambda: self.view.emit("redo")

    def delete_char(self):
        #TODO This doesn't quite work right.
        iter = self.get_cursor_iter() 
        if iter.ends_line():
            print "deleting last char"
            self.doc.delete(iter, self.doc.get_iter_at_offset(iter.get_offset() + 1))
        else:
            print "regular delete char"
            self.view.emit("delete-from-cursor", gtk.DELETE_CHARS, 1)
        self.get_cursor_iter().backward_cursor_position()

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
        cursor = self.get_cursor_iter()
        cursor.backward_sentence_start()
        self.doc.place_cursor(cursor)
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

    def save_file(self):
        if self.doc.get_uri() != None:
            self.save_menu.activate()
        else:
            self.save_as_menu.activate()
    
    def close_tab(self, save = True):
        if save and self.window.get_active_document().get_modified():
            self.file_close_menu.activate()
        else:
            self.window.close_tab(self.window.get_active_tab())
        gobject.timeout_add(100, self.wait_until_save_dialog_done)

    def wait_until_save_dialog_done(self):
        if self.window.get_active_tab() and (self.window.get_active_document().get_modified()):
            print "Window still saving..."
            return True
        else:
            print "Window done saving!"
            tab = self.window.get_active_tab()
            if tab:
                if tab.get_state() == gedit.TAB_STATE_CLOSING:
                    return True
            if self.window.get_views() == []:
                print "No more views left, so shutting down!"
                # This gives messy messages.
                self.quit_menu.activate()
                gtk.main_quit()
            return False

    def close_quit(self):
        tab = self.window.get_active_tab()
        if tab.get_state() == gedit.TAB_STATE_SAVING:
            return True
        else:
            self.close_tab()
            return False

    def yank_line(self):
        self.select_line()
        self.yank_selection()

    def increment_accumulator(self, event):
        self.acc += chr(event.keyval)

    def keyval_in_directional_keys(self, event):
        event.keyval in range(gtk.keysyms._0, gtk.keysyms._9+1)

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
