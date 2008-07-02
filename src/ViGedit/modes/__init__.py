from command import command_Mode
from visual import visual_Mode
from delete import delete_Mode
from insert import insert_Mode
from ex import ex_Mode
from yank import yank_Mode
from gmode import gmode_Mode
from cmode import cmode_Mode
from rmode import rmode_Mode
from tmode import tmode_Mode
from selection import selection_Mode
from indent import indent_Mode
import gtk
from ..actions import insert, lines, menus, others, text
from ..actions import fileOperations as fileOps
from ..actions import position as pos
from ..vibase import ViBase as base
from .. import vibase

class BindingRegistry(object):

    def init_modes(self):
        """ initialise the different modes 
        This calls their init_bindings method, which registers the different bindings for each mode """
        
        self.deleteMode = delete_Mode()
        self.commandMode = command_Mode()
        self.visualMode = visual_Mode()
        self.insertMode = insert_Mode()
        self.exMode = ex_Mode()
        self.yankMode = yank_Mode()
        self.gmodeMode = gmode_Mode()
        self.cmodeMode = cmode_Mode()
        self.rmodeMode = rmode_Mode()
        self.tmodeMode = tmode_Mode()
        self.selectionMode = selection_Mode()
        self.indentMode = indent_Mode()

    def set_mode(self, mode):
        the_mode = getattr(self, "%sMode" % mode, None)
        if the_mode is None:return
        the_mode.select_mode()
        mode_number = vibase.get_mode_number(mode)
        base.vigtk.mode = mode_number
        base.vigtk.view.set_data("mode", mode_number)
        vibase.update()

    def handle_mode(self, mode, event):
        the_mode = getattr(self, "%sMode" % mode, None)
        if the_mode is None:return
        return the_mode.handle_mode(event)

    def retrieve(self, mode, keycode, control=False, meta=False):
        """ retrieve a binding from the current mode if it exists """
        the_mode = getattr(self, "%sMode" % vibase.get_mode_name(), None)
        if the_mode is None: return
        return the_mode.retrieve(keycode, control, meta)


# vim: ai ts=4 sts=4 et sw=4
