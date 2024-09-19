from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup


from tkinter import Menu

import gc

class ItemContextMenu:

    # =================================
    # Item Context Menu
    # =================================

    @classmethod
    def show_context_menu(cls, master, event, slider):

        if master.shift_pressed:
            master.highlight_dependents(event)
        else:
            item = master.canvas.find_closest(event.x, event.y)[0]
            if "item" in master.canvas.gettags(item):   
                master.context_menu = Menu(master, tearoff=0)
                master.context_menu.add_command(label="Set impacts", command=lambda: cls.set_impacts(master, item))
                master.context_menu.add_command(label="View unit impacts", command=lambda: cls.view_impacts(master,item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Edit name", command=lambda: cls.edit_name(master,item))
                master.context_menu.add_command(label="Change units", command=lambda: cls.change_unit(master,item))
                master.context_menu.add_command(label="Change life cycle stage", command=lambda: cls.update_life_cycle_stage(master,item))
                if GUIInputManager.is_fuel(master.item_map[item]):
                    master.context_menu.add_command(label="Set density", command=lambda: cls.set_product_density(master, item))            
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Set slider properties", command=lambda: cls.set_slider_properties(master,item))
                master.context_menu.add_separator()
                relationships_menu = Menu(master, tearoff=False)
                master.context_menu.add_cascade(menu=relationships_menu, label="Relationships")
                relationships_menu.add_command(label="Set relationship", command=lambda: master.set_relationship(item, slider))
                relationships_menu.add_command(label="Clear relationship", command=lambda: master.clear_relationship(item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Delete", command=lambda: cls.delete_item(master, item))
                master.context_menu.post(event.x_root, event.y_root)  

    @classmethod
    def set_impacts(cls, master, item):

        cmd = lambda: GUIInputManager.set_impact_data(master, master.item_map[item], impact.get())

        popup = Popup(master, "Set Impacts", "300x200")

        if not GUIInputManager.get_database_data(master.project) is None:
            impact = Popup._popup_input_combo(popup, "Impact : ", GUIInputManager.get_database_data(master.project)['Flow'].tolist())
            
            Popup.button_pack_OKCancel(popup, popup, cmd)
        else:
            label = Popup._popup_label(popup, "Impact database not loaded.\nGo to Database menu and import database.", justify='left')
            label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))

            Popup.button_pack_Close(popup, popup)


    @classmethod
    def view_impacts(cls, master, item):

        popup = Popup(master, "View Impacts", "300x200")

        row = GUIInputManager.get_database_row(master.item_map[item])

        if row is not None:
            impact_data = GUIInputManager.get_impact_data(master.project, row)
            data_list = row, impact_data["Global warming potential (kg CO2 eq)"], impact_data["Acidification potential (kg SO2 eq)"], impact_data["Eutrophication potential (kg N eq)"], impact_data["Ozone depletion potential (kg CFC-11 eq)"], impact_data["Smog potential (kg O3 eq)"]
        else:
            data_list = "unasigned", 0.0, 0.0, 0.0, 0.0, 0.0

        text_str = "{0} \n GWP : {1:.2f} kg CO2 eq \n Acidification potential : {2:.2f} kg SO2 eq \n Eutrophication potential : {3:.2f} kg N eq \n Ozone depletion potential : {4:.2f} kg CFC-11 eq\n Smog potential : {5:.2f} kg O3 eq".format(*data_list)        
        Popup._popup_label(popup, text_str, justify='left')

        Popup.button_pack_Close(popup, popup)

    @classmethod
    def update_life_cycle_stage(cls, master, item_id):
        
        item = master.item_map[item_id]

        popup = Popup(master, "Update life cycle stage", "300x200")
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"])

        _cmd = lambda: GUIInputManager.update_life_cycle_stage(master, item, life_cycle_stage.get())
        cmd = lambda: cls._update_label(master,item_id, _cmd)

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def edit_name(cls, master, item_id):

        item = master.item_map[item_id]

        popup = Popup(master, "Edit name", "300x200")
        name = Popup._popup_input_field(popup, "Name: ", default_val=GUIInputManager.get_name(item)) 

        _cmd = lambda: GUIInputManager.edit_name(master, item, name.get()) 
        cmd = lambda: cls._update_label(master, item_id, _cmd)

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_label(cls, master, item_id, cmd):

        item = master.item_map[item_id]
        cmd()

        text_str = GUIInputManager.get_name(item) + '\n' + GUIInputManager.get_stage(item)
        text_item = master.label_map[item_id]
        master.canvas.itemconfig(text_item, text=text_str)

    @classmethod
    def change_unit(cls, master, item_id):

        popup = Popup(master, "Change units", "300x200")
        item = master.item_map[item_id]

        unit_list = GUIInputManager.get_all_units_list(master.project)
        default_entry = unit_list.index(GUIInputManager.get_unit(item))
        unit = Popup._popup_input_combo(popup, "units: ", unit_list, default_entry=default_entry) # TODO: Units to match current units

        cmd = lambda: cls._update_slider_label(master, item_id, unit.get(), unit_list[default_entry])

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def set_product_density(cls, master, item_id):

        popup = Popup(master, "Set density", "300x250")

        item = master.item_map[item_id]

        density =  Popup._popup_input_field(popup, "Weight per unit product: ", default_val=1.0)     
        weight_unit =  Popup._popup_input_combo(popup, "Weight unit: ", ["kg", "lb", "g", "t"]) 

        cmd = lambda :GUIInputManager.set_density(master, item, density.get(), weight_unit.get()) 
        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_slider_label(cls, master, item_id, new_unit, old_unit):

        item = master.item_map[item_id]
        GUIInputManager.set_unit(item, new_unit)

        conversion_factor = GUIInputManager.unit_conversion(master.project, old_unit, new_unit)
        if conversion_factor is not None:
            master.slider_map[item_id]
            old_val = master.sliders[item_id]["widget"].get()
            new_val = old_val * conversion_factor

            GUIInputManager.update_qty(master, item, new_val)

            master.sliders[item_id]["widget"].update_value(new_val)

        master.slider_map[item_id].config(label= "Qty (in {})".format(new_unit))

    @classmethod
    def set_slider_properties(cls, master, item):
                
        popup = Popup(master, "Set slider properties", "300x200")

        slider = master.slider_map[item]
        
        qty_min = Popup._popup_input_field(popup, "qty slider min: ", validate_num=True, default_val=slider.cget("from"))
        qty_max = Popup._popup_input_field(popup, "qty slider max: ", validate_num=True, default_val=slider.cget("to"))
        qty_reolution = Popup._popup_input_field(popup, "qty slider resolution: ", validate_num=True, default_val=slider.cget("resolution"))

        cmd = lambda: slider.update_slider(qty_min.get(), qty_max.get(), qty_reolution.get())

        Popup.button_pack_OKCancel(popup, popup, cmd)
    

    @classmethod
    def delete_item(cls, master, item):

        GUIInputManager.delete(master, master.item_map[item])
        del master.item_map[item]

        master.sliders[item]["widget"].destroy()
        del master.sliders[item]
        group_tag = f"group_{item}"
        master.canvas.delete(group_tag)

        for connector in master.connectors[:]:
            if (connector["start_item"] == item) or (connector["end_item"] == item):
                master.canvas.delete(connector["line"])
                master.connectors.remove(connector)

        gc.collect()


