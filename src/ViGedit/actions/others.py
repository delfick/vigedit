""" random functions """
import gtk
import re
import gedit
import gobject
import os
from gettext import gettext as _

from .. import vibase
from ..vibase import ViBase as base
import insert, lines, text, position as pos, fileOperations as fileOps

def next_search_item():
    if base.vigtk.doc.get_can_search_again():
        vibase.get_menu("search_next").activate()
       
def search():
    base.vigtk.view.emit("start_interactive_search")
    
def undo():
    base.vigtk.view.emit("undo")
    
def redo():
    base.vigtk.view.emit("redo")

def update_ex_bar():
    base.vigtk.statusbar.update(":" + "".join(base.vigtk.acc))
    
def evaluate_ex(acc):
    command = "".join(acc)
    print "ex command is %s" % command
    if command == "w":
        fileOps.save_file()
    elif command == "wq":
        # Need to wait for file to finish saving
        fileOps.save_file()
        gobject.timeout_add(100, fileOps.close_quit)
    elif re.compile("sav (.+)$").match(command):
        result = re.compile("sav (.+)$").match(command).group(1)
        # this doesn't seem to work
        # base.vigtk.doc.save_as(result, gedit.encoding_get_current(), gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
    elif re.compile("(\d+).*").match(command):
        result = re.compile("(\d+).*").match(command).group(1)
        print "Go to line %s" % result
        pos.go_to_line(int(result))
    elif command == "q":
        fileOps.close_tab()
    elif command == "q!":
        fileOps.close_tab(False)
    elif command == "tabnew":
        base.vigtk.window.create_tab(True)
    elif command == "bn":
        print "Select next tab"
    elif command == "bp":
        print "Select previous tab."
    elif re.compile("tabnew (.+)$").match(command):
        # os.getcwd seems to only get the home directory
        file_name = "file://" + os.getcwd() + "/"+ re.compile("tabnew (.+)$").match(command).group(1)
        if not base.vigtk.window.get_active_document().get_uri():
            base.vigtk.window.close_tab(base.vigtk.window.get_active_tab())
        base.vigtk.window.create_tab_from_uri(file_name, gedit.encoding_get_utf8(), 1, True, True)
    elif re.compile("e (.+)$").match(command):
        file_name = "file://" + os.getcwd() + "/"+ re.compile("e (.+)$").match(command).group(1)
        base.vigtk.window.close_tab(base.vigtk.window.get_active_tab())
        base.vigtk.window.create_tab_from_uri(file_name, gedit.encoding_get_utf8(), 1, True, True)
