#!/usr/bin/env python

import os
from distutils.file_util import *
from distutils.dir_util import *

GEDIT_BASE = os.environ["HOME"] + "/.gnome2/gedit"
TARGET = GEDIT_BASE + "/plugins"

if os.path.exists(TARGET) != True:
    os.mkdir(GEDIT_BASE)
    os.mkdir(TARGET)

def install_plugin(name):
    plugin_dir = TARGET + "/" + name 
    copy_file("data/" + name.lower() + ".gedit-plugin", TARGET)
    base_name = "src/" + name.lower()
    single_file = base_name + "/" + name.lower() + ".py"
    if os.path.exists(single_file):
       copy_file(single_file, TARGET) 
    else:
        if os.path.exists(plugin_dir) != True:
            os.mkdir(plugin_dir)
        copy_tree("src/" + name, plugin_dir)      

install_plugin("ViGedit")
install_plugin("autotab")
# Considering integration with other plugins
# install_plugin("classbrowser")

