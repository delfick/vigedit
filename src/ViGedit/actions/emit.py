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

def name(name):
	nextEvent = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
	nextEvent.keyval = getattr(gtk.keysyms, name)
	nextEvent.state = gtk.gdk.MOD2_MASK
	nextEvent.time = 0 
	
	event(nextEvent)


def number(keyval):

	nextEvent = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
	nextEvent.keyval = keyval
	nextEvent.state = gtk.gdk.MODIFIER_MASK
	nextEvent.time = 0 
	
	event(nextEvent)
	
def array_names(array):
	for key in array:
		name(key)
	
	
def event(theEvent):

	keyName = gtk.gdk.keyval_name(theEvent.keyval)

	if keyName == "Left":
		pos.move_backward()
	elif keyName == "Right":
		pos.move_forward()
	elif keyName == "Up":
		pos.move_up()
	elif keyName == "Down" :
		pos.move_down()
	elif keyName == "End" :
		pos.move_line_end()
	elif keyName == "Home" :
		pos.move_line_begin()
	elif keyName == "Page_Down":
		pos.move_page_down()
	elif keyName == "Page_Up":
		pos.move_page_up()
	else:
		base.vigtk.view.emit("key-press-event", theEvent)
