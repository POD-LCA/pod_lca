from GUI.GUI_inputManager import GUIInputManager
from GUI.popup import Popup
from GUI.slider import Slider

from tkinter import Frame, Button, Label
from tkinter import LEFT, DISABLED

class Transportation:

    # =================================
    # Process Objects
    # =================================

    def open_popup_transport_process(self):

        popup = Popup(self, "Create transportation process", "300x200")
        
        name =  popup._popup_input_field("Transportation by: ", default_val="vehicle")    
        life_cycle_stage = popup._popup_input_combo("Life cycle stage: ", ["A1", "A2", "A3"], default_entry=1, default_state=DISABLED)
        travel_dist = popup._popup_input_field("travel distance: ", validate_num=True, default_val=0.0)
        units = popup._popup_input_combo("units: ", ["km"])  

        button_frame = Frame(popup)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: self.create_transport_process(popup, name.get(), travel_dist.get(), units.get(), life_cycle_stage.get()))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=LEFT, padx=10)
        
    def create_transport_process(self, popup, name, qty, units, stage):

        x1, y1, x2, y2, = 50, 50, 150, 100

        prc = self.canvas.create_rectangle(50, 50, 150, 100, fill="blue", tags=("process","transportation"))

        text_x, text_y = (x1 + x2) // 2, (y1 + y2) // 2
        text_str = name + '\n' + stage
        text_item = self.canvas.create_text(text_x, text_y, text=text_str, tags="process")

        id_pack = 5
        id_x, id_y = x1 + id_pack , y1 + id_pack
        text_id = self.canvas.create_text(id_x, id_y, text=str(prc), tags="process")

        self.process_data[prc] = GUIInputManager.create_transport_process(self.project.model, name, self.project, units, float(qty), stage)
    
        slider = Slider(self.canvas, "Qty (in {})".format(units), min=0, max=100, command=lambda x: GUIInputManager.update_transport_dist(self, self.process_data[prc], x))
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