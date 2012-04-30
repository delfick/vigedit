import gedit
from vigtk import VIG_Window

class VigeditPlugin(gedit.Plugin):
    """ Creates the VigeditWindowHelper on activate. """

    def activate(self, window):
        vigtk = VIG_Window(window)
        window.set_data("vigedit", vigtk)

    def deactivate(self, window):
        window.get_data("vigedit").deactivate()
        window.set_data("vigedit", None)
        
    def update_ui(self, window):
        window.get_data("vigedit").updateUI()
        
