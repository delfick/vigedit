""" object holding reference to particular menu items
there is only ever one instance of this 
that instance can be referenced through vibase.get_menu or vibase.activate_menu"""

class Menus(object):

    def __init__(self, window):
        self.window = window    
        self.ui_manager = self.window.get_ui_manager()
        # print self.ui_manager.get_ui()
        self.menubar = self.window.get_children()[0].get_children()[0]
        self.save_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveMenu")
        self.save_as_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveAsMenu")
        self.search_next_menu = self.ui_manager.get_action("/MenuBar/SearchMenu/SearchFindNextMenu")
        self.quit_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileQuitMenu")
        self.file_close_menu = self.ui_manager.get_action("/MenuBar/FileMenu/FileCloseMenu")
        self.indent_right_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Indent")
        self.indent_left_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Unindent")
        self.split_lines_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/SplitLines")
        self.join_lines_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/JoinLines")
        self.select_all_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditSelectAllMenu")
        self.paste_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditPasteMenu")
        self.cut_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditCutMenu")
        self.copy_menu = self.ui_manager.get_action("/MenuBar/EditMenu/EditCopyMenu")
        
    def get_menu(self, menuType):
        """ returns a reference to the specified menu """
        the_menu = getattr(self, "%s_menu" % menuType, None)
        if the_menu is None: return
        return the_menu
        
    def activate_menu(self, menuType):
        """ activates the specified menu """
        the_menu = getattr(self, "%s_menu" % menuType, None)
        if the_menu is None: return
        the_menu.activate()
        
    
