class BindingRegistry(object):
    modes = { 0 : 'command', 1 : 'visual', 
              2: 'delete',   3 : 'insert', 
              4: 'ex', 5: 'yank', 6: 'gmode', 
              7:'cmode', 8: 'rmode', 9: 'tmode' }

    def __init__(self):
        self.command_mode = {}   
        self.visual_mode = {}
        self.ex_mode = {}

    def register_common(self, func, keycode, control=False, meta=False):
        self.register('visual', func, keycode, control, meta)
        self.register('command', func, keycode, control, meta)

    def register(self, mode, func, keycode, control=False, meta=False):
        binding_map = getattr(self, "%s_mode" % mode, None)
        if binding_map is None: return
        keycombo = keycode, control, meta
        binding_map[keycombo] = func

    def retrieve(self, mode, keycode, control=False, meta=False):
        binding_map = getattr(self, "%s_mode" % self.modes[mode], None)
        if binding_map is None: return
        return binding_map.get((keycode, control, meta), None)
