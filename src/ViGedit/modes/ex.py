import os
import sys
from binding_base import *
class ex_Mode(binding_base):

    def __init__(self):
        binding_base.__init__(self)

    def init_bindings(self):
        self.register(self.evaluate_ex, gtk.keysyms.Return, True)
        self.register(self.evaluate_ex, gtk.keysyms.KP_Enter, True)
        self.register(self.cycle_completions, gtk.keysyms.Tab, False)
        self.register(self.handle_right_button, gtk.keysyms.Right, False)

    def handle_right_button(self):
        print "handle_right_button"
        base.vigtk.tabbing_through_entries = False 

    def parse_ls(self, part):
        # I'm sure this isn't how you do it
        ls_readout = os.popen(r"ls -a1 %s*" % re.escape(part)).read()
        listed_files = ls_readout.split("\n")
        start_of_dirs = False
        keep_files = []
        for file in listed_files:
            if file == "":
                continue
            if file.find(":") != -1:
                file = file.replace(":", "/")
                keep_files.append(file)
                start_of_dirs = True
            elif start_of_dirs == False:
                keep_files.append(file)
            elif start_of_dirs == True:
                pass

        return keep_files


    def cycle_completions(self): 
        # Wow, vim completion is tricky if you think about it
        command = "".join(base.vigtk.acc)
        tab_options = []
        if re.compile(r"tabnew (.+)$").match(command):
            part = re.compile(r"tabnew (.+)$").match(command).group(1)
            listed_files = self.parse_ls(part) 
            matching_files = []
            for file in listed_files:
                if re.compile(r"^%s" % re.escape(part)).match(file):
                    matching_files.append(file)

            print "matching_files: %s" % matching_files

            for match in matching_files:
                full_command = "tabnew " + match
                tab_options.append([full_command, False])

        print "tab_options were: %s" % base.vigtk.tab_press_items

        if base.vigtk.tabbing_through_entries != True:
            print "resetting last_tabbed_entry"
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
                # This should be popping and pushing
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


    def handle_mode(self, event):
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
        
        
        
        
        
