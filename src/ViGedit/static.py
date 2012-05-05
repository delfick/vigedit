from gi.repository import Gdk as gdk

########################
###
###   MODES
###
########################

class VIG_Modes(object):
    """Holds info on all the modes"""
    
    def __init__(self):
        object.__setattr__(self, 'info', {
            'command':     'Command Mode',
            'visual':      'Visual Mode',
            'visualline':  'Visual Line Mode',
            'delete':      'Delete Mode',
            'insert':      'Insert Mode',
            'ex':          'Expression Mode',
            'yank':        'Yank Mode',
            'g':           'G Mode',
            'change':      'Change Mode',
            'replace':     'Replace Mode',
            't':           'T Mode',
            'selection':   'Selection Mode',
            'indent':      'Indent Mode',
            'capture':     'Capture Mode',
            'block' :      'Block Mode',
        })
        
        object.__setattr__(self, 'infoList', self.info.keys())
        
    def getModes(self):
        return self.info.keys()
    
    def __getitem__(self, key):
        if key in self.infoList:
            return info[key]
        else:
            raise Exception, "%s is not a valid mode" % key
    
    def __getattr__(self, key):
        if key in self.infoList:
            return key
        elif key.startswith("_"):
            return object.__getattr__(self, key)
        else:
            raise Exception, "%s is not a valid mode" % key
        
    def __setattr__(self, key, value):
        raise Exception, "Can't change the modes at runtime"
    
    def __setitem__(self, key, value):
        raise Exception, "Can't change the modes at runtime"
        
modes = VIG_Modes()

########################
###
###   KEYS
###
########################

ignored_keys = map( gdk.keyval_from_name, \
                    ['Page_Up', 'Page_Down', 'Tab'] + \
                    ["F%d" % n for n in range(1,13)] 
                )
                
                
