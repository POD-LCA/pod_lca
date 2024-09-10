from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider
from GUI.item import Item

from numpy import ceil, power, log10
from tkinter import Frame, Button, Label
from tkinter import LEFT, DISABLED

class Transportation:

    # =================================
    # Process Objects
    # =================================

    def open_popup_transport_process(self):

        popup = Popup(self, "Create transportation process", "300x200")
        
        name =  popup._popup_input_field("Transportation by: ", default_val="vehicle")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=1, default_state=DISABLED)
        travel_dist = popup._popup_input_field("travel distance: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["km", "mi"])  

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_transport_process(popup, name.get(), travel_dist.get(), units.get(), life_cycle_stage.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_transport_process(self, popup, name, qty, units, stage):
        
        start = [50, 50]
        height = 100
        width = 100

        process = GUIInputManager.create_transport_process(self.project.model, name, self.project, units, float(qty), stage)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100
        
        item_id, text_item, text_id = Item.create_canvas_item(self, name, stage, start, height, width, self.color_transport, tags=("process", "transportation"))
        slider, slider_data = Item.create_slider(self, start, height, width, process, qty, units, item_id, slider_min, slider_max, resolution, transport=True)
        Item.item_bind(self, item_id, text_item, text_id, slider, slider_data, process=True)

        GUIInputManager.set_id(process, item_id)
        self.process_data[item_id] = process

        popup.destroy()

    def restore_transportation_process(self, process, cords):
        
        return Item.restore_item(self, process, cords, self.color_transport, ("process","transportation"), process=True, transport=True)
