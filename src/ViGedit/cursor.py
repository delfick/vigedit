# -*- coding: utf-8 -*-

#  cursor.py - processing for the cursor
#  
#  Copyright (C) 2008 - Joseph Method
#  Copyright (C) 2008, 2009 - Stephen Moore
#  Copyright (C) 2006 - Trond Danielsen
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

class VIG_Cursor(object):
    """functions to control the cursor with"""     
        
    def getIter(self, act):
        return act.vibase.doc.get_iter_at_mark(act.vibase.doc.get_insert())
        
    def moveInsert(self, act, newIter, select=False):
        mark = act.vibase.doc.get_insert()
        
        if select:
            act.vibase.doc.move_mark(mark, newIter)
        else:
            act.vibase.doc.place_cursor(newIter)
         
        act.vibase.view.scroll_to_mark(mark, 0.0)
        
    def goToLine(self, act, line):
        cursor = self.getIter(act)
        cursor.set_line(line - 1)
        self.moveInsert(act, cursor)
    
    def move(self, act, directionType, num):
        act.vibase.view.emit("move-cursor", directionType, num, act.vibase.select)
        
    def toEmptyLine(self, act, forward = True):
        act.pos.move_LineBegin(act)
        cursor = self.getIter(act)
        if forward:
            direction = "forward"
        else:
            direction = "backward"
            
        while True:
            getattr(cursor, "%s_visible_line" % direction)()
            print "line %d : %d chars, start: %s, end : %s" % (cursor.get_line(), cursor.get_chars_in_line(), cursor.ends_line(), cursor.starts_line())
            if cursor.get_chars_in_line() == 1:
                if cursor.ends_line() and cursor.starts_line():
                    self.moveInsert(act, cursor)
                    break
            
            if cursor.is_start() or cursor.is_end():
                act.trace.info(2, "reached boundary of document")
                break
    
########################
###
###   MOVING
###
########################

    ########################
    ###   DIRECTION
    ########################
    
    def move_Up(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, -num)
        
    def move_Down(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, num)
        
    def move_Forward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_VISUAL_POSITIONS, num)
        
    def move_Backward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_VISUAL_POSITIONS, -num)
       
    ########################
    ###   PAGE
    ######################## 
        
    def move_PageUp(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PAGES, -num)
        
    def move_PageDown(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PAGES, num)
        
    ########################
    ###   WORD
    ########################
        
    def move_WordForward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_WORDS, num)
       
    def move_WordBackward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_WORDS, -num)
    
    ########################
    ###   BUFFER
    ########################
        
    def move_BufferTop(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_BUFFER_ENDS, -num)
        
    def move_BufferEnd(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_BUFFER_ENDS, num)
    
    ########################
    ###   LINE
    ########################
        
    def move_LineEnd(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, num)
        
    def move_LineBegin(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, -num)
        
instance = VIG_Cursor()  
        
