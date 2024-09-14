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
from GUI.save_load import SaveLoadMethods

from tkinter import Menu, Frame, Button, Canvas, Tk, Label
from tkinter import RIGHT, LEFT, Y, BOTH, TOP
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProcessVisualizer(Tk, CanvasOperations, Menubar, Plots, Product, Process, Transportation, Parameter, Connectors, 
                        Relationships, SaveLoadMethods):
    def __init__(self):
        super().__init__()
        self.title("Process Visualizer")
        self.geometry("1500x800")
        self.save_path = None

        # canvas properties
        self.color_transport = "#e8c4a9"
        self.color_process = "#bde8a2"
        self.color_product = "#c3e7f7"
        self.color_parameter = "#4287f5"
        self.color_canvas = "#dbdad7"
        self.outline_color = 'black'
        self.outline_width = 2
        self.highlight_color = 'red'
        self.highlight_width = 5
        self.connector_type = 'elbow'
        self.connector_offset = 50

        # Canvas actions
        self.scale = 1.0
        self.zoom_factor = 1.1
        self.pan_start = None
        self.default_slider_width = 10
        self.offset_x = 0
        self.offset_y = 0

        self.canvas_grid = True
        self.canvas_grid_size = 20
      
        # book-keeping
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.connector_data = {"line": None, "start_x": 0, "start_y": 0, "start_item": None, "end_item": None}
        self.connectors = []
        self.sliders = {}
        self.slider_map = {}
        self.label_map = {}

        self.item_map = {}
        self.relationships = {}
        self.dependents = {}

        # back-end
        self.project = GUIInputManager.create_project()

        # impacts
        self.database_file_path = ''
        self.impact_categories = {'GWP':'kg CO2 eq', 'acid_pot':'kg SO2 eq', 'eutro_pot':'kg N eq', 'ozone_dep':'kg CFC-11 eq', 'smog':'kg O3 eq'}

        # GUI
        self.content_frame = self.create_frame()
        self.palette_frame = self.create_palette(self.content_frame)
        self.canvas = self.create_canvas(self.content_frame)
        self.plot_frame, self.canvas_plot = self.create_plotter(self.content_frame)
        self.menubar = self.create_menubar()

        self.create_bindings()
        self.set_protocols()
        
    # =================================
    # GUI COMPONENTS
    # =================================

    def create_frame(self):

        content_frame = Frame(self, width=600, height=600)
        content_frame.pack(side=TOP, fill=BOTH, expand=True)

        return content_frame

    def create_palette(self, frame):

        palette_frame = Frame(frame, bg="grey", width=200, height=600)
        palette_frame.pack(side=LEFT, fill=Y)
    
        flow_object_button = Button(palette_frame, text="Product", command=self.open_popup_product)
        flow_object_button.pack(pady=10)

        process_object_button = Button(palette_frame, text="Process", command=self.open_popup_process)
        process_object_button.pack(pady=10)

        transportation_object_button = Button(palette_frame, text="Transportation", command=self.open_popup_transport_process)
        transportation_object_button.pack(pady=10)

        parameter_object_button = Button(palette_frame, text="Parameter", command=self.open_popup_parameter)
        parameter_object_button.pack(pady=10)

        return palette_frame

    def create_canvas(self,frame):

        canvas = Canvas(frame, bg=self.color_canvas, width=800, height=800)
        canvas.pack(side=LEFT, padx=10, pady=10)
        canvas.bind("<Configure>", self.on_canvas_configure)

        return canvas
    
    def create_plotter(self, frame):

        plot_frame = Frame(frame, width=300, height=300)
        plot_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        input_frame = Frame(plot_frame)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text="Environemnt Impact")
        label.pack(side=TOP, padx=(0, 10))
        
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

        canvas_plot = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

        return plot_frame, canvas_plot
    
    def create_menubar(self):

        menubar = Menu(self, tearoff=False)
        self.config(menu=menubar)

        self.create_file_menu(menubar)
        self.create_edit_menu(menubar)
        self.create_database_menu(menubar)
        self.create_help_menu(menubar)

        return menubar
    
    # =================================
    # BINDINGS / PROTOCOLS
    # =================================

    def create_bindings(self):

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

    def set_protocols(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


if __name__ == "__main__":
    app = ProcessVisualizer()
    app.mainloop()