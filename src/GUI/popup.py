from tkinter import Frame, Button, Label, Entry, Toplevel, StringVar, Radiobutton, Menu
from tkinter import LEFT, NORMAL, DISABLED
from tkinter.ttk import Combobox, Separator

class Popup(Toplevel):

    def __init__(self, master, title, shape) :
        super().__init__(master)
        
        if type(master) == Menu:
            self.visualiser = master.master
        else:
            self.visualiser = master

        main_x = self.visualiser.winfo_x()
        main_y = self.visualiser.winfo_y()

        self.title(title)
        self.geometry(shape + f"+{main_x + 50}+{main_y + 50}")
 
        self.visualiser.attributes("-disabled", True)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_popup_close)


    @staticmethod
    def _popup_input_field(master, text, validate_num=False, default_val='', width= 15):

        master = Frame(master)
        master.pack(pady=5, padx=10, anchor="w")
        
        label = Label(master, text=text)
        label.pack(side=LEFT, padx=(0, 10))
        
        if validate_num:
            vcmd = (master.register(Popup._validate_input_num), '%P')
            data = Entry(master, validate='key', validatecommand=vcmd, width=width)
        else:
            data = Entry(master, width=width)
        data.insert(0, default_val)
        data.pack(side=LEFT)

        return data
    
    @staticmethod
    def _popup_input_combo(master, text, drop_down_list, default_entry=0, default_state='readonly'):

        input_frame = Frame(master)
        input_frame.pack(pady=5, padx=10, anchor="w")
        
        label = Label(input_frame, text=text)
        label.pack(side=LEFT, padx=(0, 10))
        
        dropdown_values = drop_down_list 
        
        dropdown = Combobox(input_frame, values=dropdown_values, state=default_state)
        dropdown.pack(side=LEFT)
        dropdown.current(default_entry)

        return dropdown
    
    @staticmethod
    def _popup_label(master, text, justify='center', with_seperator=False):

        local_master = Frame(master)
        local_master.pack(pady=5, padx=10, anchor="w")

        label = Label(local_master, text=text, justify=justify)
        label.pack(side=LEFT, padx=(0, 10))

        if with_seperator:
            local_master.pack(fill='x', padx=5, pady=10)

            separator = Separator(master, orient='horizontal')
            separator.pack(fill='x', expand=True, side='left', padx=5)

        return label
    
    @staticmethod
    def _popup_radio_buttons(master, options:dict, default, cmd=None):

        selected_option = StringVar(value=default)

        for option in options:
            radio = Radiobutton(master, text=option, variable=selected_option, value=options[option], command=cmd)
            radio.pack(anchor='w', padx=50, pady=5)

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
        
    def seperator(self):

        separator = Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

    # =================================
    # Button Packs
    # =================================
    @staticmethod
    def button_custom(master, text, cmd):

        button_frame = Frame(master)
        button_frame.pack(pady=20)

        close_button = Button(button_frame, text=text, command=cmd)
        close_button.pack(side=LEFT, padx=10)


    @staticmethod
    def button_pack_OKCancelApply(master, popup, cmd):

        button_frame = Frame(master)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        close_button = Button(button_frame, text="Close", command=popup.on_popup_close)
        close_button.pack(side=LEFT, padx=10)

        import_button = Button(button_frame, text="Apply", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=True))
        import_button.pack(side=LEFT, padx=10)
    
    @staticmethod
    def button_pack_OKCancel(master, popup, cmd):

        button_frame = Frame(master)
        button_frame.pack(pady=20)

        ok_button = Button(button_frame, text="OK", command=lambda: Popup._ok_apply_button(popup, cmd, is_apply=False))
        ok_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=popup.on_popup_close)
        cancel_button.pack(side=LEFT, padx=10)

    @staticmethod
    def button_pack_Close(master, popup):

        button_frame = Frame(master)
        button_frame.pack(pady=20)

        close_button = Button(button_frame, text="Close", command=popup.on_popup_close)
        close_button.pack(side=LEFT, padx=10)

    @staticmethod
    def _ok_apply_button(popup, cmd, is_apply=False):
        """ Run command and close popup.
            Popup closed only if apply button is pushed and the command returns something other than None.
            Return of None from command is taken as an indication of an error being called and handled.
        """

        test = cmd()
        
        if not test is None:
            if not is_apply:
                popup.on_popup_close()

    def on_popup_close(self):
        self.visualiser.attributes("-disabled", False)
        self.grab_release()
        self.destroy()

        self.visualiser.lift()
        self.visualiser.focus_force()
