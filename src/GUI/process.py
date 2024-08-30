from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider

from tkinter import Menu, Frame, Button, Label
from tkinter import LEFT

class Process:

    # =================================
    # Process Objects
    # =================================

    def open_popup_process(self):

        popup = Popup(self, "Create process", "300x200")
        
        name =  popup._popup_input_field("Process name: ", default_val="new Process")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"])   
        qty = popup._popup_input_field("qty: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["m3", "kg"])  

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_process(popup, name.get(), qty.get(), units.get(), life_cycle_stage.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_process(self, popup, name, qty, units, stage):

        height = 50
        width = 150
        x1, y1, x2, y2 = height*self.scale, height*self.scale, width*self.scale, width*self.scale

        prc = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="process")

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = self.canvas.create_text(text_x, text_y, text=text_str, tags="process")

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = self.canvas.create_text(id_x, id_y, text=str(prc), tags="process")

        self.process_data[prc] = GUIInputManager.create_process(self.project.model, name, units, float(qty), stage)
    
        slider = Slider(self.canvas, "Qty (in {})".format(units), min=0, max=100, width=self.default_slider_width, command=lambda x: GUIInputManager.update_qty(self, self.process_data[prc], x))
        self.sliders.append({"widget": slider, "x": x1, "y": y2, "width": self.default_slider_width})
        slider.place(in_=self.canvas, x=x1, y=y2)
        slider.update_value(qty)

        group_tag = f"group_{prc}"
        self.canvas.addtag_withtag(group_tag, prc)
        self.canvas.addtag_withtag(group_tag, text_item)
        self.canvas.addtag_withtag(group_tag, text_id)
        
        self.canvas.tag_bind(prc, "<ButtonPress-1>", self.on_start_drag)
        self.canvas.tag_bind(prc, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(prc, "<ButtonRelease-1>", self.on_stop_drag)
        self.canvas.tag_bind(prc, "<Button-3>", self.show_process_context_menu) 

        self.canvas.tag_bind(group_tag, "<B1-Motion>", lambda event: self.move_slider(event, slider))

        # self.tooltips[prc] = Tooltip(self.canvas, f"This is a process")

        popup.destroy()

    def update_process(self):
        
        pass


    def show_process_context_menu(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Set Impacts", command=lambda: self.set_impacts(item, process=True))
        self.context_menu.add_command(label="View Unit Impacts", command=lambda: self.view_impacts(item, process=True))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Change life cycle stage", command=lambda: self.update_life_cycle_stage(item, process=True))
        self.context_menu.post(event.x_root, event.y_root)