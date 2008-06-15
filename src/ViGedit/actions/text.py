import actions_base as base
import position as pos
import insert
import lines
import gtk

def delete_char():
    # TODO This doesn't quite work right.
    iter = pos.get_cursor_iter() 
    if iter.ends_line():
        print "deleting last char"
        base.get_element("doc").delete(iter, base.get_element("doc").get_iter_at_offset(iter.get_offset() + 1))
    else:
        print "regular delete char"
        base.get_element("view").emit("delete-from-cursor", gtk.DELETE_CHARS, 1)
    pos.get_cursor_iter().backward_cursor_position()
    
def paste_clipboard_above():
    base.get_element("view").paste_clipboard()
    base.select_mode("command")

def paste_clipboard_below():
    insert.open_line_below()
    base.get_element("view").paste_clipboard()
    base.select_mode("command")
    
def yank_selection():
    base.get_element("view").copy_clipboard()
    base.select_mode("command")
    
def cut_selection():
    print "cut selection"
    base.get_element("view").cut_clipboard()
    base.select_mode("command")    
    
def cut_until_end_of_line():
    base.select_mode("visual")
    pos.move_line_end()
    cut_selection()
    
def cut_line():
    select_line()
    cut_selection()
    
def yank_line():
    number = base.get_element("number")
    lines.select_lines(number)
    yank_selection()
    lines.return_to_origin(number)

def cut_next_word():
    base.select_mode("visual")
    pos.move_word_forward()
    cut_selection()

def delete_whole_line():
    print "delete whole line function is called"
    lines.select_line() 
    cut_selection()
