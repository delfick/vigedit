import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, position, text, position as pos, fileOperations as fileOps

def protect_mode(func):
    mode = base.vigtk.mode
    func()
    vibase.set_mode(mode)
    
    
def preserve_position(func):
    # ideally this would get horizontal position as well......
    cursor = base.vigtk.doc.get_insert()
    print dir(base.vigtk.doc)
    func()
    base.vigtk.doc.place_cursor(cursor)
    base.vigttk.view.scroll_to_mark(cursor, 0.0)
