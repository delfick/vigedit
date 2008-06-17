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
from ..actions import insert, lines, others, text, wrap
class binding_base:

    def __init__(self):
        self.bindingsObject = {}
        self.init_bindings()
 
    def register(self, func, keycode, isFinal=False, isRepeatable=False, returnToMode=None, control=False, meta=False):
        keycombo = keycode, control, meta
        self.bindingsObject[keycombo] = {}
        self.bindingsObject[keycombo]["function"] = func
        self.bindingsObject[keycombo]["Final"] = isFinal
        self.bindingsObject[keycombo]["Repeatable"] = isRepeatable
        self.bindingsObject[keycombo]["ReturnToMode"] = returnToMode
    
    def retrieve(self, keycode, control=False, meta=False):
        return self.bindingsObject.get((keycode, control, meta), None)
        
    def increment_accumulator(self, key):
        acc = base.acc
        base.acc = acc.append(key)
