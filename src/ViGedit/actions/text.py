""" functions for doing stuff to text """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, position as pos, fileOperations as fileOps

""" deletion """

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
    
    
def delete_whole_line():
    lines.select_line()
    cut_selection()
    
def delete_whole_lines():
    number = base.vigtk.numLines
    lines.select_lines(number)
    base.vigtk.menus.activate_menu("cut")
    delete_char()
        
def delete_to_line_end():
    lines.select_to_line_end()
    cut_selection()
    
""" copying """

def yank_line():
    number = base.vigtk.numLines
    lines.select_lines(number)
    base.vigtk.menus.activate_menu("copy")
    pos.return_to_origin(number+1)
    
def yank_selection():
    base.vigtk.view.copy_clipboard()
    
""" pasting """
    
def paste_clipboard_above():
    pos.move_line_begin()
    base.vigtk.view.paste_clipboard()
    base.vigtk.doc.insert_at_cursor("\n")

def paste_clipboard_below():
    pos.move_line_end()
    base.vigtk.doc.insert_at_cursor("\n")
    base.vigtk.view.paste_clipboard()
    
    
""" cutting """
    
def cut_selection():
    base.vigtk.view.cut_clipboard()
    
def cut_until_end_of_line():
    vibase.set_mode("visual")
    pos.move_line_end()
    cut_selection()
    
def cut_line():
    select_line()
    cut_selection()

def cut_next_word():
    vibase.set_mode("visual")
    pos.move_word_forward()
    cut_selection()



