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

from ..actions import insert, keys, lines, menus, others, text
from ..actions import fileOperations as fileOps
from ..actions import position as pos

class BindingRegistry(object):
    modes = { 0 : 'command', 1 : 'visual', 
              2: 'delete',   3 : 'insert', 
              4: 'ex', 5: 'yank', 6: 'gmode', 
              7:'cmode', 8: 'rmode', 9: 'tmode',
              10:'selection' }
              
    def __init__(self):
        self.deleteMode = delete_Mode(self)
        self.commandMode = command_Mode(self)
        self.visualMode = visual_Mode(self)
        self.insertMode = insert_Mode(self)
        self.exMode = ex_Mode(self)
        self.yankMode = yank_Mode(self)
        self.gmodeMode = gmode_Mode(self)
        self.cmodeMode = cmode_Mode(self)
        self.rmodeMode = rmode_Mode(self)
        self.tmodeMode = tmode_Mode(self) 
        self.selectionMode = selection_Mode(self)
        self.init_bindings()
        
    def init_bindings(self):
        self.register_cvs(menus.select_all_menu, gtk.keysyms.a, True, False, True)
        self.register_cvs(menus.copy_menu, gtk.keysyms.c, True, False, True)
        self.register_cvs(menus.paste_menu, gtk.keysyms.v, True, False, True)
        self.register_cvs(menus.cut_menu, gtk.keysyms.x, True, False, True)
        self.register_cv(self.insert_mode, gtk.keysyms.i)
        self.register_cv(insert.append_after, gtk.keysyms.a)
        self.register_cv(self.visual_mode, gtk.keysyms.v)
        self.register_cv(pos.move_forward, gtk.keysyms.l)
        self.register_cv(pos.move_backward, gtk.keysyms.h)
        self.register_cv(pos.move_down, gtk.keysyms.j)
        self.register_cv(pos.move_up, gtk.keysyms.k)
        self.register_cv(pos.move_word_forward, gtk.keysyms.w)
        self.register_cv(pos.move_word_backward, gtk.keysyms.b)
        self.register_cv(self.gmode_mode, gtk.keysyms.g)
        self.register_cv(pos.move_buffer_end, gtk.keysyms.G)
        self.register_cv(insert.insert_end_line, gtk.keysyms.A)
        self.register_cv(insert.insert_begin_line, gtk.keysyms.I)
        self.register_cv(insert.open_line_below, gtk.keysyms.o)
        self.register_cv(insert.open_line_above, gtk.keysyms.O)
        self.register_cv(others.undo, gtk.keysyms.u)
        self.register_cv(others.search, gtk.keysyms.slash)
        self.register_cv(self.ex_mode, gtk.keysyms.colon)
        self.register_cv(lines.indent_left, gtk.keysyms.less)
        self.register_cv(lines.indent_right, gtk.keysyms.greater)
        self.register_cv(self.tmode_mode, gtk.keysyms.t)
        
    def select_mode(self, mode):
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
        the_mode = getattr(self, "%sMode" % self.modes[mode], None)
        if the_mode is None: return
        return the_mode.retrieve(keycode, control, meta)
        
    def command_mode(self): 
        self.select_mode("command")
    def visual_mode(self): 
        self.select_mode("visual")
    def delete_mode(self): 
        self.select_mode("delete")
    def insert_mode(self): 
        self.select_mode("insert")
    def ex_mode(self): 
        self.select_mode("ex")
    def yank_mode(self): 
        self.select_mode("yank")
    def gmode_mode(self): 
        self.select_mode("gmode")
    def cmode_mode(self): 
        self.select_mode("cmode")
    def rmode_mode(self): 
        self.select_mode("rmode")
    def tmode_mode(self): 
        self.select_mode("tmode")
    def selection_mode(self): 
        self.select_mode("selection")
       
        
# vim: ai ts=4 sts=4 et sw=4
