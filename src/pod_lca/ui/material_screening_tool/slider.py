from numpy import power, ceil, log10

from tkinter import Scale
from tkinter import HORIZONTAL


class Slider(Scale):

    def __init__(self, root, txt, min, max, resolution, width, length, command):
        super().__init__(
            master=root,
            label=txt,
            from_=min,
            to=max,
            resolution=resolution,
            length=length,
            orient=HORIZONTAL,
            command=command,
        )
        self.rect = None
        self.temp_in_ = None
        self.temp_x = None
        self.temp_y = None
        self._always_on = False
        self._never_show = True

    def update_value(self, value):

        max = self.cget("to")
        if float(value) > max:
            new_max = power(10, ceil(log10(value)))
            self.config(to=new_max)

        res = self.cget("resolution")
        decimal_point_at = str(value)[::-1].find(".")
        if decimal_point_at > 1:
            if res > 1 / power(10, decimal_point_at):
                new_res = 1 / power(10, decimal_point_at)
                self.config(resolution=new_res)

        self.set(value)

    def get_value(self):
        return self.get()

    def update_slider(self, min, max, res):

        self.config(from_=min, to=max, resolution=res)

        return self

    def set_always_visible(self):

        self._always_on = True
        self._never_show = False
        self.show_slider(None)

    def show_slider(self, event):
        if not self._never_show:
            self.place(in_=self.temp_in_, x=self.temp_x, y=self.temp_y)

    def hide_slider(self, event):
        if not self._always_on:
            self.place_forget()
