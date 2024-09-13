from material.projectManager.projectManager import Project
from GUI.GUI_inputManager import GUIInputManager
from GUI.menubar import Menubar
from GUI.plots import Plots
from GUI.process import Process
from GUI.product import Product
from GUI.connectors import Connectors
from GUI.transportation import Transportation
from GUI.parameter import Parameter
from GUI.relationships import Relationships
from GUI.canvas_opps import CanvasOperations

from numpy import where
import pickle
from tkinter import Menu, Frame, Button, Canvas, Tk, Label
from tkinter import RIGHT, LEFT, Y, BOTH, TOP, DISABLED
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ProcessVisualizer(Tk, CanvasOperations, Menubar, Plots, Product, Process, Transportation, Parameter, Connectors, Relationships):
    def __init__(self):
        super().__init__()
        self.title("Process Visualizer")
        self.geometry("1500x800")
        self.save_path = None

        # color palette
        self.color_transport = "#e8c4a9"
        self.color_process = "#bde8a2"
        self.color_product = "#c3e7f7"
        self.color_parameter = "#4287f5"
        self.color_canvas = "#dbdad7"
        self.outline_color = 'black'
        self.outline_width = 2
        self.highlight_color = 'red'
        self.highlight_width = 5

        # Zoom and Pan settings
        self.scale = 1.0
        self.zoom_factor = 1.1
        self.pan_start = None
        self.default_slider_width = 10
        self.offset_x = 0
        self.offset_y = 0

        # Menu
        self.menu_frame = Frame(self, bg="grey", width=200, height=600)
        self.menu_frame.pack(side=LEFT, fill=Y)
        
        self.create_menu()
        
        # Canvas
        self.canvas_grid = True
        self.canvas_grid_size = 20      
        self.content_frame = Frame(self, width=600, height=600)
        self.content_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas = Canvas(self.content_frame, bg=self.color_canvas, width=800, height=800)
        self.canvas.pack(side=LEFT, padx=10, pady=10)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Figure
        self.plot_frame = Frame(self.content_frame, width=300, height=300)
        self.plot_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        input_frame = Frame(self.plot_frame)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text="Environemnt Impact")
        label.pack(side=TOP, padx=(0, 10))
        
        self.impact_categories = {'GWP':'kg CO2 eq', 'acid_pot':'kg SO2 eq', 'eutro_pot':'kg N eq', 'ozone_dep':'kg CFC-11 eq', 'smog':'kg O3 eq'}
        dropdown = Combobox(input_frame, values=list(self.impact_categories.keys()))
        dropdown.pack(side=TOP)
        dropdown.current(0)
        dropdown.bind("<<ComboboxSelected>>", lambda x:self._update_plot_from_combo(x))

        self.plot_data = {}
        for impact in self.impact_categories.keys():
            self.plot_data[impact] = {'A1':0.0, 'A2':0.0, 'A3':0.0}
        self.ax = None
        self.plot_impact_cat = dropdown.get()
        fig = self.create_plot()

        self.canvas_plot = FigureCanvasTkAgg(fig, master=self.content_frame)
        self.canvas_plot.draw()
        self.canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

        # Menu bar
        self.database_file_path = ''

        menubar = Menu(self, tearoff=False)
        self.config(menu=menubar)

        self.create_file_menu(menubar)
        self.create_edit_menu(menubar)
        self.create_database_menu(menubar)
        self.create_help_menu(menubar)
        
        # background data
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.connector_type = 'elbow'
        self.connector_offset = 50
        self.connector_data = {"line": None, "start_x": 0, "start_y": 0, "start_item": None, "end_item": None}
        self.connectors = []
        self.sliders = {}
        self.slider_map = {}
        self.label_map = {}
        # self.tooltips = {}

        self.item_map = {}
        self.relationships = {}
        self.dependents = {}

        # back-end
        self.project = GUIInputManager.create_project()

        # ctrl and shift press binding
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.bind_all("<Control_L>", self.on_ctrl_press)
        self.bind_all("<KeyRelease-Control_L>", self.on_ctrl_release)
        self.bind_all("<KeyPress-Shift_L>", self.on_shift_press)
        self.bind_all("<KeyRelease-Shift_L>", self.on_shift_release)

        self.canvas.bind("<ButtonPress-3>", self.start_pan)  # Right mouse button for panning
        self.canvas.bind("<B3-Motion>", self.do_pan)
        self.canvas.bind("<MouseWheel>", self.zoom)  # Mouse wheel for zoom
        self.bind_all("<Control-plus>", self.zoom_in)  # Ctrl + for zooming in
        self.bind_all("<Control-minus>", self.zoom_out)  # Ctrl - for zooming out

        # window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # =================================
    # SAVE/LOAD
    # =================================

    def save_state(self, file_path):

        state = {"sliders": {key:{"x": self.sliders[key]["x"], 
                                  "y": self.sliders[key]["y"], 
                                  "length": self.sliders[key]["length"]} for key in self.sliders},
                "processess": [], 
                "products": [], 
                "transportation": [],
                "parameter": [],
                "connectors": self.connectors,
                "relationships": self.relationships,
                "project": self.project,
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

        with open(file_path, "wb") as file:
            pickle.dump(state, file)

    def load_state(self, file_path):

        with open(file_path, "rb") as file:
            state = pickle.load(file)

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
        self.restore_relationships()

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
        
    # =================================
    # MENU
    # =================================

    def create_menu(self):
        flow_object_button = Button(self.menu_frame, text="Product", command=self.open_popup_product)
        flow_object_button.pack(pady=10)

        process_object_button = Button(self.menu_frame, text="Process", command=self.open_popup_process)
        process_object_button.pack(pady=10)

        transportation_object_button = Button(self.menu_frame, text="Transportation", command=self.open_popup_transport_process)
        transportation_object_button.pack(pady=10)

        parameter_object_button = Button(self.menu_frame, text="Parameter", command=self.open_popup_parameter)
        parameter_object_button.pack(pady=10)

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

if __name__ == "__main__":
    app = ProcessVisualizer()
    app.mainloop()