#!/usr/bin/env python

import os
from distutils.file_util import *
from distutils.dir_util import *

TARGET = os.environ["HOME"] + "/.gnome2/gedit/plugins/"

if os.path.exists(TARGET) != True:
    os.mkdir(TARGET)

def install_plugin(name):
    plugin_dir = TARGET + "/" + name 
    if os.path.exists(plugin_dir) != True:
        os.mkdir(plugin_dir)
    copy_file("data/" + name.lower() + ".gedit-plugin", TARGET)
    copy_tree('src/' + name, plugin_dir)

install_plugin("ViGedit")
# Considering integration with other plugins
# install_plugin("classbrowser")

