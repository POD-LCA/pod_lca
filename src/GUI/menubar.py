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

        menu_file.add_command(label='New', command=lambda :self._newFile(menubar))
        menu_file.add_command(label='Open', command=self._openFile)
        menu_file.add_separator()
        menu_file.add_command(label='Save', command=self._quicksaveFile)
        menu_file.add_command(label='Save As', command=self._saveFile)
        menu_file.add_separator()
        menu_file.add_command(label='Close', command=lambda : self._closeFile(menubar))

    def _newFile(self, menubar):

        cmd = self.clear_state
        self._savePrompt(menubar, cmd)

    
    def _closeFile(self, menubar):

        cmd = sys.exit
        self._savePrompt(menubar, cmd)

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
            self.save_file(file_path)
            self.save_path = file_path

    def _openFile(self):

        home_dir = os.path.expanduser("~")
        file_path = filedialog.askopenfilename(initialdir=home_dir, 
                                                title="Open file", 
                                                defaultextension=".pkl",
                                                filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*")))

        if file_path:
            self.clear_state()
            self.load_file(file_path)

    def _savePrompt(self, menubar, cmd):

        popup = Popup(menubar, "Save Prompt", "300x125")
        popup._popup_label("Do you want to save the current project? ", justify='left', font=("Arial", 10))

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="Yes", command=lambda: self._save_and_then(cmd))
        ok_button.pack(side=LEFT, padx=10)

        import_button = Button(button_frame, text="No", command=lambda: Menubar._notsave_and_then(cmd, popup))
        import_button.pack(side=LEFT, padx=10)

        close_button = Button(button_frame, text="Cancel", command=popup.destroy)
        close_button.pack(side=LEFT, padx=10)


    def _save_and_then(self, cmd):

        Menubar._quicksaveFile(self)
        cmd()

    @staticmethod
    def _notsave_and_then(cmd, popup):

        popup.destroy()
        cmd()


    # =================================
    # EDIT MENU
    # =================================

    def create_edit_menu(self, menubar):
        
        menu_edit = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_edit.add_command(label='Canvas Settings', command=lambda :self._update_setting(menubar))

    def _update_setting(self, menubar):

        popup = Popup(menubar, "Canvas Settings", "450x700")

        popup._popup_label("Colors ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        color_canvas = popup._popup_input_field("canvas color", default_val=self.color_canvas)
        color_product =  popup._popup_input_field("product color", default_val=self.color_product)
        color_process =  popup._popup_input_field("process color", default_val=self.color_process)
        color_transport = popup._popup_input_field("transportation process color", default_val=self.color_transport)
        color_energy = popup._popup_input_field("Energy product color", default_val=self.color_energy)
        color_emission = popup._popup_input_field("Emission product color", default_val=self.color_emission)
        color_waste = popup._popup_input_field("Waste product color", default_val=self.color_waste)
        
        popup._popup_label("Grid ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        canvas_grid = popup._popup_radio_buttons({'On': True, 'Off':False}, self.canvas_grid, 
                                                 cmd= lambda: Popup.update_entry_state(bool(int(canvas_grid.get())), grid_spacing))
        
        grid_spacing = popup._popup_input_field("grid spacing", default_val=self.canvas_grid_size, validate_num=True)

        popup._popup_label("Connectors ", justify='left', with_seperator=True, font=("Arial", 12, "bold"))
        color_connectors = popup._popup_input_field("connector color", default_val=self.connector_color)
        connector_type = popup._popup_radio_buttons({'straight':'straight',
                                                            'elbow': 'elbow',
                                                            'spline':'spline' }, self.connector_type,
                                                            cmd= lambda: Popup.update_entry_state(connector_type.get() != "straight", connector_offset))
        connector_offset = popup._popup_input_field("connector offset", default_val=self.connector_offset, validate_num=True)

        cmd = lambda: self._apply_settings(color_canvas.get(), color_connectors.get(),
                                            tag_colors = {"product": color_product.get(), 
                                                          "process": color_process.get(), 
                                                          "transportation": color_transport.get(),
                                                          "energy": color_energy.get(),
                                                          "emission": color_emission.get(),
                                                          "waste": color_waste.get()}                                                    , 
                                            canvas_grid=canvas_grid.get(),
                                            connector_type=connector_type.get(),
                                            grid_spacing=grid_spacing.get(),
                                            connector_offset=connector_offset.get())

        popup.button_pack_OKCancelApply(cmd)

    def _apply_settings(self, color_canvas, color_connectors, tag_colors, canvas_grid, connector_type, grid_spacing, connector_offset):

        self.color_canvas = color_canvas
        self.color_connectors = color_connectors
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
        self.color_energy = tag_colors["energy"]
        self.color_emission = tag_colors["emission"]
        self.color_waste = tag_colors["waste"]

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

        menu_database.add_command(label='Import', command=lambda :self.import_database(self))

    def import_database(self, menubar):

        popup = Popup(menubar, "Import database", "450x100")
        file_path =  popup._popup_input_field("File name: ") 

        browse_button  = Button(popup, text ="Select File", command=lambda: menubar._file_open_dialog(menubar, file_path, popup))
        browse_button.place(x=250,y=0)

        cmd = lambda: GUIInputManager.import_data_from_CSV(file_path.get(), self.project)
        popup.button_pack_OKCancelApply(cmd)


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
