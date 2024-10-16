from GUI.GUI_inputManager import GUIInputManager
from GUI.GUI_outputManager import GUIOutputManager

from tkinter import END, E, W, CENTER, Entry
from tkinter.ttk import Treeview, Scrollbar


class CellTable(Treeview):

    def __init__(self, root, project):
        super().__init__(master=root, columns=list(range(7)), show='headings')
        self.project = project
        self.pack(fill="both", expand=True)

        scrollbar = Scrollbar(self, orient="vertical", command=self.yview)
        self.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        headings = ["id", "Name", "type", "LC stage", "qty", "unit", "GWP"]
        widths = [50, 200, 100, 50, 50, 50, 50]
        align = [CENTER, W, CENTER, CENTER, E, W, CENTER]
        self.create_headings(headings, widths, align)
        self.import_data(model="Model_0")

    def create_headings(self, headings, widths, align):

        for col, heading in enumerate(headings):
            self.heading(col, text=heading, command=lambda _col=col: self.sort_column(_col, False))

        for col, (width, anchor) in enumerate(zip(widths, align)):
            self.column(col, width=width, anchor=anchor)
        
    
    def import_data(self, model="Model_0", hotspots=True):

        if hotspots:
            hotspots = GUIOutputManager.get_hotspots(self.project, model)
            self.tag_configure('hotpsot', background='lightgreen')

        for product in self.project.models[model].products + self.project.models[model].processes: # TODO: call through input manager
            if hotspots:
                if product in hotspots:
                    tag = 'hotspot'
                else:
                    tag = ''
            else:
                tag = ''

            self.insert("", END, values=(str(GUIInputManager.get_id(product)), 
                                            str(GUIInputManager.get_name(product)),
                                            str(type(product)),
                                            str(GUIInputManager.get_stage(product)),
                                            str(GUIInputManager.get_qty(product)),
                                            str(GUIInputManager.get_unit(product)),
                                            str(round(GUIInputManager.get_impacts(product).GWP, 1))), 
                                            tags=(tag))

        self.bind("<Double-1>", self.edit_cell)

    def edit_cell(self, event):
        # Find the row and column of the selected item
        selected_item = self.selection()[0]
        column = self.identify_column(event.x)  # E.g. '#1' for first column
        
        # Get the column number (e.g. from '#1' to 1)
        col_num = int(column.replace('#', ''))
        
        # Get the bounding box of the selected cell
        x, y, width, height = self.bbox(selected_item, column)
        
        # Get the current value in the selected cell
        cell_value = self.item(selected_item, 'values')[col_num - 1]
        
        # Create an Entry widget and place it over the cell
        entry = Entry(self.master)
        entry.place(x=x + self.winfo_x(), y=y + self.winfo_y(), width=width, height=height)
        entry.insert(0, cell_value)
        entry.focus()

        entry.bind("<Return>", self.on_enter)

    # Bind Enter key to save the new value
    def on_enter(self, event):
        pass
    #     new_value = entry.get()
    #     current_values = list(tree.item(selected_item, 'values'))
    #     current_values[col_num - 1] = new_value
    #     tree.item(selected_item, values=current_values)
    #     entry.destroy()  # Remove the Entry widget
        
    #     # Call a function to handle the updated value (optional)
    #     cell_updated(selected_item, col_num - 1, new_value)
    
    def sort_column(self, col, reverse):
        """Sort the items in the selected column."""
        # Get all items in the treeview and sort them based on the column
        data_list = [(self.set(item, col), item) for item in self.get_children('')]
        
        # Sort data based on the column values (ascending or descending based on 'reverse')
        if CellTable.is_float(data_list[0][0]):
            data_list.sort(reverse=reverse, key=lambda x: float(x[0]))
        else:
            data_list.sort(reverse=reverse, key=lambda x: x[0])

        # Rearrange the items in the treeview
        for index, (val, item) in enumerate(data_list):
            self.move(item, '', index)
        
        # Toggle the sorting order for the next time the header is clicked
        self.heading(col, command=lambda: self.sort_column(col, not reverse))    

    def cell_updated(item_id, col_index, new_value):
        """Callback function when a cell is updated."""
        print(f"Cell at Row {item_id}, Column {col_index} updated to: {new_value}")

    @staticmethod
    def is_float(value):
        try:
            float(value)  
            return True
        except ValueError:
            return False