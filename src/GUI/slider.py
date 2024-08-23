from tkinter import Scale
from tkinter import HORIZONTAL

class Slider(Scale):

    def __init__(self, label, min, max, command):
        super().__init__(from_=min, to=max, orient=HORIZONTAL, command=command)
        self.label = label

    def update_value(self, value):
        self.set(value)

    def get_value(self):
        return self.get()
