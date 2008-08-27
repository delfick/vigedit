# -*- coding: utf-8 -*-

#  __init__.py - initialise the plugin
#  
#  Copyright (C) 2006 - Trond Danielsen
#  Copyright (C) 2008 - Stephen Moore
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
from actions.menus import Menus
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
    """ One of these gets created when the plugin is installed. A ViBase is
    added to each view if it already exists or as it's created. """

    VIEW_DATA_KEY = "VigeditPluginViewData"

    def __init__(self, plugin, window, bindings):
        self.window = window
        self.bindings = bindings
        self.oldView = None
        self.menus = Menus(window)
        self.statusbar = VigeditStatusbar(window)
        for view in window.get_views():
            view.set_data("statusbar", self.statusbar)
            view.set_data("menus", self.menus)
            view.set_data("window", self.window)
            view.set_data("bindings", self.bindings)
            view.set_data("mode", 0)
            self.attach_vigtk(view, window)
        self.id_1 = self.window.connect("tab-added", self.on_tab_added)
        self.id_2 = self.window.connect("active-tab-changed", self.on_active_tab_changed)

    def on_active_tab_changed(self, window, tab):
        print "active-tab-changed" # : %s with %s" % (tab, tab.get_view())
        vibase = tab.get_view().get_data(self.VIEW_DATA_KEY)
        if vibase is not None:
            tab.get_view().get_data(self.VIEW_DATA_KEY).update_vigtk(tab.get_view(), 0)

    def on_tab_added(self, window, tab):
        print "on_tab_added" #: attach to %s on %s" % (tab.get_view(), tab)
        self.attach_vigtk(tab.get_view(), window)

    def attach_vigtk(self, view, window):
        view.set_data("statusbar", self.statusbar)
        view.set_data("menus", self.menus)
        view.set_data("window", window)
        view.set_data("bindings", self.bindings)
        view.set_data("mode", 0)

        vi_plugin = vibase.ViBase(view)
        print "attach_vigtk" #: %s in %s" % (vi_plugin, view)
        view.set_data(self.VIEW_DATA_KEY, vi_plugin)
        vi_plugin.update()

    def deactivate(self):
        for view in self.window.get_views():
            vi_plugin = view.get_data(self.VIEW_DATA_KEY)
            vi_plugin.deactivate(view)
            view.get_data("statusbar").update(None)
            view.set_data(self.VIEW_DATA_KEY, None)
        self.window.disconnect(self.id_1)
        self.window.disconnect(self.id_2)
        self.window = None

    def update_ui(self):
        tab = self.window.get_active_tab()
        if tab: 
            view = tab.get_view()
        else:
            view = self.window.get_active_view()
        if view:
            vi_plugin = view.get_data(self.VIEW_DATA_KEY)
            if vi_plugin:
                vi_plugin.update()


class VigeditPlugin(gedit.Plugin):
    """ Creates the VigeditWindowHelper on activate. """

    WINDOW_DATA_KEY = "VigeditPluginWindowData"

    def __init__(self):
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
