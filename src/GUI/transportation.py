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

        popup = Popup(self, "Create transportation process", "300x225")
        
        name =  Popup._popup_input_field(popup, "Transportation by: ", default_val="vehicle")    
        lca_data = Popup._popup_input_combo(popup, "LCA data: ", [None] + GUIInputManager.get_database_data(self.project)['Flow'].tolist())
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"], default_entry=1, default_state=DISABLED)
        travel_dist = Popup._popup_input_field(popup, "travel distance: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["km", "mi"])  

        cmd = lambda: self.create_transport_process(popup, name.get(), travel_dist.get(), units.get(), life_cycle_stage.get(), lca_data.get())
        Popup.button_pack_OKCancel(popup, popup, cmd)
        
        self.wait_window(popup)
        self.update_plot()
        
    def create_transport_process(self, popup, name, qty, unit, stage, lca_data):
        
        model_id = self.get_current_model()

        process = GUIInputManager.create_transport_process(name, self.project, unit, float(qty), stage, lca_data)

        if not process is None:
            slider_min = 0.0
            slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
            resolution = (slider_max - slider_min) / 100
            
            item_id, text_item, text_id = Transportation.create_canvas_item(self, model_id, name, stage, qty, unit, self.color_transport, tags=["process", "transportation"])
            slider_cmd = lambda x: Transportation.update_qty(self, item_id, x)
            slider, slider_data = Transportation.create_slider(self, model_id, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
            Transportation.item_bind(self, item_id, text_item, text_id, slider, slider_data)

            GUIInputManager.set_id(process, item_id)
            self.item_map[model_id][item_id] = process

            self.update_plot()
            if self.hotspot_on_off.get():
                self.show_hotspots()
                
            popup.destroy()
            return process
        
        else:
            return None
    
    def restore_transportation_process(self, model, process, cords):

        slider_cmd = lambda x: GUIInputManager.update_transport_dist(self, process, x)
        
        return Transportation.restore_item(self, model, process, cords, self.color_transport, ["process","transportation"], slider_cmd)

    @classmethod
    def update_qty(cls, master, item_id, qty):

        model_id = master.get_current_model()
        process = master.item_map[model_id][item_id]

        cmd = lambda: GUIInputManager.update_transport_dist(master, process, qty)
        cls._on_update(master, item_id, cmd, update_slider=False)

    # =================================
    # Context Menu (Overides)
    # =================================

    @classmethod
    def change_unit(cls, master, item_id):

        model_id = master.get_current_model()

        popup = Popup(master, "Change units", "300x200")
        item = master.item_map[model_id][item_id]

        unit_list = GUIInputManager.get_all_units_list(master.project)
        default_entry = unit_list.index(GUIInputManager.get_travel_unit(item))
        unit = Popup._popup_input_combo(popup, "units: ", unit_list, default_entry=default_entry) # TODO: Units to match current units

        cmd = lambda: cls._update_slider_label(master, model_id, item_id, unit.get(), unit_list[default_entry])

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_slider_label(cls, master, model_id, item_id, new_unit, old_unit):

        item = master.item_map[model_id][item_id]
        GUIInputManager.set_travel_unit(item, new_unit)

        conversion_factor = GUIInputManager.unit_conversion(master.project, old_unit, new_unit)
        if conversion_factor is not None:
            master.slider_map[model_id][item_id]
            old_val = master.sliders[model_id][item_id]["widget"].get()
            new_val = old_val * conversion_factor

            GUIInputManager.update_transport_dist(master, item, new_val)

            master.sliders[model_id][item_id]["widget"].update_value(new_val)

            master.slider_map[model_id][item_id].config(label= "Qty (in {})".format(new_unit))
        else:
            raise TypeError
        
    @classmethod
    def _update_label(cls, master, item_id, update_slider=False):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]
        slider = master.slider_map[model_id][item_id]

        text_str = GUIInputManager.get_name(item) + '\n' + GUIInputManager.get_stage(item)
        if not slider._always_on:
            text_str += '\n' + str(GUIInputManager.get_travel_distance(item)) + ' ' + GUIInputManager.get_travel_unit(item)
        if update_slider:
            slider.update_value(GUIInputManager.get_travel_distance(item))
        text_item = master.label_map[item_id]
        master.current_canvas.itemconfig(text_item, text=text_str)