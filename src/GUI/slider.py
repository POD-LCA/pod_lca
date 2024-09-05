from tkinter import Scale, Label
from tkinter import HORIZONTAL

class Slider(Scale):

    def __init__(self, root, txt, min, max, width, length, command):
        super().__init__(master=root, label=txt, from_=min, to=max, length=length, orient=HORIZONTAL, command=command)
        self.rect = None

    def update_value(self, value):
        self.set(value)

    def get_value(self):
        return self.get()
    
    # def update_position(self, canvas, slider_data):

    #     coords = canvas.coords(self.rect)
    #     self.place(in_=canvas, x=coords[0], y=coords[3])

    #     slider_data['x'] = coords[0]
    #     slider_data['y'] = coords[3]

