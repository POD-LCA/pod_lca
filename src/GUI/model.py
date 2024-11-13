from GUI.GUI_inputManager import GUIInputManager

from tkinter import Frame, Canvas, Checkbutton, BooleanVar
from tkinter import LEFT, BOTH

class ModelMixin:

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

        self.update_plot()

        return model
