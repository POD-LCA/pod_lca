from ui.materials_screening_tool.GUI_inputManager import GUIInputManager
from ui.materials_screening_tool.slider import Slider
from ui.materials_screening_tool.item_context_menu import ItemContextMenuMixin

from tkinter import DISABLED


class Item(ItemContextMenuMixin):

    # =================================
    # Canvas Item Methods
    # =================================

    @classmethod
    def create_canvas_item(
        cls, master, model, name, stage, qty, unit, color, tags, start=None, height=None, width=None
    ):

        tags.append("item")
        start, height, width = Item._get_placement(master, model, tags, start, height, width)

        x1, y1, x2, y2 = (
            start[0],
            start[1],
            start[0] + width * master.scale[model],
            start[1] + height * master.scale[model],
        )

        item_id = master.current_canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline=master.outline_color, width=master.outline_width, tags=tuple(tags)
        )
        disp_num = len(master.item_disp_num[model]) + 1

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + "\n" + stage + "\n" + str(qty) + " " + unit
        text_item = master.current_canvas.create_text(text_x, text_y, text=text_str)

        master.label_map[item_id] = text_item
        master.item_disp_num[model][item_id] = disp_num
        master.disp_num_item[model][disp_num] = item_id

        id_pack = 5
        id_x, id_y = x1 + id_pack, y1 + id_pack
        text_id = master.current_canvas.create_text(id_x, id_y, text=str(disp_num))

        return item_id, text_item, text_id

    @staticmethod
    def _get_placement(master, model, tags, start, height, width):

        height = 100 if height is None else height
        width = 100 if width is None else width

        no_params = len(master.current_canvas.find_withtag("parameter"))
        no_product = len(master.current_canvas.find_withtag("product"))
        no_transportation = len(master.current_canvas.find_withtag("transportation"))
        no_process = len(master.current_canvas.find_withtag("process"))
        no_energy = len(master.current_canvas.find_withtag("energy"))
        no_waste = len(master.current_canvas.find_withtag("waste"))
        no_emission = len(master.current_canvas.find_withtag("emission"))

        k = 50
        if "parameter" in tags:
            s_x = 0
            s_y = k + no_params * (height + k)
        elif "transportation" in tags:
            s_x = 4 * width
            s_y = k + no_transportation * (height + k)
        elif "process" in tags:
            s_x = 6 * width
            s_y = k + (no_process - no_transportation) * (height + k)
        elif "energy" in tags:
            s_x = 5 * width + k
            s_y = 50 + (1.5 + no_energy) * (height + k)
        elif "waste" in tags or "emission" in tags:
            s_x = 8 * width + k
            s_y = 50 + (no_waste + no_emission) * (height + k)
        elif "product" in tags:
            s_x = 2 * width
            s_y = k + (no_product - no_energy - no_waste - no_emission) * (height + k)
        else:
            raise NotImplementedError

        start = (
            [
                master.reference_point[model][0] + s_x * master.scale[model],
                master.reference_point[model][1] + s_y * master.scale[model],
            ]
            if start is None
            else start
        )

        return start, height, width

    @classmethod
    def create_slider(
        cls,
        master,
        model,
        qty,
        units,
        item_id,
        cmd,
        slider_min=0,
        slider_max=100,
        resolution=0.1,
        start=None,
        height=None,
        width=None,
    ):

        no_items = len(master.current_canvas.find_withtag("item"))
        height = 100 if height is None else height
        width = 100 if width is None else width
        start = [50 + no_items * width, 50 + no_items * height] if start is None else start
        x, y = start[0], start[1] + height * master.scale[model]

        slider = Slider(
            master.current_canvas,
            "Qty (in {})".format(units),
            min=slider_min,
            max=slider_max,
            resolution=resolution,
            width=master.default_slider_width * master.scale[model],
            length=width * master.scale[model],
            command=cmd,
        )
        slider_data = {"widget": slider, "x": x, "y": y, "length": slider.cget("length")}
        master.sliders[model][item_id] = slider_data
        slider.temp_in_, slider.temp_x, slider.temp_y = master.current_canvas, x, y
        slider.update_value(qty)
        slider.rect = item_id

        master.slider_map[model][item_id] = slider

        slider.bind("<Enter>", slider.show_slider)
        slider.bind("<Leave>", slider.hide_slider)

        return slider, slider_data

    @classmethod
    def update_qty(cls, master, item_id, qty):

        model_id = master.get_current_model()
        product = master.item_map[model_id][item_id]

        cmd = lambda: GUIInputManager.update_qty(master, product, qty)
        cls._on_update(master, item_id, cmd, update_slider=False)

    @classmethod
    def item_bind(cls, master, item_id, text_item, text_id, slider, slider_data):

        group_tag = f"group_{item_id}"
        master.current_canvas.addtag_withtag(group_tag, item_id)
        master.current_canvas.addtag_withtag(group_tag, text_item)
        master.current_canvas.addtag_withtag(group_tag, text_id)

        master.current_canvas.tag_bind(item_id, "<ButtonPress-1>", master.on_start_drag)
        master.current_canvas.tag_bind(item_id, "<B1-Motion>", master.on_drag)
        master.current_canvas.tag_bind(item_id, "<ButtonRelease-1>", master.on_stop_drag)
        master.current_canvas.tag_bind(
            item_id, "<Button-3>", lambda event: cls.show_context_menu(master, event, slider)
        )
        master.current_canvas.tag_bind(item_id, "<ButtonRelease-3>", master.remove_highight)

        master.current_canvas.tag_bind(
            group_tag, "<B1-Motion>", lambda event: master.move_slider(event, slider, slider_data)
        )

        master.current_canvas.tag_bind(group_tag, "<Enter>", slider.show_slider)
        master.current_canvas.tag_bind(group_tag, "<Leave>", slider.hide_slider)

    @classmethod
    def restore_item(cls, master, model, item, cords, color, tags, slider_cmd):

        x1, y1, x2, y2 = cords[0], cords[1], cords[2], cords[3]
        start = [x1, y1]
        height = abs(y2 - y1)
        width = abs(x2 - x1)

        name = GUIInputManager.get_name(item)
        unit = GUIInputManager.get_unit(item)
        stage = GUIInputManager.get_stage(item)
        qty = (
            GUIInputManager.get_travel_distance(item)
            if GUIInputManager.is_transport(item)
            else GUIInputManager.get_qty(item)
        )

        item_id, text_item, text_id = cls.create_canvas_item(
            master, model, name, stage, qty, unit, color, tags, start=start, height=height, width=width
        )
        slider, slider_data = cls.create_slider(
            master, model, qty, unit, item_id, slider_cmd, start=start, height=height, width=width
        )
        cls.item_bind(master, item_id, text_item, text_id, slider, slider_data)

        dependents_all = [item for sublist in master.dependents[model].values() for item in sublist]
        if item_id in dependents_all:
            slider.config(state=DISABLED)

        master.item_map[model][item_id] = item
        GUIInputManager.set_id(item, item_id)

        return item_id
