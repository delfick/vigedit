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
    if number > 0:
        select_many_lines(number)
    else:
        select_one_line()
        
def get_lines_till_end():
    cursor = pos.get_cursor_iter()
    line = cursor.get_line()
    total = base.vigtk.doc.get_line_count()
    return total-line

def select_many_lines(number):
    will_not_reach_end = False
    linesTillEnd = get_lines_till_end()
    if linesTillEnd != number:
        will_not_reach_end = True
        
    pos.move_line_begin()
    vibase.set_mode("visual")
    #select the number of lines specified
    while number > 0:
        pos.move_down()
        number = number-1 
        
    if will_not_reach_end:
        print "didn't get to end of the file"
        pos.move_backward()
        
def select_one_line():
    pos.move_line_begin()
    vibase.set_mode("visual")
    pos.move_line_end()
    pos.move_forward() # Select \n too.

def return_to_origin(number):
    print "moving up %d lines" % number
    while number > 0:
        pos.move_up()
        number = number -1
    pos.move_line_begin()

    

    
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
