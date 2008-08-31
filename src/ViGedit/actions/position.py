""" functions to change the position of the iter """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, text, fileOperations as fileOps

def get_cursor_iter():
    return base.vigtk.doc.get_iter_at_mark(base.vigtk.doc.get_mark('insert'))   
    
def return_to_origin(number):
    print "moving up %d lines" % number
    while number > 0:
        move_up()
        number = number -1
    move_line_begin()
    
def go_to_line(line):
    cursor = get_cursor_iter()
    cursor.set_line(line - 1)
    base.vigtk.doc.place_cursor(cursor)
    base.vigtk.view.scroll_to_mark(base.vigtk.doc.get_mark('insert'), 0.0)
    
def to_empty_line(forward = True):
    cursor = get_cursor_iter()
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
            
def move_forward():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, base.vigtk.select)
    
def move_up():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, -1, base.vigtk.select)
    
def move_down():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, 1, base.vigtk.select)
    
def move_backward():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, -1, base.vigtk.select)
    
def move_word_forward():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_WORDS, 1, base.vigtk.select)
   
def move_word_backward():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_WORDS, -1, base.vigtk.select)
    
def move_buffer_top():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, -1, base.vigtk.select)
    
def move_buffer_end():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, 1, base.vigtk.select)
    
def move_line_end():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, 1, base.vigtk.select)
    
def move_line_begin():
    base.vigtk.view.emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, -1, base.vigtk.select)
   
    
    
    
    
