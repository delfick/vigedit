""" base for the different modes """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
from ..actions import fileOperations as fileOps
from ..actions import position as pos
from ..actions import insert, lines, others, text

class binding_base:

    def __init__(self):
        """ create an object to hold the bindings and initialise the bindings """
        self.bindingsObject = {}
        self.init_bindings()
 
    def register(self, func, keycode, isFinal=False, isRepeatable=False, returnToMode=None, 
    				control=False, meta=False, preservePos=False):
        """ create a key in the bindingsObject equal to the keycombo with the relevant information in it """
        keycombo = keycode, control, meta
        self.bindingsObject[keycombo] = {}
        self.bindingsObject[keycombo]["function"] = func
        self.bindingsObject[keycombo]["Final"] = isFinal
        self.bindingsObject[keycombo]["Repeatable"] = isRepeatable
        self.bindingsObject[keycombo]["ReturnToMode"] = returnToMode
        self.bindingsObject[keycombo]["PreservePos"] = preservePos
        
    def register_ppos(self, func, keycode, isFinal=False, isRepeatable=False, returnToMode=None, control=False, meta=False):
    	""" convience function so that not all the params have to be filled out if position is to be preserved """
    	self.register(func, keycode, isFinal, isRepeatable, returnToMode, control, meta, True)
    
    def retrieve(self, keycode, control=False, meta=False):
        return self.bindingsObject.get((keycode, control, meta), None)
