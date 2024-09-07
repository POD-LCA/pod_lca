from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider
from GUI.item import Item

from tkinter import Menu, Frame, Button, Label
from tkinter import LEFT

class Parameter(Item):

    # =================================
    # Process Objects
    # =================================

    def open_popup_parameter(self):

        popup = Popup(self, "Parameter", "300x200")
        
        name =  popup._popup_input_field("Parameter name: ", default_val="new Parameter")   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["m3", "kg", "unit"])  

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_parameter(popup, name.get(), qty.get(), units.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_parameter(self, popup, name, qty, units):

        start = [50, 50]
        height = 50
        width = 100

        item_id, text_item, text_id = Item.create_canvas_item(self, name, '', start, height, width, self.color_parameter, tags="parameter")
        slider, slider_data = self.create_slider(start, height, width, None, qty, units, item_id)
        Item.item_bind(self, item_id, text_item, text_id, slider, slider_data, process=True)

        popup.destroy()

    def create_slider(self, start, height, width, item, qty, units, item_id, transport=False):

        x, y = start[0], start[1] + height * self.scale

        cmd = None

        slider = Slider(self.canvas, "Qty (in {})".format(units), min=0, max=100, width=self.default_slider_width*self.scale, length= width*self.scale, command=cmd)
        slider_data = {"widget": slider, "x": x, "y": y, "length": slider.cget("length")}
        self.sliders.append(slider_data)
        slider.place(in_=self.canvas, x=x, y=y)
        slider.update_value(qty)
        slider.rect = item_id

        return slider, slider_data

    def restore_process(self, item, cords):

        pass
        
        # x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        # start = [x1, y1]
        # height = abs(y2-y1)
        # width = abs(x2-x1)

        # name = GUIInputManager.get_name(item)
        # units = GUIInputManager.get_unit(item)
        # stage = GUIInputManager.get_stage(item)
        # qty = GUIInputManager.get_travel_distance(item) if GUIInputManager.is_transport(item) else GUIInputManager.get_qty(item)

        # item_id, text_item, text_id = Item.create_canvas_item(self, name, stage, start, height, width, color, tags)
        # slider, slider_data = Item.create_slider(self, start, height, width, item, qty, units, item_id, transport)
        # Item.item_bind(self, item_id, text_item, text_id, slider, slider_data, product, process)

        # self.product_data[item_id] = item

        # return item_id
