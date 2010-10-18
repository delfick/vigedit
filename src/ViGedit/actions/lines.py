import re

########################
###
###   SELECT WHOLE
###
########################

def select_Line(act):
    select_OneLine(act)

def select_Lines(act, number):
    if act.mode == act.modes.command:
        act.bindings.mode = act.modes.visual
    if number > 1:
        select_ManyLines(act, number)
    else:
        select_OneLine(act)
        
def select_OneLine(act):
    
    if act.mode == act.modes.visual:
        act.bindings.mode = act.modes.command
        
    act.pos.move_LineBegin(act)   
    
    cursor = act.pos.getIter(act)
    l1 = cursor.get_line()
    cursor.forward_line()
    if cursor.get_line() != l1:
        cursor.backward_char()
    
    act.pos.moveInsert(act, cursor, True)
        
def select_ManyLines(act, number):

    if act.mode == act.modes.visual:
        act.bindings.mode = act.modes.command
        
    if type(number) in (list, tuple):
        try:
            number = int("".join(number))
        except ValueError:
            number = 0
    
    act.pos.move_LineBegin(act)
    cursor = act.pos.getIter(act)
    l1 = cursor.get_line()
    cursor.forward_lines(number)
    l2 = cursor.get_line()
    if abs(l1 - l2) == number:
        cursor.backward_char()
        
    act.pos.moveInsert(act, cursor, True)
        
def getLinesTillEnd(act):
    """ determine how many lines from current position to the end of the file """
    cursor = act.pos.getIter(act)
    line = cursor.get_line()
    total = act.vibase.doc.get_line_count()
    act.trace.info(2, "lines till end of document : ", total-line)
    return total-line
    
########################
###
###   SELECT PART
###
########################

def select_ToLineEnd(act):
    act.bindings.mode = act.modes.visual
    act.pos.move_LineEnd(act)
    
def select_ToLineBegin(act):
    act.bindings.mode = act.modes.visual
    act.pos.move_LineBegin(act)
    
########################
###
###   OTHER
###
########################
    
def indentLeft(act):
    indent(act, "Left")

def indentRight(act):
    indent(act, "Right")

def manual_indent(act):
    pass

def indent(act, direction):
    numLines = act.vibase.numLines
    view = act.vibase.view
    buf = view.get_buffer()
    cursor = act.pos.getIter(act)
    select_Lines(act, numLines)
        
    if act.menus["indent%s" % direction] is not None:
        act.menus["indent%s" % direction].activate()
    else:
        if view.get_insert_spaces_instead_of_tabs():
            text = view.get_tab_width() * ' '
        else:
            text = '\t'
        
        cursor.set_line_offset(0)

        if direction is 'Right':
            buf.insert(cursor, text)
        else:
            end = cursor.copy()
            end.set_line_offset(len(text))
            #check that we are not deleting into line contents
            #(can happen when the indent width is larger than
            #current white space before line)
            while not re.match('^[\t ]+$', buf.get_text(cursor, end)):
                end.backward_cursor_position()

            if cursor.get_char() in ['\t', ' ']:
                buf.delete(cursor, end)

        #move to end of indentation
        cursor.forward_sentence_end()
        cursor.backward_sentence_start()

    act.pos.moveInsert(act, cursor)
    
