from GUI.GUI_inputManager import GUIInputManager

from tkinter import LAST

class Connectors:

    # =================================
    # Connectors
    # =================================
    def on_ctrl_press(self, event):

        self.canvas.bind("<ButtonPress-1>", self.on_start_connector)
        self.canvas.bind("<B1-Motion>", self.on_draw_connector)
        self.canvas.bind("<ButtonRelease-1>", self.on_finish_connector)

        for rect in self.canvas.find_withtag("process"):
            self.canvas.tag_unbind(rect, "<ButtonPress-1>")
            self.canvas.tag_unbind(rect, "<B1-Motion>")

        for rect in self.canvas.find_withtag("product"):
            self.canvas.tag_unbind(rect, "<ButtonPress-1>")
            self.canvas.tag_unbind(rect, "<B1-Motion>")

    def on_ctrl_release(self, event):

        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        for rect in self.canvas.find_withtag("process"):
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(rect, "<B1-Motion>", self.on_drag)
        
        for rect in self.canvas.find_withtag("product"):
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(rect, "<B1-Motion>", self.on_drag)

    def on_start_connector(self, event):
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        start_item = None
        
        for item in overlapping_items:
            if "process" in self.canvas.gettags(item) or "product" in self.canvas.gettags(item):
                start_item = item
                break
        
        if start_item:
            self.connector_data["start_item"] = start_item
            self.connector_data["start_x"] = event.x
            self.connector_data["start_y"] = event.y

            
            if not self.shift_pressed:
                self.connector_data["line"] = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)

    def on_draw_connector(self, event):
        if not self.shift_pressed:
            if self.connector_data["line"] is not None:
                self.canvas.coords(self.connector_data["line"], self.connector_data["start_x"], self.connector_data["start_y"], event.x, event.y)
        else:
            self.canvas.delete(self.connector_data["line"])

    def on_finish_connector(self, event):
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        end_item = None
        
        for item in overlapping_items:
            if "process" in self.canvas.gettags(item) or "product" in self.canvas.gettags(item):
                end_item = item
                break
            
        start_item = self.connector_data["start_item"]        
        if start_item is not None and end_item is not None:
                if self.shift_pressed:
                    self.delete_connection(start_item, end_item)
                else:
                    if self.allow_to_connect(end_item) and not self.already_connected(start_item, end_item):
                        self.draw_connection(self.connector_data["start_item"], end_item, self.connector_data["line"])

                        self.connectors.append({
                            "line": self.connector_data["line"],
                            "start_item": start_item,
                            "end_item": end_item})

                        connects_to_transport = "transportation" in self.canvas.gettags(item)
                        if connects_to_transport:
                            GUIInputManager.set_transported_products(self, self.process_data[end_item], self.product_data[start_item])
                    else:
                        self.canvas.delete(self.connector_data["line"])
        else:
            self.canvas.delete(self.connector_data["line"])

        self.connector_data = {"line": None, "start_item": None, "start_x": 0, "start_y": 0}


    def delete_connection(self, start_item, end_item):
        for connector in self.connectors:
            if connector["start_item"] == start_item and connector["end_item"] == end_item:
                self.canvas.delete(connector["line"])
                self.connectors.remove(connector)

                if connector["start_item"] in self.product_data and connector["end_item"] in self.process_data:
                    product = self.product_data[connector["start_item"]]
                    process = self.process_data[connector["end_item"]]
                    if GUIInputManager.is_transport(process):
                        GUIInputManager.remove_transported_product(self, process, product)

                break

    def update_connectors(self, item):

        item_id = item if isinstance(item, int) else item[0]
        for connector in self.connectors:
            start_item_id = connector["start_item"] if isinstance(connector["start_item"], int) else connector["start_item"][0]
            end_item_id = connector["end_item"] if isinstance(connector["end_item"], int) else connector["end_item"][0]

            if start_item_id == item_id or end_item_id == item_id:
                self.draw_connection(connector["start_item"], connector["end_item"], connector["line"])


    def restore_connections(self, item_id_map):
        """ Restoring connections after loading saved canvas.
        """
        for connector in self.connectors:
            for tag in ["start_item", "end_item"]:
                connector[tag] = item_id_map[connector[tag]]
            connector["line"] = self.canvas.create_line(0, 0, 0, 0, fill="black", width=2)
            self.draw_connection(connector["start_item"], connector["end_item"], connector["line"])

    def draw_connection(self, start, end, line):

        start_coords = self.canvas.coords(start)
        end_coords = self.canvas.coords(end)
        
        start_center_x = (start_coords[0] + start_coords[2]) / 2
        start_center_y = (start_coords[1] + start_coords[3]) / 2
        end_center_x = (end_coords[0] + end_coords[2]) / 2
        end_center_y = (end_coords[1] + end_coords[3]) / 2
        
        # connector line connects to the centers of the rectangles
        self.canvas.coords(line, start_center_x, start_center_y, end_center_x, end_center_y)
        self.canvas.itemconfig(line, arrow=LAST)


    def allow_to_connect(self, item):
        """ Checks if connections is a valid connection for the flow diagram.
            This are logic rules imposed.
        """

        is_from_product = self.connector_data["start_item"] in self.product_data
        is_to_process = "process" in self.canvas.gettags(item)
        is_to_transport = "transportation" in self.canvas.gettags(item)

        create = True
        if is_from_product:
            if not is_to_process:
                create = False

        if is_to_transport:
            if not is_from_product:
                create = False

        return create
    
    def already_connected(self, start_item, end_item):

        for connector in self.connectors:
            if ((connector["start_item"] == start_item and connector["end_item"]  == end_item) or 
                (connector["start_item"] == end_item and connector["end_item"]  == start_item)):
                return True

        return False 
    
    def on_shift_press(self, event):
        self.shift_pressed = True

    def on_shift_release(self, event):
        self.shift_pressed = False