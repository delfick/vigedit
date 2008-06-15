import position as pos
import actions_base as base
import menus

def select_lines(number):
    print "selecting %d lines" % (number+1)
    pos.move_line_begin()
    base.select_mode("visual")
    pos.move_line_end()
    pos.move_forward()
    #select the number of lines specified
    while number > 0:
        pos.move_down()
        number = number-1 

def return_to_origin(number):
    number = int(number) + 1
    while number > 0:
        self.move_up()
        number = int(number) - 1
    pos.move_line_begin()
    self.command_mode()

    
def select_line():
    pos.move_line_begin()
    base.select_mode("visual")
    pos.move_line_end()
    pos.move_forward() # Select \n too.

def split_lines():
    if menus.get_menu("split_lines") == None:
        return False
    begin = pos.to_empty_line(False)
    end = pos.to_empty_line(True)
    print begin, end
    if (begin != None) and (end != None):
        base.doc().select_range(begin, end)
        print "activate split_lines_menu"
        menus.get_menu("split_lines").activate()
    base.select_mode("command")
    
def indent_left():
    number = base.get_element("number")
    select_lines(number)
    if menus.get_menu("indent_left") is not None:
        menus.get_menu("indent_left").activate()
    return_to_origin(number)

def indent_right():
    number = base.get_element("number")
    select_lines(number)
    if menus.get_menu("indent_right") is not None:
        menus.get_menu("indent_right").activate()
    return_to_origin(number)
