
from numpy import power, ceil, log10

from tkinter import Scale
from tkinter import HORIZONTAL

class Slider(Scale):

    def __init__(self, root, txt, min, max, resolution, width, length, command):
        super().__init__(master=root, label=txt, from_=min, to=max, resolution=resolution,length=length, orient=HORIZONTAL, command=command)
        self.rect = None

    def update_value(self, value):

        max = self.cget("to")
        if float(value) > max:
            new_max = power(10,ceil(log10(value)))
            self.config(to=new_max)

        self.set(value)

    def get_value(self):
        return self.get()
    
    def update_slider(self, min, max, res):

        self.config(from_=min, to=max, resolution=res)

