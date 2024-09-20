from tkinter import Frame, Canvas
from tkinter import LEFT, BOTH

class Model:

    def add_model(self):

        model_no =  len(self.models) + 1
        notebook = self.notebook

        model_new = Frame(notebook)

        model_name = "Model_" + str(model_no)
        notebook.add(model_new, text=model_name)
        notebook.pack(expand=True, fill='both')

        canvas_model = Canvas(model_new, bg=self.color_canvas, width=self.canvas_width, height=self.canvas_height)
        canvas_model.pack(side=LEFT, padx=0, pady=0, fill=BOTH)
        canvas_model.bind("<Configure>", self.on_canvas_configure)

        self.models[model_name] = canvas_model
