from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.item import Item

import gc

from numpy import ceil, power, log10
from tkinter import Menu

class ParamObj:

    # =================================
    # Parameter Objects
    # =================================

    def __init__(self, name, qty, unit):
        self.id = None
        self.name = name
        self.qty = qty
        self.unit = unit

    def update_qty(self, master, qty):

        self.qty = qty
        master.update_dependent_qtys(self, qty)
    
    def edit_name(self, name):
        
        self.name = name

    def set_unit(self, unit):

        self.unit = unit

    def set_id(self, id):

        self.id = id

    def get_name(self):
    
        return self.name
    
    def get_unit(self):

        return self.unit

    def get_id(self):
        
        return self.id
    
    def get_qty(self):

        return self.qty



class Parameter(Item):

    # =================================
    # Parameter Items
    # =================================

    def open_popup_parameter(self):

        popup = Popup(self, "Parameter", "300x200")
        
        name =  Popup._popup_input_field(popup, "Parameter name: ", default_val="new Parameter")   
        qty = Popup._popup_input_field(popup, "qty: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["m3", "kg", "unit"])  

        cmd = lambda: self.create_parameter(popup, name.get(), qty.get(), units.get())
        Popup.button_pack_OKCancel(popup, popup, cmd)
        
    def create_parameter(self, popup, name, qty, unit):

        start = [50, 50]
        height = 50
        width = 100
        model_id = self.get_current_model()

        param = ParamObj(name, qty, unit)
        slider_cmd = lambda x: param.update_qty(self, x)

        slider_min = 0.0
        slider_max = power(10,ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
        resolution = (slider_max - slider_min) / 100

        item_id, text_item, text_id = Parameter.create_canvas_item(self, model_id, name, '', start, height, width, self.color_parameter, tags=["parameter"])
        slider, slider_data = Parameter.create_slider(self, model_id, start, height, width, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution)
        Parameter.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        self.item_map[model_id][item_id] = param
        param.set_id(item_id)

        popup.destroy()

    @classmethod
    def show_context_menu(cls, master, event, slider):

        if master.shift_pressed:
            master.highlight_dependents(event)
        else:
            item = master.current_canvas.find_closest(event.x, event.y)[0]
            if "parameter" in master.current_canvas.gettags(item):   
                master.context_menu = Menu(master, tearoff=0)
                master.context_menu.add_command(label="Edit name", command=lambda: Parameter.edit_name(master,item))
                master.context_menu.add_command(label="Change units", command=lambda: Parameter.change_unit(master,item))
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

        model_id = master.get_current_model()
        param = master.item_map[model_id][item_id]

        popup = Popup(master, "Edit name", "300x200")
        name = Popup._popup_input_field(popup, "Item name: ", default_val=param.get_name()) 

        _cmd = lambda: param.edit_name(name.get()) 
        cmd = lambda: cls._update_label(master, item_id, _cmd)
        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_label(cls, master, item_id, cmd):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]
        cmd()

        text_str = GUIInputManager.get_name(item)
        text_item = master.label_map[item_id]
        master.current_canvas.itemconfig(text_item, text=text_str)

    @classmethod
    def change_unit(cls, master, item_id):

        model_id = master.get_current_model()
        popup = Popup(master, "Change units", "300x200")
        item = master.item_map[model_id][item_id]

        unit_list = ["m3", "kg", "lb", "MJ", "km", "mi"]
        default_entry = unit_list.index(item.get_unit())
        unit = Popup._popup_input_combo(popup, "units: ", unit_list, default_entry=default_entry) # TODO: Units to match current units

        cmd = lambda: cls._update_slider_label(master, item_id, unit.get(), unit_list[default_entry])
        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_slider_label(cls, master, item_id, new_unit, old_unit):

        model_id = master.get_current_model()
        param = master.item_map[model_id][item_id]
        param.set_unit(new_unit)

        conversion_factor = GUIInputManager.unit_conversion(master.project, old_unit, new_unit)
        if conversion_factor is not None:
            master.slider_map[model_id][item_id]
            old_val = master.sliders[model_id][item_id]["widget"].get()
            new_val = old_val * conversion_factor

            param.update_qty(master, new_val)

            master.sliders[item_id]["widget"].update_value(new_val)

        master.slider_map[model_id][item_id].config(label= "Qty (in {})".format(new_unit))


    @classmethod
    def delete_item(cls, master, item):

        model_id = master.get_current_model()
        del master.item_map[model_id][item]

        master.sliders[model_id][item]["widget"].destroy()
        del master.sliders[model_id][item]
        group_tag = f"group_{item}"
        master.current_canvas.delete(group_tag)

        for connector in master.connectors[model_id][:]:
            if (connector["start_item"] == item) or (connector["end_item"] == item):
                master.current_canvas.delete(connector["line"])
                master.connectors[model_id].remove(connector)

        gc.collect()

    def restore_parameter(self, model, param, cords):

        x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        start = [x1, y1]
        height = abs(y2-y1)
        width = abs(x2-x1)

        name = param.get_name()
        units = param.get_unit()
        qty = param.get_qty()

        slider_cmd = lambda x: param.update_qty(self, x)

        item_id, text_item, text_id = Item.create_canvas_item(self, model, name, '', start, height, width, self.color_parameter, tags=["parameter"])
        slider, slider_data = Item.create_slider(self, model, start, height, width, qty, units, item_id, slider_cmd)
        Item.item_bind(self, item_id, text_item, text_id, slider, slider_data)

        self.item_map[model][item_id] = param
        param.set_id(item_id)

        return item_id
