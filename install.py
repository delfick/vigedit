#!/usr/bin/env python

import os
import sys
import shutil
from distutils.dir_util import copy_tree
class Complaint(Exception): pass

class Installer(object):
    def __init__(self, base=None, plugins=None):
        
        self.availablePlugins = ['ViGedit', 'autotab']
        
        try:
            if not base:
                self.base = os.sep.join([os.environ['HOME'], '.gnome2', 'gedit'])
            else:
                self.flag_base(base)
            
            if not plugins:
                self.plugins = [p for p in self.availablePlugins]
            else:
                self.flag_plugins(plugins)
                
        except Complaint, c:
            self.error(c)
        
        self.flags = (
            (['--help', '-h'], "Show help", self.flag_help, False),
            (['--base', '-b'], "Specify folder that holds plugins folder (default : %s)" % base, self.flag_base, True),
            (
                ['--plugins', '-p'], 
                "Comma seperated list of desired plugins to install (available : %s)" % ','.join(self.availablePlugins),    
                self.flag_plugins, 
                True
            ),
        )
        
        self.register = {}
        for flags, _, func, needsArg in self.flags:
            for flag in flags:
                self.register[flag] = (func, needsArg)
    
    def error(self, error):
        print "\nERROR : %s\n" % error
        exit()
        
    def copy(self, plugin, src, dest):
        if os.path.exists(src):
            if os.path.isdir(src):
                print "Copying directory %s to %s" % (src, dest)
                pluginFolder = os.sep.join([dest, plugin])
                if not os.path.exists(pluginFolder):
                    os.mkdir(pluginFolder)
                    
                copy_tree(src, pluginFolder)
            else:
                print "Copying file %s to %s" % (src, dest)
                shutil.copy(src, dest)
                
        else:
            raise Complaint("%s doesn't exist" % src)
            
    ########################
    ###   FLAGS
    ########################
    
    def flag_help(self, arg=None):
        print "Usage : python install.py [options]"
        print "-----------------------------------"
        lines = []
        for flags, message, _, _ in self.flags:
            lines.append((', '.join(flags), message))
        
        l1 = max(len(flags) for flags, _ in lines)
        s = "%%-%ds : %%s" % l1
        for flags, message in lines:
            print s % (flags, message)
        
        exit()
    
    def flag_base(self, arg):
        self.base = arg
    
    def flag_plugins(self, arg):
        plugins = [p.lstrip().rstrip().lower() for p in arg.split(',')]
        
        if not plugins:
            raise Complaint("You need to install atleast one plugin")
        
        available = dict([(p.lower(), p) for p in self.availablePlugins])
        matched = []
        
        #ensuring correct case
        for plugin in plugins:
            if plugin in available.keys():
                matched.append(available[plugin])
            else:
                raise Complaint("%s is not an available plugin" % plugin)
        
        self.plugins = matched
                
    ########################
    ###   INSTALLER
    ########################
    
    def install(self):
        pluginDir = os.sep.join([self.base, 'plugins'])
        if not os.path.exists(pluginDir):
            os.makedirs(pluginDir)
            
        for plugin in self.plugins:
            # copy gedit-plugin file
            geditPluginFile = os.sep.join(['data', '%s.gedit-plugin' % plugin.lower()])
            self.copy(plugin, geditPluginFile, pluginDir)
            
            initFile = os.sep.join(['src', plugin, '__init__.py'])
            singleFile = os.sep.join(['src', plugin, '%s.py' % plugin])
            
            if not os.path.exists(initFile):
                # installing a single file
                self.copy(plugin, singleFile, pluginDir)
            
            else:
                #installing directory
                self.copy(plugin, os.sep.join(['src', plugin]), pluginDir)
                
    ########################
    ###   MAIN
    ########################
        
    def main(self):
        args = sys.argv[1:]
        index = 0
        try:
            while index < len(args):
                flag = args[index]
                if flag.startswith('-'):
                    if flag in self.register:
                        func, needsArg = self.register[flag]
                        if needsArg:
                            index += 1
                            if index >= len(args):
                                raise Complaint("%s flag needs a following arguement" % flag)
                            func(args[index])
                        else:
                            func()
                    else:
                        raise Complaint("%s is an unkown flag" % flag)
                else:
                    raise Complaint("All arguements must be preceded by a flag. Try --help or -h")
                
                index += 1
                
            self.install()
            
        except Complaint, c:
            self.error(c)
        
if __name__ == '__main__':
    Installer().main()
