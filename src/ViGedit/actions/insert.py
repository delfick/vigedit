import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import lines, others, text, position as pos, wrap, fileOperations as fileOps

def append_after():
    iter = pos.get_cursor_iter()
    if iter.ends_line():
        print "insert ' '"
        base.vigtk.doc.insert_at_cursor(" ")
    else:
        print "move forward cursor position" 
        base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, base.vigtk.select)
        #iter.forward_cursor_position()  
    return True
    
def insert_after():
    pos.move_forward()
    
def insert_end_line():
    pos.move_line_end()
    
def insert_begin_line():
    cursor = pos.get_cursor_iter()
    cursor.backward_sentence_start()
    base.vigtk.doc.place_cursor(cursor)
    
    
def open_line_above():
    print "Opening line above in %s" % base.vigtk.view
    pos.move_line_begin()
    mode = base.vigtk.mode
    vibase.set_mode("insert")
    base.vigtk.view.emit("insert-at-cursor", "\n")
    vibase.set_mode(mode)
    pos.move_up()

def open_line_below():
    print "Opening line below in %s" % base.vigtk.view
    pos.move_line_end()
    mode = base.vigtk.mode
    vibase.set_mode("insert")
    base.vigtk.view.emit("insert-at-cursor", "\n")
    vibase.set_mode(mode)
