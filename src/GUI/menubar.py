from material.databaseManager.databaseManager import DatabaseManager
from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup

import os
import sys
from tkinter import Button, Menu, filedialog, END, LEFT, Frame

class Menubar:
    
    # =================================
    # FILE MENU
    # =================================

    def create_file_menu(self, menubar):

        menu_file = Menu(self, tearoff=False)
        menubar.add_cascade(menu=menu_file, label='File')

        menu_file.add_command(label='New', command=self._newFile)
        menu_file.add_command(label='Open', command=self._openFile)
        menu_file.add_separator()
        menu_file.add_command(label='Save', command=self._quicksaveFile)
        menu_file.add_command(label='Save As', command=self._saveFile)
        menu_file.add_separator()
        menu_file.add_command(label='Close', command=self._closeFile)

    def _newFile(self):

        # TODO: Add warning and ask to save
        self.clear_state()
    
    def _closeFile(self):

        sys.exit()

    def _quicksaveFile(self):

        if self.save_path is None:
            self._saveFile()
        else:
            self.save_state(self.save_path)

    def _saveFile(self):

        home_dir = os.path.expanduser("~")
        file_path = filedialog.asksaveasfilename(initialdir=home_dir, 
                                                    title="Save As", 
                                                    defaultextension=".pkl",
                                                    filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*")))

        if file_path:
            self.save_state(file_path)
            self.save_path = file_path

    def _openFile(self):

        home_dir = os.path.expanduser("~")
        file_path = filedialog.askopenfilename(initialdir=home_dir, 
                                                title="Open file", 
                                                defaultextension=".pkl",
                                                filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*")))

        if file_path:
            self.clear_state()
            self.load_state(file_path)

    # =================================
    # EDIT MENU
    # =================================

    def create_edit_menu(self, menubar):
        
        menu_edit = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_edit.add_command(label='Canvas Settings', command=lambda :self._update_setting(menubar))

    def _update_setting(self, menubar):

        popup = Popup(menubar, "Canvas Settings", "450x575")

        popup._popup_label("Colors ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        color_canvas = popup._popup_input_field("canvas color", default_val=self.color_canvas)
        color_product =  popup._popup_input_field("product color", default_val=self.color_product)
        color_process =  popup._popup_input_field("process color", default_val=self.color_process)
        color_transport = popup._popup_input_field("transportation process color", default_val=self.color_transport)
        
        popup._popup_label("Grid ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        canvas_grid = popup._popup_radio_buttons({'On': True, 'Off':False}, self.canvas_grid, 
                                                 cmd= lambda: Popup.update_entry_state(bool(int(canvas_grid.get())), grid_spacing))
        
        grid_spacing = popup._popup_input_field("grid spacing", default_val=self.canvas_grid_size, validate_num=True)

        popup._popup_label("Connectors ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        connector_type = popup._popup_radio_buttons({'straight':'straight',
                                                            'elbow': 'elbow',
                                                            'spline':'spline' }, self.connector_type,
                                                            cmd= lambda: Popup.update_entry_state(connector_type.get() != "straight", connector_offset))
        connector_offset = popup._popup_input_field("connector offset", default_val=self.connector_offset, validate_num=True)

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        cmd = lambda: self._apply_settings( color_canvas.get(), 
                                            tag_colors = {"product":color_product.get(), 
                                                          "process":color_process.get(), 
                                                          "transportation":color_transport.get()}, 
                                            canvas_grid=canvas_grid.get(),
                                            connector_type=connector_type.get(),
                                            grid_spacing=grid_spacing.get(),
                                            connector_offset=connector_offset.get())

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        close_button = Button(button_frame, text="Close", command=popup.destroy)
        close_button.pack(side=LEFT, padx=10)

        import_button = Button(button_frame, text="Apply", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
        import_button.pack(side=LEFT, padx=10)

    def _apply_settings(self, color_canvas, tag_colors, canvas_grid, connector_type, grid_spacing, connector_offset):

        self.color_canvas = color_canvas
        self.canvas.config(bg=color_canvas)
        
        self.canvas_grid_size = float(grid_spacing)
        self.canvas_grid = bool(int(canvas_grid))
        if self.canvas_grid:
            self.draw_grid()
        else:
            self.canvas.delete("grid")

        self.connector_type = connector_type
        self.connector_offset = float(connector_offset)
        self.redraw_connections()

        self.color_product = tag_colors["product"]
        self.color_process = tag_colors["process"]
        self.color_transport = tag_colors["transportation"]

        for tag in ["process", "product"]:
            items_with_tag = self.canvas.find_withtag(tag)
            for item_id in items_with_tag:
                self.canvas.itemconfig(item_id, fill=tag_colors[tag])

        for tag in ["transportation"]:
            items_with_tag = self.canvas.find_withtag(tag)
            for item_id in items_with_tag:
                self.canvas.itemconfig(item_id, fill=tag_colors[tag])
    
    # =================================
    # DATABSE MENU
    # =================================

    def create_database_menu(self, menubar):

        menu_database = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_database, label='Database')

        menu_database.add_command(label='Import', command=lambda :self.import_database(menubar))

    def import_database(self, menubar):

        popup = Popup(menubar, "Import database", "450x100")
        file_path =  popup._popup_input_field("File name: ") 

        browse_button  = Button(popup, text ="Select File", command=lambda: menubar._file_open_dialog(menubar, file_path, popup))
        browse_button.place(x=250,y=0)

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        cmd = lambda: GUIInputManager.import_data_from_CSV(file_path, self.project)

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

    # =================================
    # HELP MENU
    # =================================

    def create_help_menu(self, menubar):
        
        menu_help = Menu(self, tearoff=False)
        menubar.add_cascade(menu=menu_help, label='Help')

        menu_help.add_command(label='Quick Start Guide', command=self._quick_start)
        menu_help.add_separator()
        menu_help.add_command(label='About', command=self._about)

    def _about(self):

        pass

    def _quick_start(self):

        pass
