from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider
from GUI.item import Item

from tkinter import Menu, Frame, Button, Label
from tkinter import LEFT

class Process(Item):

    # =================================
    # Process Objects
    # =================================

    def open_popup_process(self):

        popup = Popup(self, "Create process", "300x200")
        
        name =  popup._popup_input_field("Process name: ", default_val="new Process")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["m3", "kg"])  

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_process(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_process(self, popup, name, qty, units, stage):

        start = [50, 50]
        height = 100
        width = 100

        process = GUIInputManager.create_process(self.project.model, name, units, float(qty), stage)
        process_id = GUIInputManager.get_id(process)

        item_id, text_item, text_id = Item.create_canvas_item(self, name, stage, start, height, width, self.color_process, tags="process")
        slider, slider_data = Item.create_slider(self, start, height, width, process, qty, units, item_id)
        Item.item_bind(self, item_id, text_item, text_id, slider, slider_data, process=True)

        self.process_data[item_id] = process
        self.process_item_map[process_id] = item_id

        popup.destroy()

    def restore_process(self, process, cords):
        
        return Item.restore_item(self, process, cords, self.color_process, "process", process=True)
