from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.item import Item

from numpy import ceil, power, log10

class Process(Item):

    # =================================
    # Process Items
    # =================================

    def open_popup_process(self):

        popup = Popup(self, "Create process", "300x200")
        
        name =  popup._popup_input_field("Process name: ", default_val="new Process")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["m3", "kg"])  

        cmd = lambda: self.create_process(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get())
        popup.button_pack_OKCancel(cmd)
        
        
    def create_process(self, popup, name, qty, unit, stage):

        start = [50, 50]
        height = 100
        width = 100

        process = GUIInputManager.create_process(self.project.model, name, unit, float(qty), stage)
        slider_cmd = lambda x: GUIInputManager.update_qty(self, process, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Process.create_canvas_item(self, name, stage, start, height, width, self.color_process, tags=["process"])
        slider, slider_data = Process.create_slider(self, start, height, width, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        Process.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(process, item_id)
        self.item_map[item_id] = process

        popup.destroy()

    def restore_process(self, process, cords):
        
        slider_cmd = lambda x: GUIInputManager.update_qty(self, process, x) 
        return Process.restore_item(self, process, cords, self.color_process, ["process"], slider_cmd)
