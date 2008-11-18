""" functions for doing stuff to text """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import text, emit, blocks, insert, lines, others, position as pos, fileOperations as fileOps

""" selection """

def select_whole(the_type, other_type):
    print "finding %s" % the_type
    vibase.set_mode("tmode", ["find", 1, "b", getattr(gtk.keysyms, other_type)])
    emit.name(the_type)
    pos.move_forward()
    vibase.set_mode("tmode", ["select",1, "f", getattr(gtk.keysyms, the_type)])
    emit.name(other_type) 
    vibase.set_mode("selection")
    
def select_till(the_type):
    vibase.set_mode("tmode", ["select",1, "f"])
    emit.name(the_type) 
    vibase.set_mode("selection")
    
    
""" change """

def change_whole(the_type, other_type):
    select_whole(the_type, other_type)
    text.cut_selection()
    vibase.set_mode("insert")
    if the_type == "braceleft" and other_type == "braceright":
        open_block()
    
def change_till(the_type, other_type):
    select_till(the_type)
    text.cut_selection()
    vibase.set_mode("insert")
    
""" delete """

def delete_whole(the_type, other_type):
    select_whole(the_type, other_type)
    text.cut_selection()
    if the_type == "braceleft" and other_type == "braceright":
        vibase.set_mode("insert")
        open_block()
    vibase.set_mode("command")
    
def delete_till(the_type, other_type):
    select_till(the_type)
    text.cut_selection()
    vibase.set_mode("command")
    
    
""" other """

def open_block():
    emit.array_names(["Return", "Return", "Up", "Tab"])
