from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.product import Product

from numpy import ceil, power, log10

class EnergyProduct(Product):

    # =================================
    # Product Items
    # =================================

    def open_popup_energy(self):

        popup = Popup(self, "Create energy product", "300x250")
        
        name =  Popup._popup_input_field(popup, "Energy product name: ", default_val="new Energy Product")     
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = Popup._popup_input_field(popup, "qty: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["kJ", "MJ", "kWh", "MWh"])

        cmd = lambda: self.create_energy_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get())
        Popup.button_pack_OKCancel(popup, popup, cmd)
        
    def create_energy_product(self, popup, name, qty, unit, stage):

        start = [50, 50]
        height = 100
        width = 100
        model_id = self.get_current_model()

        product = GUIInputManager.create_energy(self.project, name, unit, float(qty), stage)
        slider_cmd = lambda x: GUIInputManager.update_qty(self, product, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = EnergyProduct.create_canvas_item(self, model_id, name, stage, start, height, width, self.color_energy, tags=["product", "energy"])
        slider, slider_data = EnergyProduct.create_slider(self, model_id, start, height, width, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        EnergyProduct.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(product, item_id)
        self.item_map[model_id][item_id] = product

        popup.destroy()
