#!/usr/bin/env python
import os
home = os.environ["HOME"]
target = home + "/.gnome2/gedit/plugins/"

from distutils.file_util import *
from distutils.dir_util import *

copy_file('data/vigedit.gedit-plugin', target)
copy_tree('src/ViGedit', target)

