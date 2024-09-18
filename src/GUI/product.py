from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.item import Item

from numpy import ceil, power, log10

class Product(Item):

    # =================================
    # Product Items
    # =================================

    def open_popup_product(self):

        popup = Popup(self, "Create product", "300x250")
        
        name =  popup._popup_input_field("Product name: ", default_val="new Product")     
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"])   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["kg", "lb", "g", "m3"])  
        density = popup._popup_input_field("mass per unit product: ", validate_num=True, default_val=1.0)

        cmd = lambda: self.create_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), density.get())
        popup.button_pack_OKCancel(cmd)
        
    def create_product(self, popup, name, qty, unit, stage, density):

        start = [50, 50]
        height = 100
        width = 100

        product = GUIInputManager.create_product(self.project.model, name, unit, float(qty), stage, density)
        slider_cmd = lambda x: GUIInputManager.update_qty(self, product, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Product.create_canvas_item(self, name, stage, start, height, width, self.color_product, tags=["product"])
        slider, slider_data = Product.create_slider(self, start, height, width, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        Product.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        GUIInputManager.set_id(product, item_id)
        self.item_map[item_id] = product

        popup.destroy()

    def restore_product(self, product, cords):

        slider_cmd = lambda x: GUIInputManager.update_qty(self, product, x) 

        return Product.restore_item(self, product, cords, self.color_product, ["product"], slider_cmd)


