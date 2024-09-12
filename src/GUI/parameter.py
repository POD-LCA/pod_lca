from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider
from GUI.item import Item

from numpy import ceil, power, log10
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

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Parameter.create_canvas_item(self, name, '', start, height, width, self.color_parameter, tags=["parameter"])
        slider, slider_data = Parameter.create_slider(self, start, height, width, None, qty, units, item_id, slider_min, slider_max, resolution, parameter=True)
        Parameter.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        self.item_map[item_id] = None

        popup.destroy()

    @staticmethod
    def show_context_menu(master, event, slider):

        if master.shift_pressed:
            master.highlight_dependents(event)
        else:
            item = master.canvas.find_closest(event.x, event.y)[0]
            if "parameter" in master.canvas.gettags(item):   
                master.context_menu = Menu(master, tearoff=0)
                master.context_menu.add_command(label="Edit name", command=lambda: Parameter.edit_name(master,item))
                master.context_menu.add_command(label="Change units", command=lambda: Parameter.change_units(master,item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Set slider properties", command=lambda: Parameter.set_slider_properties(master,item))
                master.context_menu.add_separator()
                relationships_menu = Menu(master, tearoff=False)
                master.context_menu.add_cascade(menu=relationships_menu, label="Relationships")
                relationships_menu.add_command(label="Set relationship", command=lambda: master.set_relationship(item, slider))
                relationships_menu.add_command(label="Clear relationship", command=lambda: master.clear_relationship(item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Delete", command=lambda: Parameter.delete_item(master, item))
                master.context_menu.post(event.x_root, event.y_root)  

    @classmethod
    def edit_name(cls, master, item_id):
        
        pass

        # item = master.item_map[item_id]

        # popup = Popup(master, "Edit name", "300x200")
        # name = popup._popup_input_field("Process name: ", default_val=GUIInputManager.get_name(item)) 

        # _cmd = lambda: GUIInputManager.edit_name(master, item, name.get()) 
        # cmd = lambda: cls._update_label(master, item_id, _cmd)

        # button_frame = Frame(popup)
        # button_frame.pack(pady=20)

        # ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        # ok_button.pack(side=LEFT, padx=10)

        # cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        # cancel_button.pack(side=LEFT, padx=10)

    def restore_parameter(self, item, cords):

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
