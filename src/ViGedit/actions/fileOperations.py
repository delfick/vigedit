import actions_base as base
import gobject
import gedit
import gtk

def save_file():
    if get_element("doc").get_uri() != None:
        base.get_menu("save").activate()
    else:
        base.get_menu("save_as").activate()

def close_tab( save = True):
    if save and base.get_element("window").get_active_document().get_modified():
        base.get_menu("file_close").activate()
    else:
        base.get_element("window").close_tab(base.get_element("window").get_active_tab())
    gobject.timeout_add(100, wait_until_save_dialog_done)

def wait_until_save_dialog_done():
    if base.get_element("window").get_active_tab() and (base.get_element("window").get_active_document().get_modified()):
        print "Window still saving..."
        return True
    else:
        print "Window done saving!"
        tab = base.get_element("window").get_active_tab()
        if tab:
            if tab.get_state() == gedit.TAB_STATE_CLOSING:
                return True
        if base.window().get_views() == []:
            print "No more views left, so shutting down!"
            # This gives messy messages.
            base.menus.get_menu("quit").activate()
            gtk.main_quit()
        return False

def close_quit():
    tab = base.get_element("window").get_active_tab()
    if tab.get_state() == gedit.TAB_STATE_SAVING:
        return True
    else:
        close_tab()
        return False
