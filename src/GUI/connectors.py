from tkinter import LAST

class Connectors:

    # =================================
    # Connectors
    # =================================

    def start_drawing_connector(self):
        self.canvas.bind("<ButtonPress-1>", self.on_start_connector)
        self.canvas.bind("<B1-Motion>", self.on_draw_connector)
        self.canvas.bind("<ButtonRelease-1>", self.on_finish_connector)

        for rect in self.canvas.find_withtag("process"):
            self.canvas.tag_unbind(rect, "<ButtonPress-1>")
            self.canvas.tag_unbind(rect, "<B1-Motion>")

        for rect in self.canvas.find_withtag("product"):
            self.canvas.tag_unbind(rect, "<ButtonPress-1>")
            self.canvas.tag_unbind(rect, "<B1-Motion>")

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
            
            self.connector_data["line"] = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)

    def on_draw_connector(self, event):
        if self.connector_data["line"] is not None:
            self.canvas.coords(self.connector_data["line"], self.connector_data["start_x"], self.connector_data["start_y"], event.x, event.y)

    def on_finish_connector(self, event):
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        end_item = None
        
        for item in overlapping_items:
            if "process" in self.canvas.gettags(item) or "product" in self.canvas.gettags(item):
                end_item = item
                break

        if self.connector_data["start_item"] is not None and ("process" in self.canvas.gettags(end_item) or "product" in self.canvas.gettags(end_item)):
            start_coords = self.canvas.coords(self.connector_data["start_item"])
            end_coords = self.canvas.coords(end_item)
            
            start_center_x = (start_coords[0] + start_coords[2]) / 2
            start_center_y = (start_coords[1] + start_coords[3]) / 2
            end_center_x = (end_coords[0] + end_coords[2]) / 2
            end_center_y = (end_coords[1] + end_coords[3]) / 2
            
            # connector line connects to the centers of the rectangles
            self.canvas.coords(self.connector_data["line"], start_center_x, start_center_y, end_center_x, end_center_y)
            self.canvas.itemconfig(self.connector_data["line"], arrow=LAST)

            self.connectors.append({
                "line": self.connector_data["line"],
                "start_item": self.connector_data["start_item"],
                "end_item": end_item
            })

        else:
            self.canvas.delete(self.connector_data["line"])

        self.connector_data = {"line": None, "start_item": None, "start_x": 0, "start_y": 0}
        
        # Release rectangles
        for rect in self.canvas.find_withtag("process"):
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(rect, "<B1-Motion>", self.on_drag)
        
        for rect in self.canvas.find_withtag("product"):
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(rect, "<B1-Motion>", self.on_drag)

        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")  

    def update_connectors(self, item):

        item_id = item if isinstance(item, int) else item[0]
        for connector in self.connectors:
            start_item_id = connector["start_item"] if isinstance(connector["start_item"], int) else connector["start_item"][0]
            end_item_id = connector["end_item"] if isinstance(connector["end_item"], int) else connector["end_item"][0]

            if start_item_id == item_id or end_item_id == item_id:
                start_coords = self.canvas.coords(connector["start_item"])
                end_coords = self.canvas.coords(connector["end_item"])
                
                start_center_x = (start_coords[0] + start_coords[2]) / 2
                start_center_y = (start_coords[1] + start_coords[3]) / 2
                end_center_x = (end_coords[0] + end_coords[2]) / 2
                end_center_y = (end_coords[1] + end_coords[3]) / 2
                
                # Connector line ends at the centroid of the rectangle
                self.canvas.coords(connector["line"], start_center_x, start_center_y, end_center_x, end_center_y)
