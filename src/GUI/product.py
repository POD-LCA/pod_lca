from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider

from tkinter import Menu, Frame, Button
from tkinter import LEFT

class Product:

    # =================================
    # Product Objects
    # =================================

    def open_popup_product(self):

        popup = Popup(self, "Create product", "300x300")
        
        name =  popup._popup_input_field("Product name: ", default_val="new Product") 
        # type = popup._popup_input_combo("type: ", ["material", "energy"])     
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"])   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["kg", "m3", "MJ"])  
        density = popup._popup_input_field("mass per unit product: ", validate_num=True, default_val=1.0)

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_product(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), density.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_product(self, popup, name, qty, units, stage, density):

        product = GUIInputManager.create_product(self.project.model, name, units, float(qty), stage, density)
        product_id = GUIInputManager.get_id(product)

        height = 50
        width = 150
        x1, y1, x2, y2 = height*self.scale, height*self.scale, width*self.scale, width*self.scale
 
        item_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", tags="product")
        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = self.canvas.create_text(text_x, text_y, text=text_str)

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = self.canvas.create_text(id_x, id_y, text=str(item_id))

        self.product_data[item_id] = product

        slider = Slider(self.canvas, "Qty (in {})".format(units), min=0, max=100, width=self.default_slider_width, command=lambda x: GUIInputManager.update_qty(self, product, x))
        slider_data = {"widget": slider, "x": x1, "y": y2, "length": slider.cget("length")}
        self.sliders.append(slider_data)
        slider.place(in_=self.canvas, x=x1, y=y2)
        slider.update_value(qty)
        slider.rect = item_id
        
        group_tag = f"group_{item_id}"
        self.canvas.addtag_withtag(group_tag, item_id)
        self.canvas.addtag_withtag(group_tag, text_item)
        self.canvas.addtag_withtag(group_tag, text_id)

        self.canvas.tag_bind(item_id, "<ButtonPress-1>", self.on_start_drag)
        self.canvas.tag_bind(item_id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item_id, "<ButtonRelease-1>", self.on_stop_drag)
        self.canvas.tag_bind(item_id, "<Button-3>", self.show_product_context_menu)

        self.canvas.tag_bind(group_tag, "<B1-Motion>", lambda event: self.move_slider(event, slider, slider_data))

        self.product_item_map[product_id] = item_id

        # self.tooltips[flw] = Tooltip(self.canvas, f"This is a flow")

        popup.destroy()

    def restore_product(self, product, cords):
        
        # TODO: additionally check if a transportation process

        x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        item_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", tags="product")

        name = GUIInputManager.get_name(product)
        units = GUIInputManager.get_unit(product)
        stage = GUIInputManager.get_stage(product)
        qty = GUIInputManager.get_qty(product)
        productID = GUIInputManager.get_id(product)

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = self.canvas.create_text(text_x, text_y, text=text_str, tags="product")

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = self.canvas.create_text(id_x, id_y, text=str(item_id), tags="product")

        self.product_data[item_id] = product
    
        slider = Slider(self.canvas, "Qty (in {})".format(units), min=0, max=100, width=self.default_slider_width, command=lambda x: GUIInputManager.update_qty(self, product, x))
        slider_data = {"widget": slider, "x": x1, "y": y2,  "length": slider.cget("length")}
        self.sliders.append(slider_data)
        slider.place(in_=self.canvas, x=x1, y=y2)
        slider.update_value(qty)
        slider.rect = item_id

        group_tag = f"group_{item_id}"
        self.canvas.addtag_withtag(group_tag, item_id)
        self.canvas.addtag_withtag(group_tag, text_item)
        self.canvas.addtag_withtag(group_tag, text_id)

        self.canvas.tag_bind(item_id, "<ButtonPress-1>", self.on_start_drag)
        self.canvas.tag_bind(item_id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item_id, "<ButtonRelease-1>", self.on_stop_drag)
        self.canvas.tag_bind(item_id, "<Button-3>", self.show_product_context_menu)

        self.canvas.tag_bind(group_tag, "<B1-Motion>", lambda event: self.move_slider(event, slider, slider_data))

        return item_id

        # self.tooltips[prc] = Tooltip(self.canvas, f"This is a process")

    def show_product_context_menu(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Set Impacts", command=lambda: self.set_impacts(item, product=True))
        self.context_menu.add_command(label="View Unit Impacts", command=lambda: self.view_impacts(item, product=True))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Change life cycle stage", command=lambda: self.update_life_cycle_stage(item, product=True))
        self.context_menu.post(event.x_root, event.y_root)

