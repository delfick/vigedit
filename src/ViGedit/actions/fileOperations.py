""" file related operations (save, close, etc) """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, others, text, position as pos

def save_file():
    if base.vigtk.doc.get_uri() != None:
        vibase.get_menu("save").activate()
    else:
        vibase.get_menu("save_as").activate()

def close_tab( save = True):
    if save and base.vigtk.window.get_active_document().get_modified():
        vibase.get_menu("file_close").activate()
    else:
        base.vigtk.window.close_tab(base.vigtk.window.get_active_tab())
    gobject.timeout_add(100, wait_until_save_dialog_done)

def wait_until_save_dialog_done():
    if base.vigtk.window.get_active_tab() and (base.vigtk.window.get_active_document().get_modified()):
        print "Window still saving..."
        return True
    else:
        print "Window done saving!"
        tab = base.vigtk.window.get_active_tab()
        if tab:
            if tab.get_state() == gedit.TAB_STATE_CLOSING:
                return True
        if base.vigtk.window.get_views() == []:
            print "No more views left, so shutting down!"
            # This gives messy messages.
            vibase.get_menu("quit").activate()
            gtk.main_quit()
        return False

def close_quit():
    tab = base.vigtk.window.get_active_tab()
    if tab.get_state() == gedit.TAB_STATE_SAVING:
        return True
    else:
        close_tab()
        return False
