from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider
from GUI.item import Item

from numpy import ceil, power, log10
from tkinter import Menu, Frame, Button
from tkinter import LEFT

class Product(Item):

    # =================================
    # Product Objects
    # =================================

    def open_popup_product(self):

        popup = Popup(self, "Create product", "300x250")
        
        name =  popup._popup_input_field("Product name: ", default_val="new Product") 
        # type = popup._popup_input_combo("type: ", ["material", "energy"])     
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"])   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["kg", "lb", "g", "m3"])  
        density = popup._popup_input_field("mass per unit product: ", validate_num=True, default_val=1.0)

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), density.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_product(self, popup, name, qty, units, stage, density):

        start = [50, 50]
        height = 100
        width = 100

        product = GUIInputManager.create_product(self.project.model, name, units, float(qty), stage, density)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Item.create_canvas_item(self, name, stage, start, height, width, self.color_product, tags="product")
        slider, slider_data = Item.create_slider(self, start, height, width, product, qty, units, item_id, slider_min, slider_max, resolution)
        Item.item_bind(self, item_id, text_item, text_id, slider, slider_data, product=True)

        GUIInputManager.set_id(product, item_id)
        self.product_data[item_id] = product

        popup.destroy()

    def restore_product(self, product, cords):

        return Item.restore_item(self, product, cords, self.color_product, "product", product=True)


