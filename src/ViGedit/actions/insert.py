import actions_base as base
import position as pos

def append_after():
    iter = pos.get_cursor_iter()
    if iter.ends_line():
        print "insert ' '"
        base.get_element("doc").insert_at_cursor(" ")
    else:
        print "move forward cursor position" 
        base.get_element("view").emit("move-cursor", gtk.MOVEMENT_VISUAL_POSITIONS, 1, base.get_element("select"))
        #iter.forward_cursor_position() 
    base.select_mode("insert")
    return True
    
def insert_after():
    pos.move_forward()
    base.select_mode("insert")
    
def insert_end_line():
    pos.move_line_end()
    base.select_mode("insert")
    
def insert_begin_line():
    cursor = pos.get_cursor_iter()
    cursor.backward_sentence_start()
    base.get_element("doc").place_cursor(cursor)
    base.select_mode("insert")
    
    
def open_line_above():
    print "Opening line above in %s" % base.get_element("view")
    pos.move_line_begin()
    base.select_mode("insert")
    base.get_element("view").emit("insert-at-cursor", "\n")
    self.move_up()

def open_line_below():
    print "Opening line below in %s" % base.get_element("view")
    pos.move_line_end()
    base.select_mode("insert")
    base.get_element("view").emit("insert-at-cursor", "\n")
