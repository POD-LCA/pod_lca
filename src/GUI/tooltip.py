
import tkinter as tk


# =================================
# Tooltip
# =================================

class Tooltip:
    # TODO: Debugging needed
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event):
        if self.tooltip:
            self.hide_tooltip(None)
        
        # Get the item ID where the mouse is hovering
        item = self.widget.find_closest(event.x, event.y)[0]
        bbox = self.widget.bbox(item)
        if bbox:
            x1, y1, x2, y2 = bbox
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            x = int(x + self.widget.winfo_rootx() + 25)  # Convert to int
            y = int(y + self.widget.winfo_rooty() + 25)  # Convert to int
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=self.text, background="lightyellow", borderwidth=1, relief="solid")
            label.pack()
    
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None