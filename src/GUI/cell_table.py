from GUI.GUI_inputManager import GUIInputManager
from GUI.GUI_outputManager import GUIOutputManager

from tkinter import END, E, W, CENTER, RIGHT, BOTH, TOP, LEFT, Entry, Label
from tkinter.ttk import Treeview, Scrollbar, Combobox, Frame


class CellTable(Treeview):

    def __init__(self, root, GUI, model):
        super().__init__(master=root, columns=list(range(7)), show='headings')
        self.GUI = GUI
        self.pack(fill="both", expand=True)

        scrollbar = Scrollbar(self, orient="vertical", command=self.yview)
        self.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        headings = ["id", "Name", "type", "LC stage", "qty", "unit", "GWP"]
        widths = [50, 200, 100, 50, 50, 50, 50]
        align = [CENTER, W, CENTER, CENTER, E, W, CENTER]
        self.create_headings(headings, widths, align)
        self.import_data(model)

    def create_headings(self, headings, widths, align):

        for col, heading in enumerate(headings):
            self.heading(col, text=heading, command=lambda _col=col: self.sort_column(_col, False))

        for col, (width, anchor) in enumerate(zip(widths, align)):
            self.column(col, width=width, anchor=anchor)
        
    
    def import_data(self, model="Model_0", hotspots=True):

        if hotspots:
            hotspots = GUIOutputManager.get_hotspots(self.GUI.project, model)
            self.tag_configure("hotpsot", background=self.GUI.hotspot_color)

        for product in self.GUI.project.models[model].products + self.GUI.project.models[model].processes: # TODO: call through input manager
            if hotspots:
                tag = "hotpsot" if product in hotspots else ""
            else:
                tag = ""

            self.insert("", END, values=(str(GUIInputManager.get_id(product)), 
                                            str(GUIInputManager.get_name(product)),
                                            str(type(product)),
                                            str(GUIInputManager.get_stage(product)),
                                            str(GUIInputManager.get_qty(product)),
                                            str(GUIInputManager.get_unit(product)),
                                            str(round(GUIInputManager.get_impacts(product).GWP, 1))), 
                                            tags=(tag,))

        self.bind("<Double-1>", lambda event: self.edit_cell(event))

    def edit_cell(self, event):
        """ Edit value in cell. 
            This is done by creating a dummy tkinter.Entry on top of the cell.
        """

        selected_item = self.selection()[0]
        column = self.identify_column(event.x)
        col_num = int(column.replace('#', ''))
        x, y, width, height = self.bbox(selected_item, column)
        cell_value = self.item(selected_item, 'values')[col_num - 1]
        
        #TODO only if the cell is allowed to be edited
        entry = Entry(self.master)
        entry.place(x=x + self.winfo_x(), y=y + self.winfo_y(), width=width, height=height)
        entry.insert(0, cell_value)
        entry.focus()

        entry.bind("<Return>", lambda event: self.on_enter(event, entry, selected_item, col_num))

    def on_enter(self, event, entry, selected_item, col_num):

        new_value = entry.get()
        current_values = list(self.item(selected_item, 'values'))
        current_values[col_num - 1] = new_value
        self.item(selected_item, values=current_values)
        entry.destroy()
        
        # TODO: Call a function to handle the updated value
    
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