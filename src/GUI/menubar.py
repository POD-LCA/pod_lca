from material.databaseManager.databaseManager import DatabaseManager
from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup

from tkinter import Button, Menu, filedialog, END, LEFT, Frame

class Menubar:
    
    # =================================
    # FILE MENU
    # =================================

    def create_file_menu(self, menubar):

        menu_file = Menu(self, tearoff=False)
        menubar.add_cascade(menu=menu_file, label='File')

        menu_file.add_command(label='New', command=self._newFile)
        menu_file.add_command(label='Open...', command=self._openFile)
        menu_file.add_command(label='Close', command=self._closeFile(self))

    def _newFile(self):

        pass
    
    def _openFile(self):

        pass

    def _closeFile(self, app):

        app.quit

    # =================================
    # EDIT MENU
    # =================================

    def create_edit_menu(self, menubar):
        
        menu_edit = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_edit, label='Edit')

    # =================================
    # DATABSE MENU
    # =================================

    def create_database_menu(self, menubar):

        menu_database = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_database, label='Database')

        menu_database.add_command(label='Import', command=lambda :self.import_database(self, "Import database", "500x200"))

    def import_database(self, menubar, title, shape):

        popup = Popup(menubar, "Import database", "450x100")
        file_path =  popup._popup_input_field("File name: ") 

        browse_button  = Button(popup, text ="Select File", command=lambda: menubar._file_open_dialog(menubar, file_path, popup))
        browse_button.place(x=250,y=0)

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        cmd = lambda: GUIInputManager.import_data_from_JSON(file_path.get(), self.project)

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        close_button = Button(button_frame, text="Close", command=popup.destroy)
        close_button.pack(side=LEFT, padx=10)

        import_button = Button(button_frame, text="Import", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
        import_button.pack(side=LEFT, padx=10)


    def _file_open_dialog(self, menubar, file_path, popup):

        ftypes = [('CSV', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(menubar, filetypes=ftypes)
        file_path_selected = dlg.show()

        if file_path_selected:
            file_path.delete(0, END)
            file_path.insert(0, file_path_selected)

        popup.lift()
        popup.focus_force()
