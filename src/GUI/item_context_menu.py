from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup

from tkinter import Menu, BooleanVar

import gc

class ItemContextMenuMixin:

    # =================================
    # Item Context Menu
    # =================================

    @classmethod
    def show_context_menu(cls, master, event, slider):

        if master.shift_pressed:
            master.highlight_dependents(event)
        else:
            item = master.current_canvas.find_closest(event.x, event.y)[0]
            if "item" in master.current_canvas.gettags(item):  
                model_id = master.get_current_model() 
                master.context_menu = Menu(master, tearoff=0)
                master.context_menu.add_command(label="Edit LCA data", command=lambda: cls.set_impacts(master, item))
                master.context_menu.add_command(label="View unit impacts", command=lambda: cls.view_impacts(master,item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Edit name", command=lambda: cls.edit_name(master,item))
                master.context_menu.add_command(label="Change quantity", command=lambda: cls.change_qty(master,item))
                master.context_menu.add_command(label="Change units", command=lambda: cls.change_unit(master,item))
                master.context_menu.add_command(label="Change life cycle stage", command=lambda: cls.update_life_cycle_stage(master,item))
                if GUIInputManager.is_product(master.item_map[model_id][item]):
                    master.context_menu.add_command(label="Set density", command=lambda: cls.set_product_density(master, item))            
                master.context_menu.add_separator()

                slider_menu = Menu(master.context_menu, tearoff=False)
                slider_on = BooleanVar(value=slider._always_on)
                slider_menu.add_radiobutton(label="On", variable=slider_on, value=True, command= lambda: cls.set_slider_state(master, item, status='on'))
                slider_menu.add_radiobutton(label="Off", variable=slider_on, value=False, command= lambda: cls.set_slider_state(master, item, status='off'))
                slider_menu.add_separator()
                slider_menu.add_command(label="Set slider properties", command=lambda: cls.set_slider_properties(master,item))
                master.context_menu.add_cascade(menu=slider_menu, label='Quantity slider')

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

        model_id = master.get_current_model()
        cmd = lambda: GUIInputManager.set_impact_data(master, master.item_map[model_id][item], impact.get())

        popup = Popup(master, "Set Impacts", "300x200")

        if not GUIInputManager.get_database_data(master.project).empty:
            impact = Popup._popup_input_combo(popup, "Impact : ", GUIInputManager.get_database_data(master.project)['Flow'].tolist())
            
            Popup.button_custom(popup, "Add custom impact", cmd= lambda: master.add_custom_item(master))

            Popup.button_pack_OKCancel(popup, popup, cmd)
        else:
            label = Popup._popup_label(popup, "Impact database not loaded.\nGo to Database menu and import database.", justify='left')
            label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))

            Popup.button_custom(popup, "Add custom impact", cmd= lambda: master.add_custom_item(master))

            Popup.button_pack_Close(popup, popup)


    @classmethod
    def view_impacts(cls, master, item):

        popup = Popup(master, "View Impacts", "300x200")

        model_id = master.get_current_model()
        row = GUIInputManager.get_database_row(master.item_map[model_id][item])

        if row is not None:
            impact_data = GUIInputManager.get_impact_data(master.project, row)
            data_list = [row]
            for impact in master.impact_categories:
                data_list.append(impact_data[impact]) 
        else:
            data_list = ["unasigned", 0.0, 0.0, 0.0, 0.0, 0.0]

        text_str = "{0} \n GWP : {1:.2f} kg CO2 eq \n Acidification potential : {2:.2f} kg SO2 eq \n Eutrophication potential : {3:.2f} kg N eq \n Ozone depletion potential : {4:.2f} kg CFC-11 eq\n Smog potential : {5:.2f} kg O3 eq".format(*data_list)        
        Popup._popup_label(popup, text_str, justify='left')

        Popup.button_pack_Close(popup, popup)

    @classmethod
    def update_life_cycle_stage(cls, master, item_id):
        
        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]

        popup = Popup(master, "Update life cycle stage", "300x200")
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"])

        _cmd = lambda: GUIInputManager.update_life_cycle_stage(master, item, life_cycle_stage.get())
        cmd = lambda: cls._on_update(master,item_id, _cmd)

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def edit_name(cls, master, item_id):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]

        popup = Popup(master, "Edit name", "300x200")
        name = Popup._popup_input_field(popup, "Name: ", default_val=GUIInputManager.get_name(item)) 

        _cmd = lambda: GUIInputManager.edit_name(master, item, name.get()) 
        cmd = lambda: cls._on_update(master, item_id, _cmd)

        Popup.button_pack_OKCancel(popup, popup, cmd)


    @classmethod
    def change_qty(cls, master, item_id):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]

        popup = Popup(master, "Change quantity", "300x200")
        qty = Popup._popup_input_field(popup, f"Qty (in {GUIInputManager.get_unit(item)}): ", validate_num=True, default_val=GUIInputManager.get_qty(item)) 

        _cmd = lambda: GUIInputManager.update_qty(master, item, qty.get()) 
        cmd = lambda: cls._on_update(master, item_id, _cmd, update_slider=True)

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _on_update(cls, master, item_id, cmd, update_slider=False):

        cmd()
        ItemContextMenuMixin._update_label(master, item_id, update_slider)

    
    @staticmethod
    def _update_label(master, item_id, update_slider=False):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]
        slider = master.slider_map[model_id][item_id]

        text_str = GUIInputManager.get_name(item) + '\n' + GUIInputManager.get_stage(item)
        if not slider._always_on:
            text_str += '\n' + str(GUIInputManager.get_qty(item)) + ' ' + GUIInputManager.get_unit(item)
        if update_slider:
            slider.update_value(GUIInputManager.get_qty(item))
        text_item = master.label_map[item_id]
        master.current_canvas.itemconfig(text_item, text=text_str)

    @classmethod
    def change_unit(cls, master, item_id):

        popup = Popup(master, "Change units", "300x200")

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]

        unit_list = GUIInputManager.get_all_units_list(master.project)
        default_entry = unit_list.index(GUIInputManager.get_unit(item))
        unit = Popup._popup_input_combo(popup, "units: ", unit_list, default_entry=default_entry) # TODO: Units to match current units

        cmd = lambda: cls._update_slider_label(master, item_id, unit.get(), unit_list[default_entry])

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def set_product_density(cls, master, item_id):

        popup = Popup(master, "Set density", "300x250")
        
        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]

        weight_units = ["kg", "lb", "g", "t"]
        default_unit =  weight_units.index(GUIInputManager.get_weight_unit(item))
        density =  Popup._popup_input_field(popup, "Weight per unit product: ", validate_num=True, default_val=GUIInputManager.get_density(item))     
        weight_unit =  Popup._popup_input_combo(popup, "Weight unit: ", weight_units, default_entry=default_unit) 

        cmd = lambda :GUIInputManager.set_density(master, item, density.get(), weight_unit.get()) 
        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def _update_slider_label(cls, master, item_id, new_unit, old_unit):

        model_id = master.get_current_model()
        item = master.item_map[model_id][item_id]
        
        GUIInputManager.change_unit(master, item, new_unit)

        master.sliders[model_id][item_id]["widget"].update_value(GUIInputManager.get_qty(item))
        master.slider_map[model_id][item_id].config(label= "Qty (in {})".format(GUIInputManager.get_unit(item)))

    @classmethod
    def set_slider_properties(cls, master, item):
                
        popup = Popup(master, "Set slider properties", "300x200")

        model_id = master.get_current_model()
        slider = master.slider_map[model_id][item]
        
        qty_min = Popup._popup_input_field(popup, "qty slider min: ", validate_num=True, default_val=slider.cget("from"))
        qty_max = Popup._popup_input_field(popup, "qty slider max: ", validate_num=True, default_val=slider.cget("to"))
        qty_reolution = Popup._popup_input_field(popup, "qty slider resolution: ", validate_num=True, default_val=slider.cget("resolution"))

        cmd = lambda: slider.update_slider(qty_min.get(), qty_max.get(), qty_reolution.get())

        Popup.button_pack_OKCancel(popup, popup, cmd)

    @classmethod
    def set_slider_state(cls, master, item, status='off'):

        model_id = master.get_current_model()
        slider = master.slider_map[model_id][item]

        if status == 'off':
            slider._always_on = False
            slider.hide_slider(None)
        elif status == 'on':
            slider._never_show = False
            slider._always_on = True
            slider.show_slider(None) 
        else:
            raise ValueError("Slider status should be either 'on' or 'off'.")              
    

    @classmethod
    def delete_item(cls, master, item):

        model_id = master.get_current_model()

        GUIInputManager.delete(master, master.item_map[model_id][item])
        del master.item_map[model_id][item]

        master.sliders[model_id][item]["widget"].destroy()
        del master.sliders[model_id][item]
        group_tag = f"group_{item}"
        master.current_canvas.delete(group_tag)

        for connector in master.connectors[model_id][:]:
            if (connector["start_item"] == item) or (connector["end_item"] == item):
                master.current_canvas.delete(connector["line"])
                master.connectors[model_id].remove(connector)

        # cehck relationships and dependents
        if item in master.relationships[model_id]:
            del master.relationships[model_id][item]

        del_keys = []
        for dep in master.dependents[model_id]:
            if item in master.dependents[model_id][dep]:
                master.dependents[model_id][dep].remove(item)
                if len(master.dependents[model_id][dep]) == 0:
                    del_keys.append(dep)

        for key in del_keys:
            del master.dependents[model_id][key]

        gc.collect()


