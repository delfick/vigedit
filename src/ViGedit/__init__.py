# -*- coding: utf-8 -*-

#  vigedit.py - Vi Keybindings for gedit.
#  
#  Copyright (C) 2006 - Trond Danielsen
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#   
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import gedit
import vibase
from modes import BindingRegistry

class VigeditStatusbar:
    def __init__(self, window):
        self.statusbar = window.get_statusbar()
        self.context_id = self.statusbar.get_context_id("VigeditStatusbar")
        
    def update(self, text=None):
        """Update statusbar"""
        self.statusbar.pop(self.context_id)
        if text is not None:
            self.statusbar.push(self.context_id, text)


class VigeditWindowHelper:
    VIEW_DATA_KEY = "VigeditPluginViewData"

    def __init__(self, plugin, window, bindings):
        self.window = window
        self.bindings = bindings
        self.oldView = None
        self.statusbar = VigeditStatusbar(window)
        print window.get_views()
        for view in window.get_views():
            self.attach_vigtk(view, window)
        self.window.connect("tab-added", self.on_tab_added)
        self.window.connect("active-tab-changed", self.on_active_tab_changed)

    def on_active_tab_changed(self, window, tab):
        print "active-tab-changed: %s with %s" % (tab, tab.get_view())

    def on_tab_added(self, window, tab):
        print "on_tab_added: attach to %s on %s" % (tab.get_view(), tab)
        self.attach_vigtk(tab.get_view(), window)
        
    def attach_vigtk(self, view, window):
        vi_plugin = vibase.ViBase(self.statusbar, view, window, self.bindings)
        print "attach_vigtk: %s in %s" % (vi_plugin, view)
        view.set_data(self.VIEW_DATA_KEY, vi_plugin)
        vi_plugin.update()

    def deactivate(self):
        for view in self.window.get_views():
            vi_plugin = view.get_data(self.VIEW_DATA_KEY)
            vi_plugin.deactivate()
            view.set_data(self.VIEW_DATA_KEY, None)
        self.window.disconnect_by_func(self.on_tab_added)
        self.window = None

    def update_ui(self):
        # TODO Something about this operation?
        tab = self.window.get_active_tab()
        if tab: 
            view = tab.get_view()
        else:
            view = self.window.get_active_view()
        if view:
            vi_plugin = view.get_data(self.VIEW_DATA_KEY)
            if vi_plugin:
           #     print "update_ui:    %s in %s" % (vi_plugin, view)
                vi_plugin.update()
        

class VigeditPlugin(gedit.Plugin):
    WINDOW_DATA_KEY = "VigeditPluginWindowData"
    
    def __init__(self):
        gedit.Plugin.__init__(self)
        self.bindings = BindingRegistry()

    def activate(self, window):
        helper = VigeditWindowHelper(self, window, self.bindings)
        window.set_data(self.WINDOW_DATA_KEY, helper)
    
    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()        
        window.set_data(self.WINDOW_DATA_KEY, None)
        
    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()

# vim: ai ts=4 sts=4 et sw=4
