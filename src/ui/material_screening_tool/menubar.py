from ui.material_screening_tool.GUI_inputManager import GUIInputManager
from ui.material_screening_tool.GUI_outputManager import GUIOutputManager
from ui.material_screening_tool.popup import Popup
from ui.material_screening_tool.cell_table import CellTable

import os
import sys
from tkinter import Button, Menu, filedialog, END, LEFT, TOP, RIGHT, BOTH, W, Frame, Label, Entry, BooleanVar, StringVar, Canvas
from tkinter.ttk import Notebook, Combobox, Scrollbar, Style

class MenubarMixin:
    
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
            self.save_file(self.save_path)

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
        Popup._popup_label(popup,"Do you want to save the current project? ", justify='left')

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="Yes", command=lambda: self._save_and_then(cmd))
        ok_button.pack(side=LEFT, padx=10)

        import_button = Button(button_frame, text="No", command=lambda: MenubarMixin._notsave_and_then(cmd, popup))
        import_button.pack(side=LEFT, padx=10)

        close_button = Button(button_frame, text="Cancel", command=popup.on_popup_close)
        close_button.pack(side=LEFT, padx=10)


    def _save_and_then(self, cmd):

        MenubarMixin._quicksaveFile(self)
        cmd()

    @staticmethod
    def _notsave_and_then(cmd, popup):

        popup.on_popup_close()
        cmd()

    # =================================
    # EDIT MENU
    # =================================

    def create_edit_menu(self, menubar):
        
        menu_edit = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_edit.add_command(label='Canvas Settings', command=lambda :self._update_setting(menubar))

    def _update_setting(self, menubar):

        popup = Popup(menubar, "Canvas Settings", "375x350")

        notebook = Notebook(popup)

        color_tab,  grid_tab, connector_tab= Frame(notebook), Frame(notebook), Frame(notebook)

        notebook.add(color_tab, text="Colors")
        notebook.add(grid_tab, text="Canvas grid")
        notebook.add(connector_tab, text="Connectors")

        notebook.pack(expand=True, fill='both')

        color_tab_frame = Frame(color_tab)
        color_tab_frame.pack(pady=5, padx=10, anchor="w")
            
        color_canvas = Popup._popup_input_field(color_tab_frame, "Canvas color", default_val=self.color_canvas)
        color_product =  Popup._popup_input_field(color_tab_frame, "Product color", default_val=self.color_product)
        color_process =  Popup._popup_input_field(color_tab_frame, "Process color", default_val=self.color_process)
        color_transport = Popup._popup_input_field(color_tab_frame, "Transportation process color", default_val=self.color_transport)
        color_energy = Popup._popup_input_field(color_tab_frame, "Energy product color", default_val=self.color_energy)
        color_emission = Popup._popup_input_field(color_tab_frame, "Emission product color", default_val=self.color_emission)
        color_waste = Popup._popup_input_field(color_tab_frame, "Waste product color", default_val=self.color_waste)
        cmd_color = lambda: self._apply_settings_colors(color_canvas.get(), color_connectors.get(),
                                                        tag_colors = {"product": color_product.get(), 
                                                                    "process": color_process.get(), 
                                                                    "transportation": color_transport.get(),
                                                                    "energy": color_energy.get(),
                                                                    "emission": color_emission.get(),
                                                                    "waste": color_waste.get()})
        Popup.button_pack_OKCancelApply(color_tab_frame, popup, cmd_color)

        grid_tab_frame = Frame(grid_tab)
        grid_tab_frame.pack(pady=5, padx=10, anchor="w")
        Popup._popup_label(grid_tab_frame, "Grid:", justify='left')
        canvas_grid = Popup._popup_radio_buttons(grid_tab_frame, {'On': True, 'Off':False}, self.canvas_grid, 
                                                 cmd= lambda: Popup.update_entry_state(bool(int(canvas_grid.get())), grid_spacing))
        grid_spacing = Popup._popup_input_field(grid_tab_frame, "Grid spacing", default_val=self.canvas_grid_size, validate_num=True)
        cmd_grid = lambda: self._apply_settings_grid(canvas_grid.get(), grid_spacing.get())
        Popup.button_pack_OKCancelApply(grid_tab_frame, popup, cmd_grid)

        connector_tab_frame = Frame(connector_tab)
        connector_tab_frame.pack(pady=5, padx=10, anchor="w")
        color_connectors = Popup._popup_input_field(connector_tab_frame, "Connector color", default_val=self.connector_color)
        Popup._popup_label(connector_tab_frame, "Connector type:", justify='left')
        connector_type = Popup._popup_radio_buttons(connector_tab_frame, {'straight':'straight',
                                                            'elbow': 'elbow',
                                                            'spline':'spline' }, self.connector_type,
                                                            cmd= lambda: Popup.update_entry_state(connector_type.get() != "straight", connector_offset))
        connector_offset = Popup._popup_input_field(connector_tab_frame, "Connector offset", default_val=self.connector_offset, validate_num=True)
        cmd_connectors = lambda: self._apply_settings_connectors(color_connectors.get(), connector_type.get(), connector_offset.get())
        Popup.button_pack_OKCancelApply(connector_tab_frame, popup, cmd_connectors)
        
        

    def _apply_settings_colors(self, color_canvas, color_connectors, tag_colors):

        self.color_canvas = color_canvas
        self.color_connectors = color_connectors
        self.canvas.config(bg=color_canvas)

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

        return self

    def _apply_settings_grid(self, canvas_grid, grid_spacing):

        self.canvas_grid_size = float(grid_spacing)
        self.canvas_grid = bool(int(canvas_grid))
        if self.canvas_grid:
            self.draw_grid()
        else:
            self.canvas.delete("grid")
        
        return self

    def _apply_settings_connectors(self, color_connectors, connector_type, connector_offset):

        self.color_connectors = color_connectors
        self.connector_type = connector_type
        self.connector_offset = float(connector_offset)
        self.redraw_connections()

        return self
    
    # =================================
    # DATABSE MENU
    # =================================

    def create_database_menu(self, menubar):

        menu_database = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_database, label='Database')

        menu_database_import = Menu(menu_database, tearoff=False)
        menu_database.add_cascade(menu=menu_database_import, label='Import')
        menu_database_import.add_command(label='From CSV', command=lambda :self.import_database(self))
        menu_database.add_separator()
        menu_database.add_command(label='Add custom entry', command=lambda :self.add_custom_item(self))

    def import_database(self, menubar):

        popup = Popup(menubar, "Import database from CSV", "925x315")
        file_path =  Popup._popup_input_field(popup, "File name: ", width=130)
        file_flags = {} 
    
        browse_button  = Button(popup, text ="Select File", command=lambda: menubar._file_open_dialog(menubar, file_path, popup))
        browse_button.pack(padx=250, pady=0)

        label = Label(popup, text="Input file data structure:")
        label.pack(anchor=W, pady=10, padx=10)
        
        width = 12

        col_entry_frame = Frame(popup)
        col_entry_frame.pack(pady=10)

        label = Label(col_entry_frame, text="Headers:", width=width)
        label.pack(side=LEFT, padx=11)

        n = len(self.impact_categories) + 2
        headers = ['Flow', 'Unit'] + list(self.impact_categories.keys())
        header_list = []
        for i in range(n):
            data = Entry(col_entry_frame, relief="solid", width=width + 2, justify='center')
            data.insert(0, headers[i])
            data.pack(side=LEFT, padx=11)
            header_list.append(data)

        impact_label_frame = Frame(popup)
        impact_label_frame.pack(pady=0)

        label = Label(impact_label_frame, text="Category:", width=width)
        label.pack(side=LEFT, padx=11)

        for i in range(n):
            impact_label = Label(impact_label_frame, text=headers[i], relief="solid", borderwidth=1, width=width)
            impact_label.pack(side=LEFT, padx=11)

        unit_label_frame = Frame(popup)
        unit_label_frame.pack(pady=10)

        label = Label(unit_label_frame, text="Unit:", width=width)
        label.pack(side=LEFT, padx=11)

        impact_units = ['', ''] + list(self.impact_categories.values())
        for i in range(n):
            label = Label(unit_label_frame, text=impact_units[i], relief="solid", borderwidth=1,width=width)
            label.pack(side=LEFT, padx=11)

        col_multipier_frame = Frame(popup)
        col_multipier_frame.pack(pady=5)

        label = Label(col_multipier_frame, text="Multiplier:", width=width)
        label.pack(side=LEFT, padx=11)

        vcmd = (col_multipier_frame.register(Popup._validate_input_num), '%P')
        multiplier_list = []
        for i in range(n):
            if i < 2:
                label = Label(col_multipier_frame, text='', relief="solid", borderwidth=1,width=width)
                label.pack(side=LEFT, padx=11)
            else:
                data = Entry(col_multipier_frame, validate='key', validatecommand=vcmd, relief="solid", width=width + 2, justify='center')
                data.insert(0, 1.0)
                data.pack(side=LEFT, padx=11)
                multiplier_list.append(data)

        cmd = lambda: self._import_data(file_path.get(), header_list, multiplier_list, file_flags)
        Popup.button_pack_OKCancelApply(popup, popup, cmd)

    def _import_data(self, file_path, header_list, multiplier_list, file_flags):

        if file_path not in file_flags:
            headers = [entry.get() for entry in header_list]
            multipliers = [float(entry.get()) for entry in multiplier_list]
            
            GUIInputManager.set_database(file_path, self.project, headers, multipliers)
            file_flags[file_path] = True

            return self
        else:
            return None

    def add_custom_item(self, menubar):

        popup = Popup(menubar, "Add custom entry to database", "300x300")

        flow =  Popup._popup_input_field(popup, "Flow name: ", default_val="new Impact Item") 
        unit =  Popup._popup_input_combo(popup, "Unit flow: ", GUIInputManager.get_all_units_list(self.project), default_entry=0)

        impacts = []
        for impact in self.impact_categories:
            label_str = impact + ' (in ' + self.impact_categories[impact] + ')'
            impact_entry =  Popup._popup_input_field(popup, label_str, validate_num=True, default_val=0.0)
            impacts.append(impact_entry)

        cmd = lambda: self._add_database_entry(flow.get(), unit.get(), impacts)
        Popup.button_pack_OKCancel(popup, popup, cmd)

    def _add_database_entry(self, flow, unit, impacts):

        impact_vals = [float(impact.get()) for impact in impacts]
        impact_dict = {key: value for key, value in zip(self.impact_categories.keys(), impact_vals)}

        GUIInputManager.set_custom_entry(self.project, flow, unit, impact_dict)

        return self

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
    # ANALYSIS MENU
    # =================================

    def create_analysis_menu(self, menubar):

        menu_analysis= Menu(self, tearoff=False)
        menubar.add_cascade(menu=menu_analysis, label='Analysis')

        menu_hotspot = Menu(menu_analysis, tearoff=False)
        self.hotspot_on_off = BooleanVar(value=True)
        menu_hotspot.add_radiobutton(label="On", variable=self.hotspot_on_off, value=True, command=lambda: self.show_hotspots())
        menu_hotspot.add_radiobutton(label="Off", variable=self.hotspot_on_off, value=False, command=lambda: self.clear_hotspots())
        menu_hotspot.add_separator()
        self.hotspot_impact_cat = StringVar(value='GWP')
        menu_hotspot.add_radiobutton(label="GWP", variable=self.hotspot_impact_cat, value='GWP', command=lambda: self.show_hotspots())
        menu_hotspot.add_radiobutton(label="AP", variable=self.hotspot_impact_cat, value='AP', command=lambda: self.show_hotspots())
        menu_hotspot.add_radiobutton(label="EP", variable=self.hotspot_impact_cat, value='EP', command=lambda: self.show_hotspots())
        menu_hotspot.add_radiobutton(label="ODP", variable=self.hotspot_impact_cat, value='ODP', command=lambda: self.show_hotspots())
        menu_hotspot.add_radiobutton(label="SFP", variable=self.hotspot_impact_cat, value='SFP', command=lambda: self.show_hotspots())
        menu_analysis.add_cascade(menu=menu_hotspot, label='Hotspot Analysis')
        menu_analysis.add_command(label='Data Quality Assessment (DQA)', command=lambda: self.open_DQA_view(menubar))
        menu_analysis.add_command(label='Sensitivity Analysis (SA)', command='')
        menu_analysis.add_separator()
        menu_analysis.add_command(label='Monte Carlo Simulation (MCS)', command='')
        menu_analysis.add_command(label='Scenario Aware Monte Carlo Simulation (SA-MCS)', command='')

    def open_DQA_view(self, menubar):

        popup = Popup(menubar, "Data Quality Assessment", "1100x500")

        # set scroll bar
        container = Frame(popup)
        container.pack(fill="both", expand=True)

        canvas = Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))

        # model picker
        dropdown_frame = Frame(content_frame)
        dropdown_frame.pack(pady=10)
        
        label = Label(dropdown_frame, bg=self.plotter_bg_color, fg='white', text="Model", font = ('Helvetica', 12,'bold'))
        label.pack(side=LEFT, padx=(0, 10))
        
        model_dropdown = Combobox(dropdown_frame, values=list(GUIInputManager.get_all_model_names(self.project)))
        model_dropdown.pack(side=RIGHT, fill=BOTH, pady=10)
        model_dropdown.current(0)
        model_dropdown.bind("<<ComboboxSelected>>", lambda x:self.create_score_panel(score_panel_frame, x.widget.get()))

        # create score panel
        score_panel_frame = Frame(content_frame)
        score_panel_frame.pack(pady=10)
        self.create_score_panel(score_panel_frame, model_dropdown.get())

        # close button
        Popup.button_pack_Close(content_frame, popup)
    
    def create_score_panel(self, frame, model_name):

        # destroy the previous score panel
        for widget in frame.winfo_children():
            widget.destroy()
        
        GUIInputManager.create_DQA(self.project)

        model = GUIInputManager.get_model(self.project, model_name) 
        indicators = GUIInputManager.DQA_inidcators(model)
        GUIOutputManager.get_hotspots(model, impact_category='GWP')

        # build score panel
        width = 15
        col_entry_frame = Frame(frame)
        col_entry_frame.pack(pady=10)

        n = len(self.impact_categories) + 3
        headers = ['Flow', 'Impact (GWP)'] + indicators + ['DQS']
        for i in range(n):
            data = Entry(col_entry_frame, relief="solid", width=width + 2, justify='center')
            data.insert(0, headers[i])
            data.pack(side=LEFT, padx=11)

        pedigree_score_dict = GUIInputManager.get_pedigree_score_objs(self.project, model_name)
        score_list = list(GUIInputManager.get_DQS_range(self.project))
        DQS_entry_dict = {}
        for obj in pedigree_score_dict:
            tmp_entry_frame = Frame(frame)
            tmp_entry_frame.pack(pady=10)
            
            if obj.is_hotspot:
                entry_vars = {'bg':"red", 'fg':"white", 'relief':"solid", 'width':width + 2, 'justify':'center'}  
            else: 
                entry_vars = {'relief':"solid", 'width':width + 2, 'justify':'center'}  
            
            data = Entry(tmp_entry_frame, **entry_vars)  
            data.insert(0, GUIInputManager.get_name(obj))
            data.pack(side=LEFT, padx=11)

            data = Entry(tmp_entry_frame, **entry_vars)
            data.insert(0, GUIInputManager.get_weighted_impact(obj))
            data.pack(side=LEFT, padx=11)

            for indicator in indicators:
                dropdown = Combobox(tmp_entry_frame, values=score_list, width=width - 2)
                dropdown.pack(side=LEFT, padx=11)
                dropdown.current(score_list.index(GUIInputManager.get_pedigree_score(pedigree_score_dict[obj], indicator)))
                dropdown.bind("<<ComboboxSelected>>", lambda x, obj=obj, indicator=indicator: self.update_DQS(x, obj, pedigree_score_dict, indicator, DQS_entry_dict, model_name, 
                                                                                                              gradient_bar, marker, marker_label,gb_width, gb_height))
                
            data = Entry(tmp_entry_frame, **entry_vars)
            data.insert(0, GUIInputManager.get_DQS(pedigree_score_dict[obj]))
            data.pack(side=LEFT, padx=11)
            DQS_entry_dict[obj] = data

        # create gradient bar for DQS for model
        gb_height, gb_width = 25, 500
        gradient_bar = Canvas(frame, width=gb_width, height=gb_height + 20, bg="white")
        gradient_bar.pack(pady=20)
        for i in range(gb_width):
            r = int((1 - i / gb_width) * 255)
            g = int((i / gb_width) * 255)
            color = f"#{r:02x}{g:02x}00"
            gradient_bar.create_line(i, 0, i, gb_height, fill=color, width=1)

        value = GUIInputManager.calculate_model_DQS(self.project, model_name)
        x_position = value * gb_width / 100
        marker =  gradient_bar.create_line(0, 0, 0, gb_height, fill="black", width=2)
        marker_label =  gradient_bar.create_text(0, gb_height + 10, text="", anchor="n", font=("Arial", 10))
        gradient_bar.coords(marker, x_position, 0, x_position, gb_height)
        gradient_bar.itemconfig(marker_label, text=f"{int(value):2d}")

    def update_DQS(self, event, obj, pedigree_score_dict, indicator, DQS_entry_dict, model_name, gradient_bar, marker, marker_label,gb_width, gb_height):

        new_value = event.widget.get()

        GUIInputManager.set_pedigree_score(pedigree_score_dict[obj], indicator, int(new_value))

        DQS_entry_dict[obj].delete(0, END)
        DQS_entry_dict[obj].insert(0, GUIInputManager.get_DQS(pedigree_score_dict[obj]))
     
        self.update_marker(model_name, gradient_bar, marker, marker_label,gb_width, gb_height)

    def update_marker(self, model_name, gradient_bar, marker, marker_label,gb_width, gb_height):

        value = GUIInputManager.calculate_model_DQS(self.project, model_name)
        x_position = value * gb_width / 100
        gradient_bar.coords(marker, x_position, 0, x_position, gb_height)
        gradient_bar.coords(marker_label, x_position, gb_height + 10)
        gradient_bar.itemconfig(marker_label, text=f"{int(value):2d}")

    # =================================
    # VIEW MENU
    # =================================

    def create_view_menu(self, menubar):
        
        menu_view = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_view, label='View')

        menu_view.add_command(label='Cell view', command= lambda: self.open_cell_view(menubar))

    def open_cell_view(self, menubar):

        popup = Popup(menubar, "Bill of materials", "1400x600")

        input_frame = Frame(popup)
        input_frame.pack(side=TOP, pady=10, padx=10)
        
        label = Label(input_frame, bg=self.plotter_bg_color, fg='white', text="Model", font = ('Helvetica', 12,'bold'))
        label.pack(side=LEFT, padx=(0, 10))
        
        dropdown = Combobox(input_frame, values=list(GUIInputManager.get_all_model_names(self.project)))
        dropdown.pack(side=RIGHT, fill=BOTH)
        dropdown.current(0)
        dropdown.bind("<<ComboboxSelected>>", lambda x:self.update_cell_table(cell_table, x.widget.get()))

        cell_table = CellTable(popup, self, self.get_current_model())

    def update_cell_table(self, cell_table, model):

        cell_table.delete(*cell_table.get_children())

        GUIInputManager.set_current_model(self.project, model)
        cell_table.model = model
        cell_table.import_data()


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

        if self.documentation_file_path is not None:
            if os.name == 'nt':  # For Windows
                os.startfile(self.documentation_file_path)
            elif os.name == 'posix':  # For macOS or Linux
                os.system(f'open "{pdf_path}"')
            else:
                print("Unsupported OS")
