import gobject

def nextSearchItem(act):
    if act.vibase.doc.get_can_search_again():
        act.menus["searchNext"].activate()
       
def search(act):
    act.vibase.view.emit("start_interactive_search")
    
def undo(act):
    act.vibase.view.emit("undo")
    
def redo(act):
    act.vibase.view.emit("redo")

def getTerminal(act):
    # Get the terminal
    # TODO Probably needs a more sophisticated lookup, e.g., python terminal not installed, etc.
    window = act.vigtk.window 
    bottom_panel = window.get_bottom_panel()
    notebook = bottom_panel.get_children()[0].get_children()[0]
    if len(notebook.get_children()) != 0: 
        terminal = notebook.get_children()[1]
        return terminal
    return None   
