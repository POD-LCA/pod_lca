from tkinter import Scale
from tkinter import HORIZONTAL

class Slider(Scale):

    def __init__(self, root, txt, min, max, resolution, width, length, command):
        super().__init__(master=root, label=txt, from_=min, to=max, resolution=resolution,length=length, orient=HORIZONTAL, command=command)
        self.rect = None

    def update_value(self, value):
        self.set(value)

    def get_value(self):
        return self.get()
    
    def update_slider(self, min, max, res):

        self.config(from_=min, to=max, resolution=res)

