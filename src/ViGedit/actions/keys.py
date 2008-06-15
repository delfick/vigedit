import gtk
import gobject
import gedit

def isControlPressed(event):
    if (event.keyval == 65507) or (event.keyval == 65508):
        return True 
    else:
        return False

def isAltPressed(event):
    if (event.keyval == 65513) or (event.keyval == 65514):
        return True 
    else:
        return False
        
def isShiftPressed(event):
    if (event.keyval == 65505) or (event.keyval == 65506):
        return True
    else:
        return False
        
def isModifierPressed(event):
    if isControlPressed(event) or isAltPressed(event) or isShiftPressed(event):
        return True
    else:
        return False
