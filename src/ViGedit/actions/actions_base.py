vigtk = None
bindings = None
    
def select_mode(mode):
    bindings.select_mode(mode)
    
def get_element(key):
    return vigtk.get_element(key)
    
def set_element(key, data):
    vigtk.set_element(key, data)
    
def update():
    vigtk.get_element("update")()
    
def view():
    return vigtk.get_element("view")
    
def doc():
    return vigtk.get_element("doc")
    
def window():
    return vigtk.get_element("window")
    
def select():
    return vigtk.get_element("select")
    
def acc():
    return vigtk.get_element("acc")
    
def old_mode():
    return vigtk.get_element("old_mode")
    
def mode():
    return vigtk.get_element("mode")

def handler_ids():
    return vigtk.get_element("handler_ids")
    
def number():
    return vigtk.get_element("number")

def get_menu(menu):
    return vigtk.get_element("menus").get_menu(menu)
    
def set_overwrite(boolean):
    vigtk.get_element("set_overwrite")(boolean)
    
def increment_accumulator(event):
    vigtk.get_element("increment_accumulator")(event)

