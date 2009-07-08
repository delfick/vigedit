from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(self.nop, act.gtk.keysyms.c,       after = act.modes.change)
        self.reg(self.nop, act.gtk.keysyms.C,       after = act.modes.capture)
        self.reg(self.nop, act.gtk.keysyms.d,       after = act.modes.delete)
        self.reg(self.nop, act.gtk.keysyms.r,       after = act.modes.replace)
        self.reg(self.nop, act.gtk.keysyms.y,       after = act.modes.yank)
        self.reg(self.nop, act.gtk.keysyms.i,       after = act.modes.insert)
        self.reg(self.nop, act.gtk.keysyms.v,       after = act.modes.visual)
        self.reg(self.nop, act.gtk.keysyms.g,       after = act.modes.g)
        self.reg(self.nop, act.gtk.keysyms.less,    after = act.modes.indent)
        self.reg(self.nop, act.gtk.keysyms.colon,   after = act.modes.ex)
        self.reg(self.nop, act.gtk.keysyms.greater, after = act.modes.indent)
        self.reg(self.nop, act.gtk.keysyms.B,       after = (act.modes.block, ["find", "number"]))
        self.reg(self.nop, act.gtk.keysyms.t,       after = (act.modes.t,     ["find", "number", "f"]))
        
        self.reg(act.lines.select_OneLine,      act.gtk.keysyms.V, after=act.modes.selection, final=True)
        self.reg(act.text.cut_UntilEndOfLine,   act.gtk.keysyms.D, after=act.modes.command,   final=True)
        self.reg(act.text.paste_ClipboardAbove, act.gtk.keysyms.P, after=act.modes.command,   pos=True, **self.fr)
        self.reg(act.text.paste_ClipboardBelow, act.gtk.keysyms.p, after=act.modes.command,   pos=True, **self.fr)

        self.reg(act.others.redo,               act.gtk.keysyms.r, True,                **self.fr)
        self.reg(act.others.undo,               act.gtk.keysyms.u,                      **self.fr)
        self.reg(act.text.delete_Char,          act.gtk.keysyms.x,                      **self.fr)
        self.reg(act.others.nextSearchItem,     act.gtk.keysyms.n,                      **self.fr)
        self.reg(act.text.delete_PrevChar,      act.gtk.keysyms.X,                      **self.fr)
        self.reg(act.text.delete_Char,          act.gtk.keysyms.Delete,                 **self.fr)
        self.reg(act.text.switchChar,			act.gtk.keysyms.S,						**self.fr)

        self.reg(act.pos.move_Forward,          act.gtk.keysyms.l,             **self.fr)
        self.reg(act.pos.move_Backward,         act.gtk.keysyms.h,             **self.fr)
        self.reg(act.pos.move_Down,             act.gtk.keysyms.j,             **self.fr)
        self.reg(act.pos.move_Up,               act.gtk.keysyms.k,             **self.fr)
        self.reg(act.pos.move_WordForward,      act.gtk.keysyms.w,             **self.fr)
        self.reg(act.pos.move_WordBackward,     act.gtk.keysyms.b,             **self.fr)
        self.reg(act.pos.move_BufferEnd,        act.gtk.keysyms.G,             **self.fr)        
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms._0,            **self.fr)
        self.reg(act.pos.move_LineEnd,          act.gtk.keysyms.dollar,        **self.fr)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.asciicircum,   **self.fr)
        self.reg(act.pos.toEmptyLine,           act.gtk.keysyms.E,             **self.fr)

        self.reg(act.pos.move_LineEnd,          act.gtk.keysyms.A, after=act.modes.insert,  **self.fr)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.I, after=act.modes.insert,  **self.fr)
        self.reg(act.insert.open_LineBelow,     act.gtk.keysyms.o, after=act.modes.insert,  **self.fr)
        self.reg(act.insert.open_LineAbove,     act.gtk.keysyms.O, after=act.modes.insert,  **self.fr)
        self.reg(act.insert.append_After,       act.gtk.keysyms.a, after=act.modes.insert,  **self.fr)
        self.reg(act.text.delete_Char,          act.gtk.keysyms.s, after=act.modes.insert,  **self.fr)
        
        self.reg(act.others.search,             act.gtk.keysyms.slash, final=True)

    def intro(self, act, options=None):
        act.vibase.stack = []
        act.vibase.setOverwrite(True)
        act.vibase.view.emit("select-all", False)
        act.vibase.resetNumber()
        act.vibase.select = False
    
    def handle(self, act, event):
        """ if a modifier is pressed, let it pass through so it can be registered by gedit 
        (so you can still use ordinary shortcuts in command mode"""
        return not act.keyboard.isModifierPressed(act, event)
    
    
    
