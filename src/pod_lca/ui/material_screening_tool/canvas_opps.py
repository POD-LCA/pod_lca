from tkinter import Canvas


class CanvasOperationsMixin:

    def get_current_model(self):

        current_tab_index = self.notebook.index("current")
        id_tag = "Model_" + str(current_tab_index)

        return id_tag

    def get_canvas_from_tab(self, index):

        tab_id = self.notebook.tabs()[index]
        tab_widget = self.notebook.nametowidget(tab_id)

        for child in tab_widget.winfo_children():
            if isinstance(child, Canvas):
                return child
        return None

    def set_current_model(self, name):

        tab_id = int(name.replace("Model_", ""))

        self.notebook.select(tab_id)
        self.update()

        self.current_canvas = self.models[name]

        return name

    def get_current_canvas(self):

        model_id = self.get_current_model()

        return self.models[model_id]

    def reset_model(self, event):

        name = self.get_current_model()
        self.current_canvas = self.models[name]

        self.on_canvas_configure(event)

    def delete_canvas(self, name):

        tab_id = int(name.replace("Model_", ""))

        self.notebook.forget(tab_id)

        return name

    def get_number_of_canvases(self):

        return len(self.notebook.winfo_children())

    # =================================
    # On Canvas: Zoom and pan
    # =================================

    def start_pan(self, event):
        item = self.current_canvas.find_withtag("current")
        if not item:
            self.current_canvas.scan_mark(event.x, event.y)
            self.pan_start = (event.x, event.y)

            self.current_canvas.configure(scrollregion=self.current_canvas.bbox("all"))

    def do_pan(self, event):
        if self.pan_start:
            self.current_canvas.scan_dragto(event.x, event.y, gain=1)

            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]

            self.offset_x += dx
            self.offset_y += dy

            self.current_canvas.move("all", dx, dy)
            model_id = self.get_current_model()

            for item in self.sliders[model_id]:
                slider_data = self.sliders[model_id][item]
                slider = slider_data["widget"]

                current_x = slider_data["x"] + dx
                current_y = slider_data["y"] + dy

                if slider._always_on:
                    slider.place(x=current_x, y=current_y)
                slider.temp_x, slider.temp_y = current_x, current_y

                slider_data["x"] = current_x
                slider_data["y"] = current_y

            if self.canvas_grid:
                self.draw_grid()

            self.pan_start = (event.x, event.y)

            self.reference_point[model_id] = [
                self.reference_point[model_id][0] + dx,
                self.reference_point[model_id][1] + dy,
            ]

    def zoom(self, event):
        x = self.current_canvas.canvasx(event.x)
        y = self.current_canvas.canvasy(event.y)

        model_id = self.get_current_model()
        if event.delta > 0:
            self.current_canvas.scale("all", x, y, self.zoom_factor[model_id], self.zoom_factor[model_id])
            self.scale_widgets(self.zoom_factor[model_id])
            self.scale[model_id] *= self.zoom_factor[model_id]
            self.reference_point[model_id] = [
                x + (self.reference_point[model_id][0] - x) * self.zoom_factor[model_id],
                y + (self.reference_point[model_id][1] - y) * self.zoom_factor[model_id],
            ]
        elif event.delta < 0:
            self.current_canvas.scale("all", x, y, 1 / self.zoom_factor[model_id], 1 / self.zoom_factor[model_id])
            self.scale_widgets(1 / self.zoom_factor[model_id])
            self.scale[model_id] /= self.zoom_factor[model_id]
            self.reference_point[model_id] = [
                x + (self.reference_point[model_id][0] - x) / self.zoom_factor[model_id],
                y + (self.reference_point[model_id][1] - y) / self.zoom_factor[model_id],
            ]

        if self.canvas_grid:
            self.draw_grid()
        self.current_canvas.configure(scrollregion=self.current_canvas.bbox("all"))

    def zoom_in(self, event):
        model_id = self.get_current_model()
        x = self.winfo_pointerx() - self.current_canvas.winfo_rootx()
        y = self.winfo_pointery() - self.current_canvas.winfo_rooty()
        x = self.current_canvas.canvasx(x)
        y = self.current_canvas.canvasy(y)
        self.current_canvas.scale("all", x, y, self.zoom_factor[model_id], self.zoom_factor[model_id])
        self.scale_widgets(self.zoom_factor[model_id])
        self.scale[model_id] *= self.zoom_factor[model_id]

        if self.canvas_grid:
            self.draw_grid()
        self.current_canvas.configure(scrollregion=self.current_canvas.bbox("all"))
        self.reference_point[model_id] = [
            x + (self.reference_point[model_id][0] - x) * self.zoom_factor[model_id],
            y + (self.reference_point[model_id][1] - y) * self.zoom_factor[model_id],
        ]

    def zoom_out(self, event):
        model_id = self.get_current_model()
        x = self.winfo_pointerx() - self.current_canvas.winfo_rootx()
        y = self.winfo_pointery() - self.current_canvas.winfo_rooty()
        x = self.current_canvas.canvasx(x)
        y = self.current_canvas.canvasy(y)
        self.current_canvas.scale("all", x, y, 1 / self.zoom_factor[model_id], 1 / self.zoom_factor[model_id])
        self.scale_widgets(1 / self.zoom_factor[model_id])
        self.scale[model_id] /= self.zoom_factor[model_id]

        if self.canvas_grid:
            self.draw_grid()
        self.current_canvas.configure(scrollregion=self.current_canvas.bbox("all"))
        self.reference_point[model_id] = [
            x + (self.reference_point[model_id][0] - x) / self.zoom_factor[model_id],
            y + (self.reference_point[model_id][1] - y) / self.zoom_factor[model_id],
        ]

    def scale_widgets(self, factor):
        model_id = self.get_current_model()
        for item in self.sliders[model_id]:
            slider_data = self.sliders[model_id][item]
            slider = slider_data["widget"]

            new_length = slider_data["length"] * factor
            slider_data["length"] = new_length
            slider.config(length=int(new_length))

            coords = self.current_canvas.coords(slider.rect)
            if slider._always_on:
                slider.place(in_=self.current_canvas, x=coords[0], y=coords[3])
            slider.temp_x, slider.temp_y = coords[0], coords[3]

            slider_data["x"] = coords[0]
            slider_data["y"] = coords[3]

    def on_canvas_configure(self, event):
        self.draw_grid()

    def draw_grid(self):
        """Draws a grid that updates based on current scale and offset."""

        self.current_canvas.delete("grid")

        width = self.current_canvas.winfo_width()
        height = self.current_canvas.winfo_height()
        model_id = self.get_current_model()

        scaled_grid_size = int(self.canvas_grid_size * self.scale[model_id])

        start_x = self.offset_x % scaled_grid_size
        start_y = self.offset_y % scaled_grid_size

        for i in range(start_x, width, scaled_grid_size):
            self.current_canvas.create_line(i, 0, i, height, fill="gray", dash=(2, 2), tags="grid")

        for i in range(start_y, height, scaled_grid_size):
            self.current_canvas.create_line(0, i, width, i, fill="gray", dash=(2, 2), tags="grid")

    # =================================
    # On Canvas : Drag
    # =================================

    def on_start_drag(self, event):
        if not self.shift_pressed:
            self.drag_data["item"] = self.current_canvas.find_closest(event.x, event.y)[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            closest_item = self.current_canvas.find_closest(event.x, event.y)[0]

            tags = self.current_canvas.gettags(closest_item)
            for tag in tags:
                if tag.startswith("group_"):
                    self.current_item = tag
                    bbox = self.current_canvas.bbox(self.current_item)

                    self.offset_x = event.x - bbox[0]
                    self.offset_y = event.y - bbox[1]
                    break

    def on_drag(self, event):
        if not self.shift_pressed:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            tags = self.current_canvas.gettags(self.drag_data["item"])
            for tag in tags:
                if tag.startswith("group_"):
                    group_tag = tag
                    break

            self.current_canvas.move(group_tag, dx, dy)

            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            self.update_connectors(self.drag_data["item"])

    def move_slider(self, event, slider, slider_data):
        if not self.ctrl_pressed:
            if self.drag_data["item"] is not None:
                slider.hide_slider(event)
                x1, y1, x2, y2 = self.current_canvas.bbox(self.drag_data["item"])
                slider.temp_x, slider.temp_y = x1, y2

                slider_data["x"] = x1
                slider_data["y"] = y2

    def on_stop_drag(self, event):
        if not self.shift_pressed and not self.ctrl_pressed:
            self.update_connectors(self.drag_data["item"])

    def on_closing(self):
        self.quit()
        self.destroy()

    # =================================
    # Utilitiy Methods
    # =================================

    def get_all_canvas_items(self, _except_tags=["grid"], canvas=None):
        """Return ids of all the items on the canvas, except those with a given tag.
        Elements with 'grid' tag excepted by default.
        If canvas is not specified, use the current canvas.
        """

        if canvas == None:
            canvas = self.get_current_canvas()

        all_items = set(canvas.find_all())

        exclude_items = set()
        for tag in _except_tags:
            exclude_items.update(canvas.find_withtag(tag))

        return list(all_items - exclude_items)
