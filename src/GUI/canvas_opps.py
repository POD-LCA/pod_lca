
class CanvasOperations:

    # =================================
    # On Canvas: Zoom and pan
    # =================================

    def start_pan(self, event):
        item = self.canvas.find_withtag("current")
        if not item:
            self.canvas.scan_mark(event.x, event.y)
            self.pan_start = (event.x, event.y)

            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def do_pan(self, event):
        if self.pan_start:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]

            self.offset_x += dx
            self.offset_y += dy

            self.canvas.move("all", dx, dy)

            for item in self.sliders:
                slider_data = self.sliders[item]
                slider = slider_data["widget"]  

                current_x = slider_data['x'] + dx
                current_y = slider_data['y'] + dy  
                    
                slider.place(x=current_x, y=current_y)
                    
                slider_data['x'] = current_x
                slider_data['y'] = current_y

            if self.canvas_grid:
                self.draw_grid()

            self.pan_start = (event.x, event.y)

    def zoom(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if event.delta > 0:
            self.canvas.scale("all", x, y, self.zoom_factor, self.zoom_factor)
            self.scale_widgets(self.zoom_factor)
            self.scale *= self.zoom_factor
        elif event.delta < 0:
            self.canvas.scale("all", x, y, 1 / self.zoom_factor, 1 / self.zoom_factor)
            self.scale_widgets(1 / self.zoom_factor)
            self.scale /= self.zoom_factor

        if self.canvas_grid:
            self.draw_grid()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self, event):
        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        x = self.canvas.canvasx(x)
        y = self.canvas.canvasy(y)
        self.canvas.scale("all", x, y, self.zoom_factor, self.zoom_factor)
        self.scale_widgets(self.zoom_factor)
        self.scale *= self.zoom_factor

        if self.canvas_grid:
            self.draw_grid()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self, event):
        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        x = self.canvas.canvasx(x)
        y = self.canvas.canvasy(y)
        self.canvas.scale("all", x, y, 1 / self.zoom_factor, 1 / self.zoom_factor)
        self.scale_widgets(1 / self.zoom_factor)
        self.scale /= self.zoom_factor

        if self.canvas_grid:
            self.draw_grid()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def scale_widgets(self, factor):
        for item in self.sliders:
            slider_data = self.sliders[item]
            slider = slider_data["widget"]

            new_length = slider_data["length"] * factor
            slider_data["length"]  = new_length
            slider.config(length=int(new_length))

            coords = self.canvas.coords(slider.rect)
            slider.place(in_=self.canvas, x=coords[0], y=coords[3])
            slider_data['x'] = coords[0]
            slider_data['y'] = coords[3]

    def on_canvas_configure(self, event):
        self.draw_grid()

    def draw_grid(self):
        """Draws a grid that updates based on current scale and offset.
        """

        self.canvas.delete("grid")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        scaled_grid_size = int(self.canvas_grid_size * self.scale)

        start_x = self.offset_x % scaled_grid_size
        start_y = self.offset_y % scaled_grid_size

        for i in range(start_x, width, scaled_grid_size):
            self.canvas.create_line(i, 0, i, height, fill="gray", dash=(2, 2), tags="grid")

        for i in range(start_y, height, scaled_grid_size):
            self.canvas.create_line(0, i, width, i, fill="gray", dash=(2, 2), tags="grid")

    # =================================
    # On Canvas : Drag
    # =================================

    def on_start_drag(self, event):
        if not self.shift_pressed:
            self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            closest_item = self.canvas.find_closest(event.x, event.y)[0]
            
            tags = self.canvas.gettags(closest_item)
            for tag in tags:
                if tag.startswith("group_"):
                    self.current_item = tag
                    bbox = self.canvas.bbox(self.current_item)
                    
                    self.offset_x = event.x - bbox[0]
                    self.offset_y = event.y - bbox[1]
                    break


    def on_drag(self, event):
        if not self.shift_pressed:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            tags = self.canvas.gettags(self.drag_data["item"])
            for tag in tags:
                if tag.startswith("group_"):
                    group_tag = tag
                    break
            
            self.canvas.move(group_tag, dx, dy)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            self.update_connectors(self.drag_data["item"])

    def move_slider(self, event, slider, slider_data):
        if not self.ctrl_pressed:
            x1, y1, x2, y2 = self.canvas.bbox(self.drag_data["item"])
            slider.place(in_=self.canvas, x=x1, y=y2)

            slider_data['x'] = x1
            slider_data['y'] = y2
    
    def on_stop_drag(self, event):
        if not self.shift_pressed and not self.ctrl_pressed:
            self.update_connectors(self.drag_data["item"])

    def on_closing(self):
        self.quit()
        self.destroy()
