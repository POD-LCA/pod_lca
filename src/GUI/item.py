from GUI.GUI_inputManager import GUIInputManager
from GUI.slider import Slider
from GUI.item_context_menu import ItemContextMenu

class Item(ItemContextMenu):

    # =================================
    # Canvas Item Methods
    # =================================

    @classmethod
    def create_canvas_item(cls, master, name, stage, start, height, width, color, tags):

        tags.append("item")
        x1, y1, x2, y2 = start[0], start[1], start[0] + width*master.scale, start[1] + height*master.scale

        item_id = master.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=master.outline_color, width=master.outline_width,
                                                 tags=tuple(tags))

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = master.canvas.create_text(text_x, text_y, text=text_str)

        master.label_map[item_id] = text_item

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = master.canvas.create_text(id_x, id_y, text=str(item_id))

        return item_id, text_item, text_id
    
    @classmethod 
    def create_slider(cls, master, start, height, width, qty, units, item_id, cmd,
                      slider_min=0, slider_max=100, resolution=0.1):

        x, y = start[0], start[1] + height*master.scale

        slider = Slider(master.canvas, "Qty (in {})".format(units), min=slider_min, max=slider_max, resolution=resolution, width=master.default_slider_width*master.scale, length= width*master.scale, command=cmd)
        slider_data = {"widget": slider, "x": x, "y": y, "length": slider.cget("length")}
        master.sliders[item_id] = slider_data
        slider.place(in_=master.canvas, x=x, y=y)
        slider.update_value(qty)
        slider.rect = item_id

        master.slider_map[item_id] = slider

        return slider, slider_data
    
    @classmethod
    def item_bind(cls, master, item_id, text_item, text_id, slider, slider_data):

        group_tag = f"group_{item_id}"
        master.canvas.addtag_withtag(group_tag, item_id)
        master.canvas.addtag_withtag(group_tag, text_item)
        master.canvas.addtag_withtag(group_tag, text_id)

        master.canvas.tag_bind(item_id, "<ButtonPress-1>", master.on_start_drag)
        master.canvas.tag_bind(item_id, "<B1-Motion>", master.on_drag)
        master.canvas.tag_bind(item_id, "<ButtonRelease-1>", master.on_stop_drag)
        master.canvas.tag_bind(item_id, "<Button-3>", lambda event: cls.show_context_menu(master, event, slider))
        master.canvas.tag_bind(item_id, "<ButtonRelease-3>", master.remove_highight)

        master.canvas.tag_bind(group_tag, "<B1-Motion>", lambda event: master.move_slider(event, slider, slider_data))

    @classmethod
    def restore_item(cls, master, item, cords, color, tags, slider_cmd):
        
        x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        start = [x1, y1]
        height = abs(y2-y1)
        width = abs(x2-x1)

        name = GUIInputManager.get_name(item)
        units = GUIInputManager.get_unit(item)
        stage = GUIInputManager.get_stage(item)
        qty = GUIInputManager.get_travel_distance(item) if GUIInputManager.is_transport(item) else GUIInputManager.get_qty(item)
        
        item_id, text_item, text_id = cls.create_canvas_item(master, name, stage, start, height, width, color, tags)
        slider, slider_data = cls.create_slider(master, start, height, width, qty, units, item_id, slider_cmd)
        cls.item_bind(master, item_id, text_item, text_id, slider, slider_data)

        master.item_map[item_id] = item
        GUIInputManager.set_id(item, item_id)

        return item_id

        