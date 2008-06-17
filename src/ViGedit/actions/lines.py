import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, others, text, wrap, position as pos, fileOperations as fileOps

def select_lines(number):
    pos.move_line_begin()
    vibase.set_mode("visual")
    pos.move_line_end()
    pos.move_forward()
    #select the number of lines specified
    while number > 1:
        pos.move_down()
        number = number-1 

def return_to_origin(number):
    print "moving up %d lines" % number
    while number > 0:
        pos.move_up()
        number = number -1
    pos.move_line_begin()

    
def select_line():
    pos.move_line_begin()
    vibase.set_mode("visual")
    pos.move_line_end()
    pos.move_forward() # Select \n too.
    
def select_to_line_end():
    vibase.set_mode("visual")
    pos.move_line_end()

def split_lines():
    if vibase.get_menu("split_lines") == None:
        return False
    begin = pos.to_empty_line(False)
    end = pos.to_empty_line(True)
    print begin, end
    if (begin != None) and (end != None):
        base.vigtk.doc.select_range(begin, end)
        print "activate split_lines_menu"
        vibase.get_menu("split_lines").activate()
    vibase.set_mode("command")
    
def indent_left():
    number = base.vigtk.numLines
    select_lines(number)
    if vibase.get_menu("indent_left") is not None:
        vibase.get_menu("indent_left").activate()
    return_to_origin(number)

def indent_right():
    number = base.vigtk.numLines
    select_lines(number)
    if vibase.get_menu("indent_right") is not None:
        vibase.get_menu("indent_right").activate()
    return_to_origin(number)
