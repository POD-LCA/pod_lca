from GUI import HOME
from GUI.GUI_inputManager import GUIInputManager
from GUI.menubar import MenubarMixin
from GUI.plots import PlotsMixin
from GUI.process import Process
from GUI.model import ModelMixin
from GUI.energy import EnergyProduct
from GUI.emission import EmissionProduct
from GUI.waste import WasteProduct
from GUI.parameter import Parameter
from GUI.connectors import ConnectorsMixin
from GUI.transportation import Transportation
from GUI.relationships import RelationshipsMixin
from GUI.canvas_opps import CanvasOperationsMixin
from GUI.save_load import SaveLoadMethods
from GUI.hotspots import HotspotMixins

from tkinter import Menu, Frame, Button, Canvas, Tk, Label, font, Checkbutton, BooleanVar
from tkinter import RIGHT, LEFT, X, Y, BOTH, TOP, NW
from tkinter.ttk import Combobox, Style, Notebook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProcessVisualizer(Tk, CanvasOperationsMixin, MenubarMixin, PlotsMixin, ModelMixin, Process, Transportation, EnergyProduct, EmissionProduct,
                        WasteProduct, Parameter, ConnectorsMixin, RelationshipsMixin, SaveLoadMethods, HotspotMixins):
    def __init__(self):
        super().__init__()
        Style().theme_use('vista')
        self.title("POD|LCA Material Explorer")
        # self.geometry("1500x800")
        self.state("zoomed")
        self.database_file_path = HOME + '\Impact Database\impact_data.csv'
        self.save_path = None

        # canvas properties
        self.color_transport = "#e8c4a9"
        self.color_process = "#bde8a2"
        self.color_product = "#c3e7f7"
        self.color_energy = "#e6d3b8"
        self.color_emission = "#d9ccde"
        self.color_waste = "#d9abbd"
        self.color_parameter = "#4287f5"
        self.color_canvas = "#313131"
        self.outline_color = 'black'
        self.connector_color = '#FFFFFF'
        self.outline_width = 2
        self.highlight_color = 'blue'
        self.highlight_width = 5
        self.hotspot_color = 'red'
        self.hotspot_width = 5
        self.impact_bubble_radius = 10
        self.connector_type = 'elbow'
        self.connector_offset = 50

        self.plotter_bg_color = "#313131"

        # Canvas actions
        self.scale = {'Model_0':1.0}
        self.zoom_factor = {'Model_0':1.1}
        
        self.default_slider_width = 10

        self.pan_start = None
        self.offset_x = 0
        self.offset_y = 0

        self.canvas_grid = True
        self.canvas_grid_size = 20
      
        # book-keeping
        self.models = {}
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.connector_data = {"line": None, "start_x": 0, "start_y": 0, "start_item": None, "end_item": None}
        self.connectors = {'Model_0':[]}
        self.sliders = {'Model_0':{}}
        self.slider_map = {'Model_0':{}}
        self.label_map = {}
        self.plot_models = {}
        self.plot_checkboxes = {}
        self.item_disp_num = {'Model_0':{}}
        self.disp_num_item = {'Model_0':{}}

        self.item_map = {'Model_0':{}}
        self.relationships = {'Model_0':{}}
        self.dependents = {'Model_0':{}}

        # back-end
        self.impact_categories = {'GWP':'kg CO2 eq', 'acid_pot':'kg SO2 eq', 'eutro_pot':'kg N eq', 'ozone':'kg CFC-11 eq', 'smog':'kg O3 eq'}
        self.project = GUIInputManager.create_project()
        GUIInputManager.set_impact_categories(self.project, list(self.impact_categories))     
        
        # GUI
        # self.create_window()
        self.content_frame = self.create_frame()
        self.palette_frame = self.create_palette(self.content_frame)
        self.current_canvas, self.notebook = self.create_canvas(self.content_frame)
        self.plot_frame, self.canvas_plot = self.create_plotter(self.content_frame)
        self.menubar = self.create_menubar()

        self.create_bindings()
        self.set_protocols()
        GUIInputManager.import_data_from_CSV(self.database_file_path, self.project)
        
    # =================================
    # GUI COMPONENTS
    # =================================

    # def move_window(self, event):
    #     self.geometry(f'+{event.x_root}+{event.y_root}')

    # def close_window(self):
    #     self.destroy()

    # def create_window(self):
    #     self.overrideredirect(True)

    #     title_bar = Frame(self, bg='black', relief='raised', bd=2)
    #     title_bar.pack(fill=X)

    #     title_label = Label(title_bar, text="POD|LCA Material Calculator", bg='black', fg='white')
    #     title_label.pack(side=LEFT, padx=10)

    #     close_button = Button(title_bar, text='X', command=lambda:self.close_window(), bg='blue', fg='white')
    #     close_button.pack(side=RIGHT)

    #     title_bar.bind('<B1-Motion>', lambda event:self.move_window(event))

    def create_frame(self):

        content_frame = Frame(self, width=600, height=600, bg='#020f12')
        content_frame.pack(side=TOP, fill=BOTH, expand=True)

        return content_frame

    def create_palette(self, frame):

        palette_color = '#313131'
        button_height = 3
        button_width = 12
        button_color = '#ff2aff'
        model_button_color = '#8f2ab0'
        button_font_color='black'
        button_font = ('Helvetica', 12,'bold')
        button_side = LEFT
        padx = 15
        pady = 15

        palette_frame = Frame(frame, bg=palette_color, width=200, height=600)
        palette_frame.pack(side=TOP, anchor=NW, padx=0, pady=(0,10), fill=BOTH)

        flow_object_button = Button(palette_frame, bg=model_button_color, highlightbackground=model_button_color,
                                    fg='white', height=button_height, width=button_width,font=button_font, 
                                    text="Model", command=self.add_model)
        flow_object_button.pack(side=button_side, padx=padx, pady=pady)

        flow_object_button = Button(palette_frame, bg=button_color, highlightbackground=button_color,
                                    fg=button_font_color, height=button_height, width=button_width,font=button_font, 
                                    text="Product", command=self.open_popup_product)
        flow_object_button.pack(side=button_side, padx=padx, pady=pady)

        process_object_button = Button(palette_frame, bg=button_color, 
                                       fg=button_font_color, height=button_height, width=button_width,font=button_font,  
                                       text="Process", command=self.open_popup_process)
        process_object_button.pack(side=LEFT, padx=padx, pady=pady)

        transportation_object_button = Button(palette_frame, bg=button_color, 
                                              fg=button_font_color, height=button_height, width=button_width,font=button_font,  
                                              text="Transportation", command=self.open_popup_transport_process)
        transportation_object_button.pack(side=LEFT,padx=padx, pady=pady)

        Energy_object_button = Button(palette_frame, bg=button_color, highlightbackground=button_color,
                                    fg=button_font_color, height=button_height, width=button_width,font=button_font, 
                                    text="Energy", command=self.open_popup_energy)
        Energy_object_button.pack(side=button_side, padx=padx, pady=pady)

        Emission_object_button = Button(palette_frame, bg=button_color, highlightbackground=button_color,
                                    fg=button_font_color, height=button_height, width=button_width,font=button_font, 
                                    text="Emission", command=self.open_popup_emission)
        Emission_object_button.pack(side=button_side, padx=padx, pady=pady)

        waste_object_button = Button(palette_frame, bg=button_color, highlightbackground=button_color,
                                    fg=button_font_color, height=button_height, width=button_width,font=button_font, 
                                    text="Waste", command=self.open_popup_waste)
        waste_object_button.pack(side=button_side, padx=padx, pady=pady)

        parameter_object_button = Button(palette_frame, bg=button_color, 
                                         fg=button_font_color, height=button_height, width=button_width,font=button_font,  
                                         text="Parameter", command=self.open_popup_parameter)
        parameter_object_button.pack(side=LEFT, padx=padx, pady=pady)


        return palette_frame

    def create_canvas(self, frame):

        self.canvas_width = 1200
        self.canvas_height = 800
        border_color = "#284387"
        border_thickness = 0

        canvas_frame = Frame(frame, highlightbackground=border_color, highlightthickness=border_thickness)
        canvas_frame.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0)
        canvas_frame.pack(side=LEFT, padx=(10,5), pady=5, fill=BOTH)

        notebook = Notebook(canvas_frame)

        model_0 = Frame(notebook)

        notebook.add(model_0, text="Model_0")
        notebook.pack(expand=True, fill='both')

        canvas_model_0 = Canvas(model_0, bg=self.color_canvas, width=self.canvas_width, height=self.canvas_height)
        canvas_model_0.pack(side=LEFT, padx=0, pady=0, fill=BOTH)

        canvas_model_0.bind("<Configure>", self.on_canvas_configure)
        self.create_canvas_bindings(canvas_model_0)

        self.models["Model_0"] = canvas_model_0

        notebook.bind("<<NotebookTabChanged>>", self.reset_model)

        return canvas_model_0, notebook
    
    def create_plotter(self, frame):

        border_color = "#284387"
        border_thickness = 0
    
        plot_frame = Frame(frame, bg=self.plotter_bg_color, width=350, height=300, highlightbackground=border_color, highlightthickness=border_thickness)
        plot_frame.pack(side=RIGHT, fill=BOTH, padx=(5,10), pady=5)

        input_frame = Frame(plot_frame)
        input_frame.pack(side=TOP, pady=10, padx=10)
        
        label = Label(input_frame, bg=self.plotter_bg_color, fg='white', text="Environmental impact category", font = ('Helvetica', 12,'bold'))
        label.pack(side=LEFT, padx=(0, 10))
        
        dropdown = Combobox(input_frame, values=list(self.impact_categories.keys()))
        dropdown.pack(side=RIGHT, fill=BOTH)
        dropdown.current(0)
        dropdown.bind("<<ComboboxSelected>>", lambda x:self._update_plot_from_combo(x))

        checkbox_frame = Frame(plot_frame, bg=self.plotter_bg_color)
        checkbox_frame.pack(fill='both', expand=True, anchor='w')

        var = BooleanVar(value=True)
        self.plot_models["Model_0"] = var
        checkbox = Checkbutton(checkbox_frame, text="Model_0" , variable=var, command=self.update_plot,
                               bg=self.plotter_bg_color, fg='white', selectcolor="gray")
        checkbox.pack(side=LEFT)  
        self.plot_checkboxes["Model_0"]  = checkbox

        self.checkbox_frame = checkbox_frame

        self.plot_data = {"Model_0":{}}
        for impact in self.impact_categories.keys():
            self.plot_data["Model_0"][impact] = {'A1':0.0, 'A2':0.0, 'A3':0.0}
        
        # TODO: Add type of plot
        # TODO: standard names for the plot types?
        self.plot = self.create_plot(dropdown.get())
        
        canvas_plot = FigureCanvasTkAgg(self.plot.fig, master=plot_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

        return plot_frame, canvas_plot
    
    def create_menubar(self):

        menubar = Menu(self, tearoff=False)
        self.config(menu=menubar)

        self.create_file_menu(menubar)
        self.create_edit_menu(menubar)
        self.create_database_menu(menubar)
        self.create_analysis_menu(menubar)
        self.create_view_menu(menubar)
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

        self.bind_all("<Control-plus>", self.zoom_in)  # Ctrl + for zooming in
        self.bind_all("<Control-minus>", self.zoom_out)  # Ctrl - for zooming out

    def create_canvas_bindings(self, canvas):

        canvas.bind("<ButtonPress-3>", self.start_pan)  # Right mouse button for panning
        canvas.bind("<B3-Motion>", self.do_pan)
        canvas.bind("<MouseWheel>", self.zoom)  # Mouse wheel for zoom

    def set_protocols(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


if __name__ == "__main__":
    app = ProcessVisualizer()
    app.mainloop()
