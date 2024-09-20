from GUI import HOME
from GUI.GUI_inputManager import GUIInputManager

import pickle
import hmac
import hashlib
import base64

class SaveLoadMethods:

    # =================================
    # SAVE/LOAD
    # =================================

    def save_file(self, file_path):

        state = self.save_state()
        pickled_data = pickle.dumps(state)

        key = self.load_key(HOME + '\Examples\key.txt')
        signature = hmac.new(key, pickled_data, hashlib.sha256).digest()

        with open(file_path, 'wb') as file:
            file.write(signature)  
            file.write(pickled_data)


    def load_file(self, file_path):

        with open(file_path, "rb") as file:
            signature = file.read(32)
            pickled_data = file.read()
        
        key = self.load_key(HOME + '\Examples\key.txt')
        expected_signature = hmac.new(key, pickled_data, hashlib.sha256).digest()
        if hmac.compare_digest(signature, expected_signature):
            state = pickle.loads(pickled_data)
            self.load_state(state)
        else:
            raise ValueError("Data integrity check failed! File may have been tampered with.")

    @staticmethod
    def load_key(filename):

        with open(filename, 'r') as file:
            encoded_key = file.read()
        binary_key = base64.b64decode(encoded_key.encode('utf-8'))
        return binary_key

    def save_state(self):

        state = {"sliders": {key:{"x": self.sliders[key]["x"], 
                                  "y": self.sliders[key]["y"], 
                                  "length": self.sliders[key]["length"]} for key in self.sliders},
                "project": self.project,
                "processess": [], 
                "products": [], 
                "transportation": [],
                "parameter": [],
                "connectors": self.connectors,
                "relationships": self.relationships,
                "dependents": self.dependents,
                "item_map": self.item_map
                }
        
        for item_id in self.canvas.find_withtag("process"):
            coords = self.canvas.coords(item_id)
            fill_color = self.canvas.itemcget(item_id, "fill")
            
            state["processess"].append({"item_id":item_id, "coords": coords, "fill": fill_color})

        for item_id in self.canvas.find_withtag("product"):
            coords = self.canvas.coords(item_id)
            fill_color = self.canvas.itemcget(item_id, "fill")
            
            state["products"].append({"item_id": item_id, "coords": coords, "fill": fill_color})

        for item_id in self.canvas.find_withtag("parameter"):
            coords = self.canvas.coords(item_id)
            fill_color = self.canvas.itemcget(item_id, "fill")
            
            state["parameter"].append({"item_id": item_id, "coords": coords, "fill": fill_color})

        return state

    def load_state(self, state):

        self.connectors = state["connectors"]
        self.project = state["project"]
        self.item_map = state["item_map"]

        # products need to be restored first due to possible dependency of transportation processes
        # on products
        item_id_history = {}
        for rect_data in state["products"]:
            item_id = rect_data["item_id"]
            product = self.item_map[item_id]
            new_item_id = self.restore_product(product, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        for rect_data in state["processess"]:
            item_id = rect_data["item_id"]
            process = self.item_map[item_id]
            if GUIInputManager.is_transport(process):
                new_item_id = self.restore_transportation_process(process, rect_data["coords"])
            else:
                new_item_id = self.restore_process(process, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        for rect_data in state["parameter"]:
            item_id = rect_data["item_id"]
            param = self.item_map[item_id]
            new_item_id = self.restore_parameter(param, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        self.restore_connections(item_id_history)
        self.dependents, self.relationships = self.restore_relationships(item_id_history, state["dependents"], 
                                                                        state["relationships"])    

    def clear_state(self):

        self.canvas.delete("all")
        if self.canvas_grid:
            self.draw_grid()

        for item in self.sliders:
            slider_data = self.sliders[item]
            slider_data["widget"].destroy()

        self.connectors.clear()
        self.sliders.clear()
        self.item_map.clear()
        self.clear_plot_data()

        self.scale = 1.0
        self.zoom_factor = 1.1
        self.pan_start = None
        self.default_slider_width = 10
        self.offset_x = 0
        self.offset_y = 0

        self.draw_grid()

        GUIInputManager.clear_project(self.project, database=False)

        self.update_plot()

        return self