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
import gtk
from ..actions import insert, lines, menus, others, text
from ..actions import fileOperations as fileOps
from ..actions import position as pos
from ..vibase import ViBase as base
from .. import vibase

class BindingRegistry(object):

    def init_modes(self):
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
        self.init_bindings()

    def init_bindings(self):
        self.register_cvs(lambda : vibase.get_menu("select_all").activate, gtk.keysyms.a, True, False, True)
        self.register_cvs(lambda : vibase.get_menu("copy").activate, gtk.keysyms.c, True, False, True)
        self.register_cvs(lambda : vibase.get_menu("paste").activate, gtk.keysyms.v, True, False, True)
        self.register_cvs(lambda : vibase.get_menu("cut").activate, gtk.keysyms.x, True, False, True)
        self.register_cv(lambda : self.set_mode("insert"), gtk.keysyms.i)
        self.register_cv(insert.append_after, gtk.keysyms.a)
        self.register_cv(lambda : self.set_mode("visual"), gtk.keysyms.v)
        self.register_cv(pos.move_forward, gtk.keysyms.l)
        self.register_cv(pos.move_backward, gtk.keysyms.h)
        self.register_cv(pos.move_down, gtk.keysyms.j)
        self.register_cv(pos.move_up, gtk.keysyms.k)
        self.register_cv(pos.move_word_forward, gtk.keysyms.w)
        self.register_cv(pos.move_word_backward, gtk.keysyms.b)
        self.register_cv(lambda : self.set_mode("gmode"), gtk.keysyms.g)
        self.register_cv(pos.move_buffer_end, gtk.keysyms.G)
        self.register_cv(insert.insert_end_line, gtk.keysyms.A)
        self.register_cv(insert.insert_begin_line, gtk.keysyms.I)
        self.register_cv(insert.open_line_below, gtk.keysyms.o)
        self.register_cv(insert.open_line_above, gtk.keysyms.O)
        self.register_cv(others.undo, gtk.keysyms.u)
        self.register_cv(others.search, gtk.keysyms.slash)
        self.register_cv(lambda : self.set_mode("exmode"), gtk.keysyms.colon)
        self.register_cv(lines.indent_left, gtk.keysyms.less)
        self.register_cv(lines.indent_right, gtk.keysyms.greater)
        self.register_cv(lambda : self.set_mode("tmode"), gtk.keysyms.t)

    def set_mode(self, mode):
        the_mode = getattr(self, "%sMode" % mode, None)
        if the_mode is None:return
        the_mode.select_mode()

    def handle_mode(self, mode, event):
        the_mode = getattr(self, "%sMode" % mode, None)
        if the_mode is None:return
        return the_mode.handle_mode(event)

    def register_cv(self, func, keycode, isFinal=False, isRepeatable=False, control=False, meta=False):
        self.register('visual', func, keycode, isFinal, isRepeatable, control, meta)
        self.register('command', func, keycode, isFinal, isRepeatable, control, meta)

    def register_cvs(self, func, keycode, isFinal=False, isRepeatable=False, control=False, meta=False):
        self.register('visual', func, keycode, isFinal, isRepeatable, control, meta)
        self.register('command', func, keycode, isFinal, isRepeatable, control, meta)
        self.register('selection', func, keycode, isFinal, isRepeatable, control, meta)

    def register(self, mode, func, keycode, isFinal=False, isRepeatable=False, control=False, meta=False):
        binding_map = getattr(self, "%sMode" % mode, None)
        if binding_map is None: return
        binding_map.register(func, keycode, isFinal, isRepeatable, control, meta)

    def retrieve(self, mode, keycode, control=False, meta=False):
        the_mode = getattr(self, "%sMode" % vibase.get_mode_name(), None)
        if the_mode is None: return
        return the_mode.retrieve(keycode, control, meta)


# vim: ai ts=4 sts=4 et sw=4
