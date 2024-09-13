from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.item import Item

from numpy import ceil, power, log10
from tkinter import DISABLED

class Transportation(Item):

    # =================================
    # Process Items
    # =================================

    def open_popup_transport_process(self):

        popup = Popup(self, "Create transportation process", "300x200")
        
        name =  popup._popup_input_field("Transportation by: ", default_val="vehicle")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=1, default_state=DISABLED)
        travel_dist = popup._popup_input_field("travel distance: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["km", "mi"])  

        cmd = lambda: self.create_transport_process(popup, name.get(), travel_dist.get(), units.get(), life_cycle_stage.get())
        popup.button_pack_OKCancel(cmd)
        
    def create_transport_process(self, popup, name, qty, units, stage):
        
        start = [50, 50]
        height = 100
        width = 100

        process = GUIInputManager.create_transport_process(self.project.model, name, self.project, units, float(qty), stage)
        slider_cmd = lambda x: GUIInputManager.update_transport_dist(self, process, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100
        
        item_id, text_item, text_id = Transportation.create_canvas_item(self, name, stage, start, height, width, self.color_transport, tags=["process", "transportation"])
        slider, slider_data = Transportation.create_slider(self, start, height, width, qty, units, item_id, slider_cmd, slider_min, slider_max, resolution)
        Transportation.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(process, item_id)
        self.item_map[item_id] = process

        popup.destroy()

    def restore_transportation_process(self, process, cords):

        slider_cmd = lambda x: GUIInputManager.update_transport_dist(self, process, x)
        
        return Transportation.restore_item(self, process, cords, self.color_transport, ["process","transportation"], slider_cmd)

    # =================================
    # Context Menu (Overides)
    # =================================

    @classmethod
    def change_unit(cls, master, item_id):

        popup = Popup(master, "Change units", "300x200")
        item = master.item_map[item_id]

        unit_list = ["m3", "kg", "lb", "MJ", "km", "mi"]
        default_entry = unit_list.index(GUIInputManager.get_travel_unit(item))
        unit = popup._popup_input_combo("units: ", unit_list, default_entry=default_entry) # TODO: Units to match current units

        cmd = lambda: cls._update_slider_label(master, item_id, unit.get(), unit_list[default_entry])

        popup.button_pack_OKCancel(cmd)

    @classmethod
    def _update_slider_label(cls, master, item_id, new_unit, old_unit):

        item = master.item_map[item_id]
        GUIInputManager.set_unit(item, new_unit)

        conversion_factor = GUIInputManager.unit_conversion(master.project, old_unit, new_unit)
        if conversion_factor is not None:
            master.slider_map[item_id]
            old_val = master.sliders[item_id]["widget"].get()
            new_val = old_val * conversion_factor

            GUIInputManager.update_transport_dist(master, item, new_val)

            master.sliders[item_id]["widget"].update_value(new_val)

        master.slider_map[item_id].config(label= "Qty (in {})".format(new_unit))