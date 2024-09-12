from GUI.GUI_inputManager import GUIInputManager
from GUI.slider import Slider

import gc

from tkinter import Menu
from tkinter import LEFT

class Item:

    # =================================
    # Canvas Item Methods
    # =================================

    @staticmethod
    def create_canvas_item(master, name, stage, start, height, width, color, tags):


        x1, y1, x2, y2 = start[0], start[1], start[0] + width*master.scale, start[1] + height*master.scale

        item_id = master.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=master.outline_color, width=master.outline_width,
                                                 tags=tags)

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = master.canvas.create_text(text_x, text_y, text=text_str)

        master.label_map[item_id] = text_item

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = master.canvas.create_text(id_x, id_y, text=str(item_id))

        return item_id, text_item, text_id
    
    def create_slider(master, start, height, width, item, qty, units, item_id, slider_min=0, slider_max=100, resolution=0.1, transport=False):

        x, y = start[0], start[1] + height*master.scale
        
        if transport: 
            cmd = lambda x: GUIInputManager.update_transport_dist(master, item, x)
        else:
            cmd = lambda x: GUIInputManager.update_qty(master, item, x)

        slider = Slider(master.canvas, "Qty (in {})".format(units), min=slider_min, max=slider_max, resolution=resolution, width=master.default_slider_width*master.scale, length= width*master.scale, command=cmd)
        slider_data = {"widget": slider, "x": x, "y": y, "length": slider.cget("length")}
        master.sliders[item_id] = slider_data
        slider.place(in_=master.canvas, x=x, y=y)
        slider.update_value(qty)
        slider.rect = item_id

        master.slider_map[item_id] = slider

        return slider, slider_data
    
    def item_bind(master, item_id, text_item, text_id, slider, slider_data):

        group_tag = f"group_{item_id}"
        master.canvas.addtag_withtag(group_tag, item_id)
        master.canvas.addtag_withtag(group_tag, text_item)
        master.canvas.addtag_withtag(group_tag, text_id)

        master.canvas.tag_bind(item_id, "<ButtonPress-1>", master.on_start_drag)
        master.canvas.tag_bind(item_id, "<B1-Motion>", master.on_drag)
        master.canvas.tag_bind(item_id, "<ButtonRelease-1>", master.on_stop_drag)
        master.canvas.tag_bind(item_id, "<Button-3>", lambda event: Item.show_context_menu(master, event, slider))
        master.canvas.tag_bind(item_id, "<ButtonRelease-3>", master.remove_highight)

        master.canvas.tag_bind(group_tag, "<B1-Motion>", lambda event: master.move_slider(event, slider, slider_data))

    @staticmethod
    def show_context_menu(master, event, slider):

        if master.shift_pressed:
            master.highlight_dependents(event)
        else:
            item = master.canvas.find_closest(event.x, event.y)[0]
            if "process" in master.canvas.gettags(item) or "product" in master.canvas.gettags(item):   
                master.context_menu = Menu(master, tearoff=0)
                master.context_menu.add_command(label="Set impacts", command=lambda: master.set_impacts(item))
                master.context_menu.add_command(label="View unit impacts", command=lambda: master.view_impacts(item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Edit name", command=lambda: master.edit_name(item))
                master.context_menu.add_command(label="Change units", command=lambda: master.change_units(item))
                master.context_menu.add_command(label="Change life cycle stage", command=lambda: master.update_life_cycle_stage(item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Set slider properties", command=lambda: master.set_slider_properties(item))
                master.context_menu.add_separator()
                relationships_menu = Menu(master, tearoff=False)
                master.context_menu.add_cascade(menu=relationships_menu, label="Relationships")
                relationships_menu.add_command(label="Set relationship", command=lambda: master.set_relationship(item, slider))
                relationships_menu.add_command(label="Clear relationship", command=lambda: master.clear_relationship(item))
                master.context_menu.add_separator()
                master.context_menu.add_command(label="Delete", command=lambda: Item.delete_item(master, item))
                master.context_menu.post(event.x_root, event.y_root)

    @staticmethod
    def restore_item(master, item, cords, color, tags, transport=False):
        
        x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        start = [x1, y1]
        height = abs(y2-y1)
        width = abs(x2-x1)

        name = GUIInputManager.get_name(item)
        units = GUIInputManager.get_unit(item)
        stage = GUIInputManager.get_stage(item)
        qty = GUIInputManager.get_travel_distance(item) if GUIInputManager.is_transport(item) else GUIInputManager.get_qty(item)

        item_id, text_item, text_id = Item.create_canvas_item(master, name, stage, start, height, width, color, tags)
        slider, slider_data = Item.create_slider(master, start, height, width, item, qty, units, item_id, transport)
        Item.item_bind(master, item_id, text_item, text_id, slider, slider_data)

        master.item_map[item_id] = item

        return item_id
    
    @staticmethod
    def delete_item(master, item):

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

    @staticmethod
    def item_from_id(master, id):

        if id in master.product_data:
            return master.product_data[id]
        elif id in master.process_data:
            return master.process_data[id]
    
        