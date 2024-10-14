import tkinter as tk
from tkinter.ttk import Treeview
import string

class CellTable(Treeview):

    def __init__(self, root):
        super().__init__(master=root, columns=("A", "B", "C"), show='headings')
        self.pack(fill="both", expand=True)

        headings = ["id", "Name", "LC stage", "qty", "unit", "GWP"]
        for alpha, heading in zip(string.ascii_lowercase, headings):
            self.heading(alpha, text=heading)
            self.column(alpha, width=100)

        # Define the column widths
        self.column("A", width=100)
        self.column("B", width=100)
        self.column("C", width=100)

        # Insert some sample data
        data = [
            ("Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"),
            ("Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"),
            ("Row 3 Col 1", "Row 3 Col 2", "Row 3 Col 3"),
        ]

        for row in data:
            self.insert("", tk.END, values=row)

        # Bind double-click event to start cell editing
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
        entry = tk.Entry(self.master)
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
    
    

    def cell_updated(item_id, col_index, new_value):
        """Callback function when a cell is updated."""
        print(f"Cell at Row {item_id}, Column {col_index} updated to: {new_value}")
