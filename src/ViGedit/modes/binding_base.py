from ..actions import keys
from ..actions import actions_base as base
class binding_base(object):
    (COMMAND_MODE, VISUAL_MODE, DELETE_MODE, 
    INSERT_MODE, EX_MODE, YANK_MODE, GMODE, 
    CMODE, RMODE, TMODE, SELECTION_MODE) = range(11)
    def __init__(self, bindings):
        self.increment_accumulator = self.increment_accumulator
        self.bindings = bindings
        self.bindingsObject = {}
        self.init_bindings()
        
    def select_mode(self, mode):
        self.bindings.select_mode(mode)
 
    def register(self, func, keycode, isFinal=False, isRepeatable=False, control=False, meta=False):
        keycombo = keycode, control, meta
        self.bindingsObject[keycombo] = {}
        self.bindingsObject[keycombo]["function"] = func
        self.bindingsObject[keycombo]["Final"] = isFinal
        self.bindingsObject[keycombo]["Repeatable"] = isRepeatable
    
    def retrieve(self, keycode, control=False, meta=False):
        return self.bindingsObject.get((keycode, control, meta), None)
        
    def increment_accumulator(self, key):
        acc = base.get_element("acc")
        base.set_element("acc", acc.append(key))
