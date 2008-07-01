import gtk
from vigtk import ViGtk

""" functions to determine if certain modifiers have been pressed """

def isControlPressed(event):
    ctrl = event.state & gtk.gdk.CONTROL_MASK
    if ctrl:
        return True 
    else:
        # necessary if control has been pressed on it's own
        if event.keyval == 65507:
            return True
        elif event.keyval == 65508:
            return True
        else:
            return False

def isAltPressed(event):
    alt = event.state & gtk.gdk.MOD1_MASK
    if alt:
        return True
    else:
        # necessary if control has been pressed on it's own
        if event.keyval == 65513:
            return True
        elif event.keyval == 65514:
            return True
        else: 
            return False


def isShiftPressed(event):
    if (event.keyval == 65505) or (event.keyval == 65506):
        return True
    else:
        return False

def isModifierPressed(event):
    if isControlPressed(event) == True:
        return True
    if isAltPressed(event) == True:
        return True
    if isShiftPressed(event) == True:
        return True
    return False

def isDirectionalPressed(event):
	if event.keyval == gtk.keysyms.Up:
		return True
	elif event.keyval == gtk.keysyms.Down:
		return True
	elif event.keyval == gtk.keysyms.Left:
		return True
	elif event.keyval == gtk.keysyms.Right:
		return True
	else:
		return False

""" nice function I found here http://diveintopython.org/power_of_introspection/index.html#apihelper.divein """    

def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.

    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
        (method.ljust(spacing),
            processFunc(str(getattr(object, method).__doc__)))
        for method in methodList])

    return True
