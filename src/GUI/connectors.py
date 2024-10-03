from GUI.GUI_inputManager import GUIInputManager

from tkinter import LAST

class ConnectorsMixin:

    # =================================
    # Connectors
    # =================================
    def on_ctrl_press(self, event):

        self.current_canvas.bind("<ButtonPress-1>", self.on_start_connector)
        self.current_canvas.bind("<B1-Motion>", self.on_draw_connector)
        self.current_canvas.bind("<ButtonRelease-1>", self.on_finish_connector)

        for rect in self.current_canvas.find_withtag("process||product||parameter"):
            self.current_canvas.tag_unbind(rect, "<ButtonPress-1>")
            self.current_canvas.tag_unbind(rect, "<B1-Motion>")

        self.ctrl_pressed = True

    def on_ctrl_release(self, event):

        self.current_canvas.unbind("<ButtonPress-1>")
        self.current_canvas.unbind("<B1-Motion>")
        self.current_canvas.unbind("<ButtonRelease-1>")

        for rect in self.current_canvas.find_withtag("process||product||parameter"):
            self.current_canvas.tag_bind(rect, "<ButtonPress-1>", self.on_start_drag)
            self.current_canvas.tag_bind(rect, "<B1-Motion>", self.on_drag)

        self.ctrl_pressed = False

    def on_start_connector(self, event):
        overlapping_items = self.current_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        start_item = None
        
        for item in overlapping_items:
            if "item" in self.current_canvas.gettags(item):
                start_item = item
                break
        
        if start_item:
            self.connector_data["start_item"] = start_item
            self.connector_data["start_x"] = event.x
            self.connector_data["start_y"] = event.y

            
            if not self.shift_pressed:
                smooth = True if self.connector_type == 'spline' else False
                self.connector_data["line"] = self.current_canvas.create_line(event.x, event.y, event.x, event.y, fill=self.connector_color, width=2, smooth=smooth, tag="connector")

    def on_draw_connector(self, event):
        if not self.shift_pressed:
            if self.connector_data["line"] is not None:
                self.current_canvas.coords(self.connector_data["line"], self.connector_data["start_x"], self.connector_data["start_y"], event.x, event.y)
        else:
            self.current_canvas.delete(self.connector_data["line"])

    def on_finish_connector(self, event):

        model_id = self.get_current_model()

        overlapping_items = self.current_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        end_item = None
        
        for item in overlapping_items:
            if "item" in self.current_canvas.gettags(item):
                end_item = item
                break
            
        start_item = self.connector_data["start_item"]        
        if start_item is not None and end_item is not None:
                if self.shift_pressed:
                    self.delete_connection(start_item, end_item)
                else:
                    if self.allow_to_connect(end_item) and not self.already_connected(start_item, end_item):
                        self.draw_connection(self.connector_data["start_item"], end_item, self.connector_data["line"])

                        self.connectors[model_id].append({
                            "line": self.connector_data["line"],
                            "start_item": start_item,
                            "end_item": end_item})

                        connects_to_transport = "transportation" in self.current_canvas.gettags(end_item)
                        from_parameter = "parameter" in self.current_canvas.gettags(start_item)

                        if connects_to_transport:
                            GUIInputManager.set_transported_product(self, self.item_map[model_id][end_item], self.item_map[model_id][start_item])
                            self.update_plot() 

                        if from_parameter:
                            relationship = "{" + str(self.item_disp_num[model_id][start_item]) + "}"
                            self.process_relationship(item, self.slider_map[model_id][end_item], relationship)

                    else:
                        self.current_canvas.delete(self.connector_data["line"])
        else:
            self.current_canvas.delete(self.connector_data["line"])

        self.connector_data = {"line": None, "start_item": None, "start_x": 0, "start_y": 0}


    def delete_connection(self, start_item, end_item):

        model_id = self.get_current_model()

        for connector in self.connectors[model_id]:
            if connector["start_item"] == start_item and connector["end_item"] == end_item:
                self.current_canvas.delete(connector["line"])
                self.connectors[model_id].remove(connector)

                
                if "product" in self.current_canvas.gettags(connector["start_item"]) and "process" in self.current_canvas.gettags(connector["end_item"]):
                    product = self.item_map[model_id][connector["start_item"]]
                    process = self.item_map[model_id][connector["end_item"]]
                    if GUIInputManager.is_transport(process):
                        GUIInputManager.remove_transported_product(self, process, product)

                if "parameter" in self.current_canvas.gettags(connector["start_item"]):
                    self.clear_relationship(self.item_map[model_id][end_item])

                break

    def update_connectors(self, item):

        item_id = item if isinstance(item, int) else item[0]
        model_id = self.get_current_model()

        for connector in self.connectors[model_id]:
            start_item_id = connector["start_item"] if isinstance(connector["start_item"], int) else connector["start_item"][0]
            end_item_id = connector["end_item"] if isinstance(connector["end_item"], int) else connector["end_item"][0]

            if start_item_id == item_id or end_item_id == item_id:
                self.draw_connection(connector["start_item"], connector["end_item"], connector["line"])


    def restore_connections(self, connections, item_id_map, model_id):
        """ Restoring connections after loading saved canvas.
        """

        for connector in connections:
            for tag in ["start_item", "end_item"]:
                connector[tag] = item_id_map[connector[tag]]
            smooth = True if self.connector_type == 'spline' else False
            connector["line"] = self.models[model_id].create_line(0, 0, 0, 0, fill=self.connector_color, width=2, smooth=smooth, tag="connector")
            self.draw_connection(connector["start_item"], connector["end_item"], connector["line"])

    def redraw_connections(self):

        self.current_canvas.delete("connector")
        model_id = self.get_current_model()

        for connector in self.connectors[model_id]:
            smooth = True if self.connector_type == 'spline' else False
            connector["line"] = self.current_canvas.create_line(0, 0, 0, 0, fill=self.connector_color, width=2, smooth=smooth, tag="connector")
            self.draw_connection(connector["start_item"], connector["end_item"], connector["line"])


    def draw_connection(self, start, end, line, connect_to='edge'):

        start_coords = self.current_canvas.coords(start)
        end_coords = self.current_canvas.coords(end)

        if connect_to =='center':
            start_x = (start_coords[0] + start_coords[2]) / 2
            end_x = (end_coords[0] + end_coords[2]) / 2
        elif connect_to =='edge':
            start_x, end_x = self.get_vertical_edges(start_coords, end_coords)
        else:
            raise NotImplementedError

        start_y = (start_coords[1] + start_coords[3]) / 2
        end_y = (end_coords[1] + end_coords[3]) / 2


        if self.connector_type == 'straight':
            self.current_canvas.coords(line, start_x, start_y, end_x, end_y)
            self.current_canvas.itemconfig(line, arrow=LAST)
        elif self.connector_type == 'elbow' or self.connector_type == 'spline':
            offset = self.connector_offset
            control_point1 = (start_x + offset, start_y)
            control_point2 = (end_x - offset, end_y)
            
            self.current_canvas.coords(line,
                       start_x, start_y,
                       control_point1[0], control_point1[1],  
                       control_point2[0], control_point2[1],  
                       end_x, end_y)  
            self.current_canvas.itemconfig(line, arrow=LAST)
        else:
            raise NotImplementedError


    def allow_to_connect(self, item):
        """ Checks if connections is a valid connection for the flow diagram.
            This are logic rules imposed.
        """

        _to = item
        _from = self.connector_data["start_item"]

        is_from_product = "product" in self.current_canvas.gettags(_from)
        is_to_process = "process" in self.current_canvas.gettags(_to)
        is_to_transport = "transportation" in self.current_canvas.gettags(_to)
        is_to_parameter = "parameter" in self.current_canvas.gettags(_to)

        create = True
        if is_from_product:
            if not is_to_process:
                create = False

        if is_to_transport:
            if not is_from_product:
                create = False

        if is_to_parameter:
            create = False

        return create
    
    def already_connected(self, start_item, end_item):

        model_id = self.get_current_model()

        for connector in self.connectors[model_id]:
            if ((connector["start_item"] == start_item and connector["end_item"]  == end_item) or 
                (connector["start_item"] == end_item and connector["end_item"]  == start_item)):
                return True

        return False 
    
    def on_shift_press(self, event):
        self.shift_pressed = True

    def on_shift_release(self, event):
        self.shift_pressed = False

    def get_vertical_edges(self, rect1_coords, rect2_coords):
        left_edge1, right_edge1 = rect1_coords[0], rect1_coords[2]
        left_edge2, right_edge2 = rect2_coords[0], rect2_coords[2]

        return (right_edge1, left_edge2)
