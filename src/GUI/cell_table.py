from GUI.GUI_inputManager import GUIInputManager
from GUI.GUI_outputManager import GUIOutputManager
from GUI.item_context_menu import ItemContextMenuMixin

import re
from tkinter import END, E, W, CENTER, RIGHT, BOTH, TOP, LEFT, Entry, Label, StringVar
from tkinter.ttk import Treeview, Scrollbar, Combobox, Frame


class CellTable(Treeview):

    def __init__(self, root, GUI, model):
        super().__init__(master=root, columns=list(range(12)), show='headings')
        self.GUI = GUI
        self.model = model
        self.row_ids = {}
        self.pack(side='left', fill="both", expand=True)

        scrollbar = Scrollbar(root, orient="vertical", command=self.yview)
        self.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.headings = ["id", "Name", "Impact data", "type", "LC stage", "qty", "unit", "GWP", "AP", "EP", "ODP", "SFP"]
        widths = [50, 200, 125, 125, 50, 50, 50, 50, 50, 50, 50, 50]
        align = [CENTER, W, W, CENTER, CENTER, E, W, E, E, E, E, E]
        self.locked_columns = [1, 3, 4, 5, 8, 9, 10, 11, 12]
        self.impact_col = 3
        self.lc_stage_col = 5
        self.create_headings(self.headings, widths, align)
        self.import_data()

    def create_headings(self, headings, widths, align):

        for col, heading in enumerate(headings):
            self.heading(col, text=heading, command=lambda _col=col: self.sort_column(_col, False))

        for col, (width, anchor) in enumerate(zip(widths, align)):
            self.column(col, width=width, anchor=anchor)
    
    def import_data(self, hotspots=True):

        if hotspots:
            hotspots = GUIOutputManager.get_hotspots(self.GUI.project, self.model)
            self.tag_configure("hotpsot", background=self.GUI.hotspot_color)

        for product in GUIInputManager.get_all_products(self.GUI, self.model) + GUIInputManager.get_all_processes(self.GUI, self.model): 
            if hotspots:
                tag = "hotpsot" if product in hotspots else ""
            else:
                tag = ""

            row_id = self.insert("", END, iid=GUIInputManager.get_id(product), values=(self.get_obj_values(product)), tags=(tag,))
            self.row_ids[row_id] = product

        self.bind("<Double-1>", lambda event: self.edit_cell(event))

    def get_obj_values(self, obj):

        decimal_places = 2
        values = []
        for heading in self.headings:
            if heading == "id":
                obj_id = GUIInputManager.get_id(obj)
                disp_id = self.GUI.item_disp_num[self.model][obj_id]
                values.append(str(disp_id))
            elif heading in ["Name", "name"]:
                values.append(str(GUIInputManager.get_name(obj)))
            elif heading in ["Impact data"]:
                values.append(str(GUIInputManager.get_database_row(obj)))
            elif heading in ["stage", "LC stage"]:
                values.append(str(GUIInputManager.get_stage(obj)))         
            elif heading in ["type"]:
                temp = str(type(obj)).split(".")[-1]
                type_name = re.sub(r'[^A-Za-z0-9 ]+', '', temp)
                values.append(type_name)
            elif heading == "qty":
                val = GUIInputManager.get_qty(obj)
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            elif heading == "unit":
                values.append(str(GUIInputManager.get_unit(obj)))
            elif heading == "GWP":
                val = GUIInputManager.get_impact_val(obj, 'GWP')
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            elif heading == "AP":
                val = GUIInputManager.get_impact_val(obj, 'acid_pot')
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            elif heading == "EP":
                val = GUIInputManager.get_impact_val(obj, 'eutro_pot')
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            elif heading == "ODP":
                val = GUIInputManager.get_impact_val(obj, 'ozone')
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            elif heading == "SFP":
                val = GUIInputManager.get_impact_val(obj, 'smog')
                val_str = str(CellTable.format_number(val, decimal_places))
                values.append(val_str)
            else:
                raise NotImplementedError
            
        return values

    def edit_cell(self, event):
        """ Edit value in cell. 
            This is done by creating a dummy tkinter.Entry on top of the cell.
        """

        selected_item = self.selection()[0]
        column = self.identify_column(event.x)
        col_num = int(column.replace('#', ''))
        x, y, width, height = self.bbox(selected_item, column)
        cell_value = self.item(selected_item, 'values')[col_num - 1]
        
        if col_num not in self.locked_columns:
            entry = Entry(self.master)
            entry.place(x=x + self.winfo_x(), y=y + self.winfo_y(), width=width, height=height)
            entry.insert(0, cell_value)
            entry.focus()

            entry.bind("<Return>", lambda event: self.on_enter(event, entry, selected_item, col_num))
            entry.bind("<Escape>", lambda event: self.cancel_edit(event, entry))

        if col_num == self.lc_stage_col:
            combobox_var = StringVar()
            combobox_var.set(cell_value)            
            dropdown_options = ['A1', 'A2', 'A3']
            dropdown_combobox = Combobox(self.master, textvariable=combobox_var, values=dropdown_options, state="readonly")
            dropdown_combobox.place(x=x, y=y + (2 * height), width=width)
            dropdown_combobox.focus()

            dropdown_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_lc_stage(event, dropdown_combobox, combobox_var))
            dropdown_combobox.bind("<Escape>", lambda event: self.cancel_edit(event, dropdown_combobox))

        if col_num == self.impact_col:
            combobox_var = StringVar()
            combobox_var.set(cell_value)
            dropdown_options = GUIInputManager.get_database_data(self.GUI.project)['Flow'].tolist()
            dropdown_combobox = Combobox(self.master, textvariable=combobox_var, values=dropdown_options, state="readonly")
            dropdown_combobox.place(x=x, y=y + (2 * height), width=width)
            dropdown_combobox.focus()
            
            dropdown_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_impact_data(event, dropdown_combobox, combobox_var))
            dropdown_combobox.bind("<Escape>", lambda event: self.cancel_edit(event, dropdown_combobox))

    def on_enter(self, event, entry, selected_item, col_num):
        
        new_value = entry.get()
        current_values = list(self.item(selected_item, 'values'))
        current_values[col_num - 1] = new_value
        self.item(selected_item, values=current_values)
        entry.destroy()

        if self.headings[col_num - 1]  in  ["Name", "name"]:
            GUIInputManager.edit_name(self.GUI, self.GUI.item_map[self.model][int(selected_item)], new_value)
        elif self.headings[col_num - 1]  in  ["stage", "LC stage"]:
            GUIInputManager.update_life_cycle_stage(self.GUI, self.GUI.item_map[self.model][int(selected_item)], new_value)
        elif self.headings[col_num - 1] == "qty":
            GUIInputManager.update_qty(self.GUI, self.GUI.item_map[self.model][int(selected_item)], new_value)
        elif self.headings[col_num - 1]  in  ["unit"]:
            GUIInputManager.change_unit(self.GUI, self.GUI.item_map[self.model][int(selected_item)], new_value)
        
        self.update_entry(selected_item)


    def update_impact_data(self, event, dropdown_combobox, combobox_var):

        selected_impact = combobox_var.get()
        selected_item = self.focus()

        GUIInputManager.set_impact_data(self.GUI, self.GUI.item_map[self.model][int(selected_item)], selected_impact)    

        dropdown_combobox.place_forget()

        self.update_entry(selected_item)

    def update_lc_stage(self, event, dropdown_combobox, combobox_var):

        selected_stage = combobox_var.get()
        selected_item = self.focus()

        GUIInputManager.update_life_cycle_stage(self.GUI, self.GUI.item_map[self.model][int(selected_item)], selected_stage)    

        dropdown_combobox.place_forget()

        self.update_entry(selected_item)
        
    def sort_column(self, col, reverse):
        """Sort the items in the selected column."""

        data_list = [(self.set(item, col), item) for item in self.get_children('')]

        if CellTable.is_float(data_list[0][0]):
            data_list.sort(reverse=reverse, key=lambda x: float(x[0]))
        else:
            data_list.sort(reverse=reverse, key=lambda x: x[0])

        for index, (val, item) in enumerate(data_list):
            self.move(item, '', index)
        
        self.heading(col, command=lambda: self.sort_column(col, not reverse))    


    @staticmethod
    def is_float(value):
        try:
            float(value)  
            return True
        except ValueError:
            return False
    
    @staticmethod
    def format_number(num, decimal_places=6, large_cutoff=10000):
        
        if abs(num) < 10 ** -decimal_places or abs(num) >= large_cutoff:
            return f"{num:.{decimal_places}e}"
        else:
            return f"{num:.{decimal_places}f}"
        
    def update_entry(self, row_id):
        """ Update the row of the column.
        """

        product = self.row_ids[row_id]
        self.item(row_id, values=(self.get_obj_values(product)))
        self.GUI.update_plot()
        ItemContextMenuMixin._update_label(self.GUI, int(row_id), update_slider=False)
                
        if GUIInputManager.get_transporter(product) is not None:
            transporter = GUIInputManager.get_transporter(product)
            self.update_entry(str(GUIInputManager.get_id(transporter)))

        # TODO: run hostspot analysis... and check those rows are red

    def cancel_edit(self, event, item):

        item.place_forget()

    # def filter_column(self, column_index, filter_value):

    #     self.delete(*self.get_children())
        
    #     for row_id, product in self.row_ids.items():
    #         if str(product[column_index]).startswith(filter_value):
    #             self.insert("", END, iid=GUIInputManager.get_id(product), values=(self.get_obj_values(product)), tags=(tag,))
        