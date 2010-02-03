#!/usr/bin/env python

import os
from distutils.file_util import copy_file
from distutils.dir_util import copy_tree

GEDIT_BASE = '%s/%s' %(os.environ["HOME"], '.gnome2/gedit')
TARGET = '%s/plugins' % GEDIT_BASE

def makeFolder(target, desc):
    """Create a folder and ignore errors if that folder already exists"""
    try:
        os.makedirs(target)
        print "Made folder at %s" % target
    except OSError:
        if not os.path.exists(target):
            raise Exception, "Failed to create %s at - %s" % (desc, target)
        #Folder must already exist


#Make sure there is a plugin folder for gedit
makeFolder(TARGET, "plugin folder")

def installPlugin(name):
    #copy the .gedit-plugin file
    copy_file("data/%s.gedit-plugin" % name.lower(), TARGET)
    
    base = "src/%s" % name
    singleFile = "%s/%s.py" % (base, name.lower())
    
    if os.path.exists(singleFile):
        #plugin is only a single file
        #however that may not always be the case, but here it is, so whatever.....
        copy_file(singleFile, TARGET) 
        print "Copied %s to %s" % (singleFile, TARGET)
    else:
        #Create folder for this plugin
        pluginDir = '%s/%s' % (TARGET, name)
        makeFolder(pluginDir, "%s folder" % name)
        copy_tree("src/%s" % name, pluginDir)      
        print "Copied plugin to %s" % pluginDir

installPlugin("ViGedit")
installPlugin("autotab")

# Considering integration with other plugins
# installPlugin("classbrowser")

