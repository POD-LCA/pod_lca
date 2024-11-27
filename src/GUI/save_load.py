from GUI import HOME
from GUI.GUI_inputManager import GUIInputManager
from GUI.GUI_outputManager import GUIOutputManager

import pickle
import hmac
import hashlib
import base64
from tkinter import BooleanVar, Checkbutton, LEFT

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
            self.clear_state()
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

        state = {"sliders": {model: {key:{"x": self.sliders[model][key]["x"], 
                                        "y": self.sliders[model][key]["y"], 
                                        "length": self.sliders[model][key]["length"]} for key in self.sliders[model]} for model in self.sliders},
                "project": self.project,
                "scale": self.scale,
                "zoom_factor": self.zoom_factor,
                "processess": {}, 
                "products": {}, 
                "transportation": {},
                "parameter": {},
                "connectors": self.connectors,
                "relationships": self.relationships,
                "dependents": self.dependents,
                "item_map": self.item_map,
                "no_models": len(self.models)
                }
        
        for model in self.models:
            self.save_model_state(state, model)

        return state
    
    def save_model_state(self, state, model):

        state["processess"][model] = []
        for item_id in self.models[model].find_withtag("process"):
            coords = self.models[model].coords(item_id)
            fill_color = self.models[model].itemcget(item_id, "fill")
            
            state["processess"][model].append({"item_id":item_id, "coords": coords, "fill": fill_color})

        state["products"][model] = []
        for item_id in self.models[model].find_withtag("product"):
            coords = self.models[model].coords(item_id)
            fill_color = self.models[model].itemcget(item_id, "fill")
            
            state["products"][model].append({"item_id": item_id, "coords": coords, "fill": fill_color})

        state["parameter"][model] = []
        for item_id in self.models[model].find_withtag("parameter"):
            coords = self.models[model].coords(item_id)
            fill_color = self.models[model].itemcget(item_id, "fill")
            
            state["parameter"][model].append({"item_id": item_id, "coords": coords, "fill": fill_color})

        return state

    def load_state(self, state):

        self.project = state["project"]
        
        self.item_map = {'Model_0':{}}
        self.relationships = {'Model_0':{}}
        self.dependents = {'Model_0':{}}

        for i in range(state["no_models"] - 1):
            self.add_model(add_to_project=False)

        for model in self.models:
            self.load_model_state(state, model)
            self.set_hotspots(model)

            self.set_current_model(model)
            if self.hotspot_on_off.get():
                self.show_hotspots()
        self.connectors = state["connectors"]
        
        self.plot.calculator.project = self.project

        self.update_plot()

    def load_model_state(self, state, model):

        self.current_canvas = self.models[model]
        GUIInputManager.set_current_model(self.project, model)
        # products need to be restored first due to possible dependency of transportation processes
        # on products
        item_map = state["item_map"]
        item_id_history = {}
        for rect_data in state["products"][model]:
            item_id = rect_data["item_id"]
            product = item_map[model][item_id]
            new_item_id = self.restore_product(model, product, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        for rect_data in state["processess"][model]:
            item_id = rect_data["item_id"]
            process = item_map[model][item_id]
            if GUIInputManager.is_transport(process):
                new_item_id = self.restore_transportation_process(model, process, rect_data["coords"])
            else:
                new_item_id = self.restore_process(model, process, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        for rect_data in state["parameter"][model]:
            item_id = rect_data["item_id"]
            param = item_map[model][item_id]
            new_item_id = self.restore_parameter(model, param, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        state["connectors"][model] = self.restore_connections(state["connectors"][model], item_id_history, model)
        self.dependents[model], self.relationships[model] = self.restore_relationships(item_id_history, 
                                                                                        state["dependents"][model], 
                                                                                        state["relationships"][model])


    def clear_state(self):

        for i in range(self.notebook.index("end") - 1, 0, -1):
            self.notebook.forget(i)
        self.current_canvas = self.models["Model_0"]
        self.current_canvas.delete("all")
        if self.canvas_grid:
            self.draw_grid()

        for model in self.sliders:
            for item in self.sliders[model]:
                slider_data = self.sliders[model][item]
                slider_data["widget"].destroy()

        self.current_canvas.current_hotspot = []

        for checkbox in self.plot_checkboxes:
            self.plot_checkboxes[checkbox].destroy()

        var = BooleanVar(value=True)
        self.plot_models["Model_0"] = var
        checkbox = Checkbutton(self.checkbox_frame, text="Model_0", variable=var, command=self.update_plot,
                                bg=self.plotter_bg_color, fg='white', selectcolor="gray")
        checkbox.pack(side=LEFT)
        self.plot_checkboxes["Model_0"] = checkbox

        self.scale = {'Model_0':1.0}
        self.zoom_factor = {'Model_0':1.1}
        self.pan_start = None
        self.default_slider_width = 10
        self.offset_x = 0
        self.offset_y = 0

        self.models = {"Model_0": self.models["Model_0"]}
        self.connectors = {'Model_0':[]}
        self.sliders = {'Model_0':{}}
        self.slider_map = {'Model_0':{}}
        self.label_map = {}
        self.plot_models = {"Model_0": self.plot_models["Model_0"]}
        self.plot_checkboxes = {"Model_0": self.plot_checkboxes["Model_0"]}

        self.item_map = {'Model_0':{}}
        self.relationships = {'Model_0':{}}
        self.dependents = {'Model_0':{}}

        GUIInputManager.clear_project(self.project, database=False)

        self.update_plot()

        return self


    
