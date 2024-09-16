from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.product import Product

from numpy import ceil, power, log10

class WasteProduct(Product):

    # =================================
    # Product Items
    # =================================

    def open_popup_waste(self):

        popup = Popup(self, "Create waste product", "300x250")
        
        name =  popup._popup_input_field("Waste name: ", default_val="Waste 01")     
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["kg", "lb", "g"])

        cmd = lambda: self.create_waste_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get())
        popup.button_pack_OKCancel(cmd)
        
    def create_waste_product(self, popup, name, qty, unit, stage):

        start = [50, 50]
        height = 100
        width = 100

        product = GUIInputManager.create_waste(self.project.model, name, unit, float(qty), stage)
        slider_cmd = lambda x: GUIInputManager.update_qty(self, product, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = WasteProduct.create_canvas_item(self, name, stage, start, height, width, self.color_waste, tags=["product", "waste"])
        slider, slider_data = WasteProduct.create_slider(self, start, height, width, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        WasteProduct.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(product, item_id)
        self.item_map[item_id] = product

        popup.destroy()

