""" functions that do something before and after a certain other function """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, position, text, position as pos, fileOperations as fileOps

def preserve_mode(func):
    """ returns to the active mode previous to calling the specified function """
    mode = base.vigtk.mode
    func()
    vibase.set_mode(mode)
    
    
def preserve_position(func):
    """ returns the iter to it's position prior to calling the specified function """
    origin = base.vigtk.doc.get_insert()
    cursor = base.vigtk.doc.get_iter_at_mark(origin)
    line = cursor.get_line()
    lineOffset = cursor.get_line_offset()
    
    func()
    
    origin = base.vigtk.doc.get_insert()
    cursor = base.vigtk.doc.get_iter_at_mark(origin)
    cursor.set_line(line)
    cursor.set_line_offset(lineOffset)    
    origin = base.vigtk.doc.move_mark_by_name("insert", cursor)   
   
def preserve_position_and_mode(func):
    preserve_mode(lambda : preserve_position(func))
