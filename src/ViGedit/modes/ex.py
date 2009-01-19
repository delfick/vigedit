import os
import sys
from binding_base import *
import glob

class ex_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(self.evaluate_ex, gtk.keysyms.Return, True)
        self.register(self.evaluate_ex, gtk.keysyms.KP_Enter, True)
        self.register(self.cycle_completions, gtk.keysyms.Tab, False)
        self.register(self.cycle_completions, gtk.keysyms.Up, False)
        self.register(self.cycle_completions_down, gtk.keysyms.Down, False)

    def parse_ls(self, part):
        query = "%s*" % part
        listed_files = glob.glob(query)
        keep_files = []
        for file in listed_files:
            if file == "":
                continue
            if os.path.isdir(file):
                file = file + "/"
                keep_files.append(file)
            else:
                keep_files.append(file)
        return keep_files

    def complete_file_operation(self, command):
        tab_options = []
        pieces = command.split()
        command = pieces[0]
        if len(pieces) == 2:
            argument = pieces[1]
        else:
            argument = ""
        listed_files = self.parse_ls(argument) 
        matching_files = []
        for file in listed_files:
            if re.compile(r"^%s" % argument).match(file):
                matching_files.append(file)
        for match in matching_files:
            full_command = command + " " + match
            tab_options.append([full_command, False])
        return tab_options

    def ex_action_completions(self):
        return [["tabnew", True], ["e", True], ["sp", True], ["vsplit", True]]

    def cycle_completions_down(self):
        self.cycle_completions(False)

    def get_ex_commands_history(self):
        tab_options = []
        for command in base.vigtk.ex_commands_history:
            tab_options.append([command, False])
        if len(tab_options) != 0:
            tab_options[0][1] = True
        return tab_options

    def cycle_completions(self, up = True): 
        # Wow, vim completion is tricky if you think about it
        print os.getcwd()
        command = "".join(base.vigtk.acc)
        tab_options = []
        
        if command != "":
            pieces = command.split()
            if len(pieces) == 1:
                tab_options = self.ex_action_completions()
            elif len(pieces) == 2:
                if pieces[0] in ["tabnew", "e", "sp", "vsplit", "!ls", "!cat", "!mv", "!cp"]:
                    tab_options = self.complete_file_operation(command)
        else:
            tab_options = self.get_ex_commands_history()

        if base.vigtk.tabbing_through_entries != True:
            # We start with the first tab match
            base.vigtk.tab_press_items = tab_options 
            if len(base.vigtk.tab_press_items) != 0:
                base.vigtk.tab_press_items[0][1] = True
            base.vigtk.tabbing_through_entries = True
            print "tab_options now are: %s" % base.vigtk.tab_press_items
        
        tab_press = 0
        tab_press_items = base.vigtk.tab_press_items
        for tab_press_item in tab_press_items:
            print tab_press_item
            if tab_press_item[1] == True:
                print "current tab_press_item is: %s" % tab_press_item[0]
                # We're pushing the tab along
                base.vigtk.tab_press_items[tab_press][1] = False
                # This should be popping and pushing, but my python's rusty

                #TODO needs the up/down logic here
                if tab_press != len(tab_press_items) - 1:
                    base.vigtk.tab_press_items[tab_press + 1][1] = True 
                else:
                    base.vigtk.tab_press_items[0][1] = True 

                new_acc = []
                full_command = tab_press_item[0]
                for i in range(0, len(full_command)):
                    new_acc.append(full_command[i])
                base.vigtk.acc = new_acc 
                others.update_ex_bar()
                break
            tab_press += 1
        return False

    def handle_mode(self, event):
        print "ex mode: %s - %s" % (event.keyval, event.keyval == gtk.keysyms.Right)
        if event.keyval == gtk.keysyms.BackSpace:
            if base.vigtk.acc:
                base.vigtk.acc.pop()
                others.update_ex_bar()
        if event.keyval == gtk.keysyms.Escape:
            vibase.set_mode("command")
        elif (event.keyval != gtk.keysyms.Return) and (event.keyval != gtk.keysyms.BackSpace):
            vibase.increment_accumulator(event)
            others.update_ex_bar()
        base.vigtk.tabbing_through_entries = False 
        return True
        
    def evaluate_ex(self):
        others.evaluate_ex(base.vigtk.acc)
        if base.vigtk.window.get_views != []:
            vibase.set_mode("command")       
       
        
    def select_mode(self, option=None):
        base.vigtk.acc = []
        base.vigtk.view.emit("select-all", False)
        base.vigtk.select = False
        
