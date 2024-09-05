from material.projectManager.projectManager import Project
from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.menubar import Menubar
from GUI.plots import Plots
from GUI.process import Process
from GUI.product import Product
from GUI.connectors import Connectors
from GUI.transportation import Transportation

import pickle
from tkinter import Menu, Frame, Button, Canvas, Tk, Label
from tkinter import RIGHT, LEFT, Y, BOTH, TOP
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =================================
# CANVAS
# =================================

class ProcessVisualizer(Tk, Menubar, Plots, Product, Process, Transportation, Connectors):
    def __init__(self):
        super().__init__()
        self.title("Process Visualizer")
        self.geometry("1500x600")

        # color palette
        self.color_transport = "#e8c4a9"
        self.color_process = "#bde8a2"
        self.color_product = "#c3e7f7"
        self.color_canvas = "#dbdad7"

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
        self.connector_type = 'elbow' # 'straight', 'elbow', 'spline'
        self.connector_data = {"line": None, "start_x": 0, "start_y": 0, "start_item": None, "end_item": None}
        self.connectors = []
        self.sliders = []
        # self.tooltips = {}

        self.process_data = {}
        self.product_data = {}
        self.process_item_map = {}
        self.product_item_map = {}

        # back-end
        self.project = GUIInputManager.create_project()

        # ctrl and shift press binding
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

        state = {"sliders": [{"x": slider["x"], "y": slider["y"], "length": slider["length"]} for slider in self.sliders],
                "processess": [], 
                "products": [], 
                "transportation": [],
                "connectors": self.connectors,
                "project": self.project,
                "process_data": self.process_data,
                "product_data": self.product_data
                }
        
        for item_id in self.canvas.find_withtag("process"):
            coords = self.canvas.coords(item_id)
            fill_color = self.canvas.itemcget(item_id, "fill")
            
            state["processess"].append({"item_id":item_id, "coords": coords, "fill": fill_color})

        for item_id in self.canvas.find_withtag("product"):
            coords = self.canvas.coords(item_id)
            fill_color = self.canvas.itemcget(item_id, "fill")
            
            state["products"].append({"item_id": item_id, "coords": coords, "fill": fill_color})

        with open(file_path, "wb") as file:
            pickle.dump(state, file)

    def load_state(self, file_path):

        with open(file_path, "rb") as file:
            state = pickle.load(file)

        self.connectors = state["connectors"]
        self.project = state["project"]
        self.process_data = state["process_data"]
        self.product_data = state["product_data"]

        item_id_map = {}
        for rect_data in state["products"]:
            item_id = rect_data["item_id"]
            process = self.product_data[item_id]
            new_item_id = self.restore_product(process, rect_data["coords"])
            item_id_map[item_id] = new_item_id

        for rect_data in state["processess"]:
            item_id = rect_data["item_id"]
            process = self.process_data[item_id]
            if GUIInputManager.is_transport(process):
                new_item_id = self.restore_transportation_process(process, rect_data["coords"])
            else:
                new_item_id = self.restore_process(process, rect_data["coords"])
            item_id_map[item_id] = new_item_id

        self.restore_connections(item_id_map)


    def clear_state(self):

        self.canvas.delete("all")
        if self.canvas_grid:
            self.draw_grid()

        for slider_data in self.sliders:
            slider_data["widget"].destroy()

        self.connectors.clear()
        self.sliders.clear()
        self.process_data.clear()
        self.product_data.clear()
        self.process_item_map.clear()
        self.product_item_map.clear()
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

        # connector_button = Button(self.menu_frame, text="Connector", command=self.start_drawing_connector)
        # connector_button.pack(pady=10)

    # =================================
    # PROCESS/PRODUCT COMMANDS
    # =================================

    def set_impacts(self, item, process=False, product=False):

        if product:
            cmd = lambda: GUIInputManager.set_impact_data(self, self.product_data[item], impact.get())
        elif process:
            cmd = lambda: GUIInputManager.set_impact_data(self, self.process_data[item], impact.get())
        else:
            raise NotImplementedError
        popup = Popup(self, "Set Impacts", "300x200")

        if not GUIInputManager.get_database_data(self.project) is None:
            impact = popup._popup_input_combo("Impact : ", GUIInputManager.get_database_data(self.project)['Flow'].tolist())

            button_frame = Frame(popup)
            button_frame.pack(pady=20)

            ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
            ok_button.pack(side=LEFT, padx=10)

            cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
            cancel_button.pack(side=LEFT, padx=10)

            apply_button = Button(button_frame, text="Apply", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
            apply_button.pack(side=LEFT, padx=10)
        else:
            label = popup._popup_label("Impact database not loaded.\nGo to Database menu and import database.", justify='left')
            label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))

            button_frame = Frame(popup)
            button_frame.pack(pady=20)

            close_button = Button(button_frame, text="Close", command=popup.destroy)
            close_button.pack(side=LEFT, padx=10)

    def view_impacts(self, item, process=False, product=False):

        popup = Popup(self, "View Impacts", "300x200")

        if product:
            row = GUIInputManager.get_database_row(self.product_data[item])
        elif process:
            row = GUIInputManager.get_database_row(self.process_data[item])
        else:
            raise NotImplementedError

        if row is not None:
            impact_data = GUIInputManager.get_impact_data(self.project, row)
            data_list = row, impact_data["Global warming potential (kg CO2 eq)"], impact_data["Acidification potential (kg SO2 eq)"], impact_data["Eutrophication potential (kg N eq)"], impact_data["Ozone depletion potential (kg CFC-11 eq)"], impact_data["Smog potential (kg O3 eq)"]
        else:
            data_list = "unasigned", 0.0, 0.0, 0.0, 0.0, 0.0

        text_str = "{0} \n GWP : {1:.2f} kg CO2 eq \n Acidification potential : {2:.2f} kg SO2 eq \n Eutrophication potential : {3:.2f} kg N eq \n Ozone depletion potential : {4:.2f} kg CFC-11 eq\n Smog potential : {5:.2f} kg O3 eq".format(*data_list)        
        popup._popup_label(text_str, justify='left')

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        close_button = Button(button_frame, text="Close", command=popup.destroy)
        close_button.pack(side=LEFT, padx=10)

    def update_life_cycle_stage(self, item, process=False, product=False):

        popup = Popup(self, "Update life cycle stage", "300x200")
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"])

        if product:
            cmd = lambda: GUIInputManager.update_life_cycle_stage(self, self.product_data[item], life_cycle_stage.get())
        elif process:
            cmd = lambda: GUIInputManager.update_life_cycle_stage(self, self.process_data[item], life_cycle_stage.get())
        else:
            raise NotImplementedError

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)

        apply_button = Button(button_frame, text="Apply", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
        apply_button.pack(side=LEFT, padx=10)

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
        x1, y1, x2, y2 = self.canvas.bbox(self.drag_data["item"])
        slider.place(in_=self.canvas, x=x1, y=y2)

        slider_data['x'] = x1
        slider_data['y'] = y2
    
    def on_stop_drag(self, event):
        if not self.shift_pressed:
            self.update_connectors(self.drag_data["item"])

    # =================================
    # On Canvas: Zoom and pan
    # =================================

    def start_pan(self, event):
        item = self.canvas.find_withtag("current")
        if not item:
            self.canvas.scan_mark(event.x, event.y)

            self.pan_start = (event.x, event.y)


    def do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        self.offset_x += dx
        self.offset_y += dy

        self.canvas.move("all", dx, dy)

        for slider_data in self.sliders:
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
        for slider_data in self.sliders:
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

    def on_closing(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = ProcessVisualizer()
    app.mainloop()