from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.product import Product

from numpy import ceil, power, log10

class EnergyProduct(Product):

    # =================================
    # Product Items
    # =================================

    def open_popup_energy(self):

        popup = Popup(self, "Create energy product", "300x225")
        
        name =  Popup._popup_input_field(popup, "Energy product name: ", default_val="new Energy Product")     
        lca_data = Popup._popup_input_combo(popup, "LCA data: ", [None] + GUIInputManager.get_database_data(self.project)['Flow'].tolist())
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = Popup._popup_input_field(popup, "qty: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["kJ", "MJ", "kWh", "MWh"])

        cmd = lambda: self.create_energy_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), lca_data.get())
        Popup.button_pack_OKCancel(popup, popup, cmd)
        
        self.wait_window(popup)
        self.update_plot()
        
    def create_energy_product(self, popup, name, qty, unit, stage, lca_data):

        model_id = self.get_current_model()

        product = GUIInputManager.create_energy(self.project, name, unit, float(qty), stage, lca_data)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = EnergyProduct.create_canvas_item(self, model_id, name, stage, qty, unit, self.color_energy, tags=["product", "energy"])
        slider_cmd = lambda x: EnergyProduct.update_qty(self, item_id, x)
        slider, slider_data = EnergyProduct.create_slider(self, model_id, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        EnergyProduct.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(product, item_id)
        self.item_map[model_id][item_id] = product

        self.update_plot()
        if self.hotspot_on_off.get():
            self.show_hotspots()
            
        popup.destroy()
