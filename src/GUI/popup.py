from tkinter import Frame, Button, Label, Entry, Toplevel, StringVar, Radiobutton, Checkbutton, IntVar
from tkinter import LEFT, NORMAL, DISABLED
from tkinter.ttk import Combobox, Separator

class Popup(Toplevel):

    def __init__(self, visualiser, title, shape) :
        super().__init__(visualiser)
        self.title(title)
        self.geometry(shape)

    def _popup_input_field(self, text, validate_num=False, default_val=''):

        input_frame = Frame(self)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text=text)
        label.pack(side=LEFT, padx=(0, 10))
        
        if validate_num:
            vcmd = (self.register(Popup._validate_input_num), '%P')
            data = Entry(input_frame, validate='key', validatecommand=vcmd)
        else:
            data = Entry(input_frame)
        data.insert(0, default_val)
        data.pack(side=LEFT)

        return data
    
    def _popup_input_combo(self, text, drop_down_list, default_entry=0, default_state='readonly'):

        input_frame = Frame(self)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text=text)
        label.pack(side=LEFT, padx=(0, 10))
        
        dropdown_values = drop_down_list
        dropdown = Combobox(input_frame, values=dropdown_values, state=default_state)
        dropdown.pack(side=LEFT)
        dropdown.current(default_entry)

        return dropdown
    
    def _popup_label(self, text, justify='center', with_seperator=False, font=("Arial", 14)):

        input_frame = Frame(self)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text=text, font=font, justify=justify)
        label.pack(side=LEFT, padx=(0, 10))

        if with_seperator:
            input_frame.pack(fill='x', padx=5, pady=10)

            separator = Separator(input_frame, orient='horizontal')
            separator.pack(fill='x', expand=True, side='left', padx=5)

        return label
    
    def _popup_radio_buttons(self, options:dict, default, cmd=None):

        selected_option = StringVar(value=default)

        for option in options:
            radio = Radiobutton(self, text=option, variable=selected_option, value=options[option], command=cmd)
            radio.pack(anchor='w', padx=10, pady=5)

        return selected_option

    @staticmethod
    def update_entry_state(test, entry):
        if test:
            entry.config(state=NORMAL)
        else:
            entry.config(state=DISABLED)

    @staticmethod
    def _validate_input_num(value_if_allowed):

        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def _ok_apply_button(popup, cmd, is_apply=False):

        cmd()
        
        if not is_apply:
            popup.destroy()

    def seperator(self):

        separator = Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

