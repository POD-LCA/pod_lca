from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.item import Item

from numpy import ceil, power, log10

class Process(Item):

    # =================================
    # Process Items
    # =================================

    def open_popup_process(self):

        popup = Popup(self, "Create process", "300x225")
        
        name =  Popup._popup_input_field(popup, "Process name: ", default_val="new Process")
        lca_data = Popup._popup_input_combo(popup, "LCA data: ", [None] + GUIInputManager.get_database_data(self.project)['Flow'].tolist())    
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = Popup._popup_input_field(popup, "qty: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["m3", "kg"])  

        cmd = lambda: self.create_process(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), lca_data.get())
        Popup.button_pack_OKCancel(popup, popup, cmd)
        
        self.wait_window(popup)
        self.update_plot()
        
    def create_process(self, popup, name, qty, unit, stage, lca_data):

        model_id = self.get_current_model()

        process = GUIInputManager.create_process(self.project, name, unit, float(qty), stage, lca_data)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Process.create_canvas_item(self, model_id, name, stage, qty, unit, self.color_process, tags=["process"])
        slider_cmd = lambda x: Process.update_qty(self, item_id, x)
        slider, slider_data = Process.create_slider(self, model_id, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        Process.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(process, item_id)
        self.item_map[model_id][item_id] = process

        self.update_plot()
        if self.hotspot_on_off.get():
            self.show_hotspots()
            
        popup.destroy()

    def restore_process(self, model, process, cords):
        
        slider_cmd = lambda x: GUIInputManager.update_qty(self, process, x) 
        return Process.restore_item(self, model, process, cords, self.color_process, ["process"], slider_cmd)
