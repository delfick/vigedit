import actions_base as base
import gtk

def get_cursor_iter():
    return base.doc().get_iter_at_mark(base.doc().get_mark('insert'))   
    
def go_to_line(line):
    cursor = get_cursor_iter(doc)
    cursor.set_line(line - 1)
    base.doc().place_cursor(cursor)
    base.view().scroll_to_mark(doc.get_mark('insert'))
    
def to_empty_line(forward = True):
    cursor = get_cursor_iter(base.doc())
    while True:
        if forward:
            cursor.forward_line()
        else:
            cursor.backward_line()

        print "=======forward(%s)====%s" % (forward, cursor.get_line() + 1)

        while True:
            print cursor.get_line_offset()
            if cursor.starts_line():
                break
            cursor.backward_char()

        end_cursor = cursor.copy()
        if not end_cursor.ends_line():
            end_cursor.forward_to_line_end()
        text = cursor.get_text(end_cursor)
        print text.__repr__()
        print "Is space: %s" % text.isspace()
        print "========================="
        if text.isspace() or (len(text) == 0):
            print "text is space"
            return cursor
        elif cursor.is_start():
            return cursor
        elif end_cursor.is_end():
            return end_cursor
            
def move_forward():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, base.select())
    
def move_up():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, -1, base.select())
    
def move_down():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_DISPLAY_LINES, 1, base.select())
    
def move_backward():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, -1, base.select())
    
def move_word_forward():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_WORDS, 1, base.select())
   
def move_word_backward():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_WORDS, -1, base.select())
    
def move_buffer_top():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, -1, base.select())
    
def move_buffer_end():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_BUFFER_ENDS, 1, base.select())
    
def move_line_end():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, 1, base.select())
    
def move_line_begin():
    base.get_element("view").emit("move-cursor", gtk.MOVEMENT_PARAGRAPH_ENDS, -1, base.select())
   
    
    
    
    
