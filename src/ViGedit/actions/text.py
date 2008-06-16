import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, position as pos, fileOperations as fileOps

def delete_char():
    # TODO This doesn't quite work right.
    iter = pos.get_cursor_iter() 
    if iter.ends_line():
        print "deleting last char"
        base.vigtk.doc.delete(iter, base.vigtk.doc.get_iter_at_offset(iter.get_offset() + 1))
    else:
        print "regular delete char"
        base.vigtk.view.emit("delete-from-cursor", gtk.DELETE_CHARS, 1)
    pos.get_cursor_iter().backward_cursor_position()
    
def paste_clipboard_above():
    base.vigtk.view.paste_clipboard()
    vibase.set_mode("command")

def paste_clipboard_below():
    insert.open_line_below()
    base.vigtk.view.paste_clipboard()
    delete_char()
    pos.move_up()
    vibase.set_mode("command")
    
def yank_selection():
    base.vigtk.view.copy_clipboard()
    vibase.set_mode("command")
    
def cut_selection():
    base.vigtk.view.cut_clipboard()
    vibase.set_mode("command")    
    
def cut_until_end_of_line():
    vibase.set_mode("visual")
    pos.move_line_end()
    cut_selection()
    
def cut_line():
    select_line()
    cut_selection()
    
def yank_line():
    number = base.vigtk.number
    lines.select_lines(number)
    yank_selection()
    lines.return_to_origin(number)

def cut_next_word():
    vibase.set_mode("visual")
    pos.move_word_forward()
    cut_selection()

def delete_whole_line():
    lines.select_line() 
    cut_selection()
