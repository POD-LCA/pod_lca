from GUI.popup import Popup
from GUI.GUI_inputManager import GUIInputManager
from GUI.item import Item

import re
from tkinter import Menu, Frame, Button
from tkinter import RIGHT, LEFT, Y, BOTH, TOP, DISABLED, ACTIVE

class Relationships:

    def set_relationship(self, item, slider):

        popup = Popup(self, "Set realtionship", "600x150")
        
        label = popup._popup_label("Set relationship to other items on the canvas: \n e.g., {3} * 4.6 to set the qty to be always be 4.6 times that of item 3.", justify='left', font=("Arial",10))
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))   
        
        txt_str = '{' + str(item) + '} = '
        default_str = self.relationships[item] if item in self.relationships else ''
        relationship = popup._popup_input_field(txt_str, default_val=default_str)
        
        cmd =lambda : self.process_relationship(item, slider, relationship.get())          
        
        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)

        apply_button = Button(button_frame, text="Apply", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
        apply_button.pack(side=LEFT, padx=10)

    def process_relationship(self, item, slider, relationship):

        slider.config(state=DISABLED)

        masters = re.findall(r'\{ *(-?\d+(?:\.\d*)?) *\}', relationship)

        cyclicDependence = False
        if item in self.dependents:
            for master in masters:
                if master in self.dependents[item]:
                    cyclicDependence = True
                    break
        
        if not cyclicDependence:
            self.relationships[item] = relationship
            for master in masters:
                if int(master) not in self.dependents:
                    self.dependents[int(master)] = [item]
                else:
                    if not item in self.dependents[int(master)]:
                        self.dependents[int(master)].append(item)

    def update_dependent_qtys(self, item, qty):

        item_id = GUIInputManager.get_id(item)

        if item_id in self.dependents:
            for dependent in self.dependents[item_id]:
                rel = self.relationships[dependent]
                rel_ss = re.sub(r'\s+', '', rel)
                masters = re.findall(r'\{ *(-?\d+(?:\.\d*)?) *\}', rel_ss)
                for master in masters:
                    master_item = Item.item_from_id(self, int(master))
                    if GUIInputManager.is_transport(master_item):
                        qty = GUIInputManager.get_travel_distance(master_item)
                    else:
                        qty = GUIInputManager.get_qty(master_item)
 
                    tag_str = '{' + str(master) + '}'
                    rel_ss = rel_ss.replace(tag_str, str(qty))

                expression = re.sub(r'\{ *(-?\d+(?:\.\d*)?) *\}', r'\1', rel_ss)
                try:
                    calc_qty = eval(expression)
                except Exception as e:
                    f"Error evaluating expression: {e}"

                dependent_item = Item.item_from_id(self, dependent)
                GUIInputManager.update_qty(self, dependent_item, calc_qty)
                slider = self.slider_map[dependent]
                slider.config(state=ACTIVE) 
                slider.set(calc_qty)
                slider.config(state=DISABLED)

    def clear_relationship(self, item):

        self.relationships.pop(item, None)
        for dependent in self.dependents:
            if item in self.dependents[dependent]:
                self.dependents[dependent].remove(item)

        slider = self.slider_map[item]
        slider.config(state=ACTIVE) 


    def highlight_dependents(self, event):

        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self.dependents:
            for dependent in self.dependents[item]:
                self.canvas.itemconfig(dependent, outline=self.highlight_color, width=self.highlight_width)
                self.canvas.current_highlight = dependent

    def remove_highight(self, event):

        if hasattr(self.canvas, 'current_highlight'):
            self.canvas.itemconfig(self.canvas.current_highlight, outline=self.outline_color, width=self.outline_width)
