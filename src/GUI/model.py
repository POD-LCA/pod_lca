from GUI.GUI_inputManager import GUIInputManager

import csv
import os
from tkinter import Frame, Canvas, Checkbutton, BooleanVar, Menu, filedialog
from tkinter import LEFT, BOTH

class ModelMixin:

    def add_model_context_menu(self, root):

        context_menu = Menu(root, tearoff=0)
        context_menu.add_command(label="New", command=lambda: self.add_model())
        context_menu_import = Menu(context_menu, tearoff=False)
        context_menu.add_cascade(menu=context_menu_import, label='Import')
        context_menu_import.add_command(label='From CSV', command=lambda :self.import_model_from())
        context_menu_from = Menu(context_menu, tearoff=False)
        context_menu.add_cascade(menu=context_menu_from, label='From Model')
        for id in range(len(self.models)):
            model_id = 'Model_' + str(id)
            context_menu_from.add_command(label=model_id, command=lambda :self.copy_model(model_id))

        button_x = self.model_object_button.winfo_rootx()
        button_y = self.model_object_button.winfo_rooty() + self.model_object_button.winfo_height()
        
        context_menu.tk_popup(button_x, button_y)

    def add_model(self, add_to_project=True):

        model_no =  len(self.models)
        notebook = self.notebook

        model_new = Frame(notebook)

        model_name = "Model_" + str(model_no)
        notebook.add(model_new, text=model_name)
        notebook.pack(expand=True, fill='both')

        canvas_model = Canvas(model_new, bg=self.color_canvas, width=self.canvas_width, height=self.canvas_height)
        canvas_model.pack(side=LEFT, padx=0, pady=0, fill=BOTH)

        canvas_model.bind("<Configure>", self.on_canvas_configure)
        self.create_canvas_bindings(canvas_model)

        self.models[model_name] = canvas_model
        self.scale[model_name] = 1.0
        self.zoom_factor[model_name] = 1.1
        self.reference_point[model_name] = [0,0]
        self.sliders[model_name] = {}
        self.slider_map[model_name] = {}
        self.item_map[model_name] = {}
        self.relationships[model_name] = {}
        self.dependents[model_name] = {}
        self.connectors[model_name] = []
        self.item_disp_num[model_name] = {}
        self.disp_num_item[model_name] = {}

        var = BooleanVar(value=True)
        self.plot_models[model_name] = var
        checkbox = Checkbutton(self.checkbox_frame, text=model_name, variable=var, command=self.update_plot,
                                bg=self.plotter_bg_color, fg='white', selectcolor="gray")
        checkbox.pack(side=LEFT)
        self.plot_checkboxes[model_name] = checkbox

        if add_to_project:
            model = GUIInputManager.create_model(self.project, model_name)

            self.update()
            self.update_plot()

        return model_name
    
    def copy_model(self, source_model_id):

        new_model_id = self.add_model(add_to_project=True)
        self.set_current_model(new_model_id) # Check if this is needed

        state = {"processess": {}, 
                "products": {}, 
                "transportation": {},
                "parameter": {},
                "connectors": self.connectors,
                "relationships": self.relationships,
                "dependents": self.dependents,
                "item_map": self.item_map,
                }
        state = self.save_model_state(state, source_model_id)

        # products need to be restored first due to possible dependency of transportation processes
        # on products
        item_map = state["item_map"]
        item_id_history = {}
        for rect_data in state["products"][source_model_id]:
            item_id = rect_data["item_id"]
            product = item_map[source_model_id][item_id]
            copy_product = GUIInputManager.copy(product)
            GUIInputManager.add_product(self.project, new_model_id, copy_product)
            new_item_id = self.restore_product(new_model_id, copy_product, rect_data["coords"])
            item_id_history[item_id] = new_item_id
            GUIInputManager.set_id(copy_product, new_item_id)

        for rect_data in state["processess"][source_model_id]:
            item_id = rect_data["item_id"]
            process = item_map[source_model_id][item_id]
            copy_process = GUIInputManager.copy(process)
            GUIInputManager.add_process(self.project, new_model_id, copy_process)
            if GUIInputManager.is_transport(process):
                new_item_id = self.restore_transportation_process(new_model_id, copy_process, rect_data["coords"])
            else:
                new_item_id = self.restore_process(new_model_id, copy_process, rect_data["coords"])
            item_id_history[item_id] = new_item_id
            GUIInputManager.set_id(copy_process, new_item_id)

        for rect_data in state["parameter"][source_model_id]:
            item_id = rect_data["item_id"]
            param = item_map[source_model_id][item_id] # TODO: test this - check what is returned here
            new_item_id = self.restore_parameter(new_model_id, param, rect_data["coords"])
            item_id_history[item_id] = new_item_id

        connections_lst = self.restore_connections(state["connectors"][source_model_id], item_id_history, new_model_id) #FIXME
        self.connectors[new_model_id] = connections_lst

        self.dependents[new_model_id], self.relationships[new_model_id] = self.restore_relationships(item_id_history, 
                                                                                        state["dependents"][source_model_id], 
                                                                                        state["relationships"][source_model_id]) # TODO: test 

        self.update_plot()
        if self.hotspot_on_off.get():
            self.show_hotspots()
            

    def import_model_from(self):

        home_dir = os.path.expanduser("~")
        file_path = filedialog.askopenfilename(initialdir=home_dir, 
                                                title="Open file", 
                                                defaultextension=".csv",
                                                filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

        if file_path:

            if self.get_number_of_canvases() == 1 and len(self.get_all_canvas_items()) == 0:
                model_id = self.get_current_model()
            else:
                model_id = self.add_model(add_to_project=True)
                self.set_current_model(model_id)
                
            tmp_transportation_map = {}
            tmp_product_item_map = {}
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                data = csv.reader(file)
                headers = next(data)
                header_map = {header:index for index, header in enumerate(headers)} 
                for row in data:
                    name = row[header_map['Name']]
                    life_cycle_stage = row[header_map['LC stage']]
                    database_item = row[header_map['Impact data']]
                    qty, unit = row[header_map['qty']], row[header_map['unit']]
                    
                    item_type = row[header_map['type']]
                    if item_type == 'Product':
                        item_id = self.create_product(None, name, qty, unit, life_cycle_stage, database_item)
                    elif item_type == 'Process':
                        item_id = self.create_process(None, name, qty, unit, life_cycle_stage, database_item)
                    elif item_type == 'Transportation':
                        item_id = self.create_transport_process(None, name, qty, unit, life_cycle_stage, database_item)
                    elif item_type == 'Energy':
                        item_id = self.create_energy_product(None, name, qty, unit, life_cycle_stage, database_item)
                    elif item_type == 'Emission':
                        item_id = self.create_emission_product(None, name, qty, unit, life_cycle_stage, database_item)
                    elif item_type == 'Waste':
                        item_id = self.create_waste_product(None, name, qty, unit, life_cycle_stage, database_item)                   
                    else:
                        raise TypeError(f"Item type of {item_type} is undefined.")
                    tmp_product_item_map[name] = item_id

                    item = self.item_map[model_id][item_id]
                    if item_type == 'Transportation':
                        transported_item = row[header_map['transported item']]
                        if not (transported_item == ''):
                            tmp_transportation_map[transported_item] = name
                    else:
                        density = row[header_map['density']]
                        weight_unit = row[header_map['weight unit']]
                        if not (density == ''):
                            item.set_density(density)        
                        if not (weight_unit == ''):
                            item.set_weight_unit(weight_unit)
            
            if tmp_transportation_map:
                for entry in tmp_transportation_map:
                    product_item_id = tmp_product_item_map[entry]
                    transporter_item_id = tmp_product_item_map[tmp_transportation_map[entry]]
                    GUIInputManager.set_transported_product(self, 
                                                            transporter=self.item_map[model_id][transporter_item_id], 
                                                            product=self.item_map[model_id][product_item_id])
                    
                    smooth = True if self.connector_type == 'spline' else False
                    line = self.current_canvas.create_line(0, 0, 0, 0, fill=self.connector_color, width=2, smooth=smooth, tag="connector") 
                    self.draw_connection(product_item_id, transporter_item_id, line)  
                    self.connectors[model_id].append({"line": line,
                                                      "start_item": product_item_id,
                                                      "end_item": transporter_item_id})
