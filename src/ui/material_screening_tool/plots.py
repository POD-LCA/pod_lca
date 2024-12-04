from lca_modules.material.visualizer.bar_chart import BarChart
from lca_modules.material.visualizer.bar_chart2 import BarChart2
from lca_modules.material.visualizer.bar_chart3 import BarChart3
from lca_modules.material.visualizer.Spider_chart import Spiderchart
from lca_modules.material.visualizer.Spider_chart_normilized import Spiderchart_n


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import RIGHT, LEFT, Radiobutton, Checkbutton

class PlotsMixin:

    def create_figure(self, plot_frame, impact_cat, plot_type='Bar chart 1'):
        
        model_lst = []
        for model in self.plot_models:
            if self.plot_models[model].get():
                model_lst.append(model)
        
        if plot_type == 'Bar chart 1':
            plot = BarChart(self.project)
        elif plot_type == 'Bar chart 2':
            plot = BarChart2(self.project)
        elif plot_type == 'Bar chart 3':
            plot = BarChart3(self.project)
        else:
            raise NotImplementedError
        
        plot.set_active_models(model_lst)
        plot.set_impact_category(impact_cat)
        plot.draw()

        self.plot = plot

        canvas_plot = FigureCanvasTkAgg(plot.fig, master=plot_frame)
        canvas_plot.draw()
        
        canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

        return canvas_plot
    
    def replace_figure(self, plot_frame, plot_type):

        self.canvas_plot.get_tk_widget().pack_forget()
        self.canvas_plot = None

        model_lst = []
        for model in self.plot_models:
            if self.plot_models[model].get():
                model_lst.append(model)
        
        if plot_type == 'Bar chart 1':
            self.allow_plot_multiple_impact_categories = False
            self.create_checkbuttons()
            plot = BarChart(self.project)
        elif plot_type == 'Bar chart 2':
            self.allow_plot_multiple_impact_categories = False
            self.create_checkbuttons()
            plot = BarChart2(self.project)
        elif plot_type == 'Bar chart 3':
            self.allow_plot_multiple_impact_categories = True
            self.create_checkbuttons()
            plot = BarChart3(self.project)
        elif plot_type == 'Radar plot':
            self.allow_plot_multiple_impact_categories = False
            self.create_checkbuttons()
            plot = Spiderchart(self.project)
        elif plot_type == 'Radar plot (normalized)':
            self.allow_plot_multiple_impact_categories = True
            self.create_checkbuttons(setall=True)
            plot = Spiderchart_n(self.project)
        else:
            raise NotImplementedError
        
        plot.set_active_models(model_lst)
        plot.set_impact_category(self.get_impact_selection())
        plot.draw()

        self.plot = plot

        self.canvas_plot = FigureCanvasTkAgg(plot.fig, master=plot_frame)
        self.canvas_plot.draw()
        
        self.canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

    def update_plot(self):
        
        if not self.resetting_plot:
            model_lst = []
            for model in self.plot_models:
                if self.plot_models[model].get():
                    model_lst.append(model)

            self.plot.set_active_models(model_lst)
            self.plot.set_impact_category(self.get_impact_selection())
            self.plot.draw()
            self.canvas_plot.draw()

    def _update_plot_from_combo(self, event):
        
        self.plot.set_impact_category(event.widget.get())
        self.update_plot()


# ============================================
# UTILS
# ============================================

    def create_checkbuttons(self, setall=False):

        # reset values
        self.resetting_plot = True
        if self.allow_plot_multiple_impact_categories:
            for var in self.impact_var_list:
                if setall:
                    var.set(True)
                else:
                    var.set(False)
            if not setall:
                self.impact_var_list[0].set(True)
        else:
            self.impact_single_var.set(0)

        # create buttons
        options = list(self.impact_categories.keys())
        for widget in self.input_frame_impact_cat.winfo_children():
            widget.destroy()

        if self.allow_plot_multiple_impact_categories:
            checkbuttons = [
                Checkbutton(
                    self.input_frame_impact_cat,
                    text=option,
                    variable=self.impact_var_list[i],
                )
                for i, option in enumerate(options)
            ]
        else:
            checkbuttons = [
                Radiobutton(
                    self.input_frame_impact_cat,
                    text=option,
                    variable=self.impact_single_var,
                    value=i,
                )
                for i, option in enumerate(options)
            ]

        for btn in checkbuttons:
            btn.pack(side=LEFT, padx=5)
        self.resetting_plot = False

    def get_impact_selection(self):

        options = list(self.impact_categories.keys())

        if self.allow_plot_multiple_impact_categories:
            selected_options = [option for option, var in zip(options, self.impact_var_list) if var.get()]
        else:
            selected_index = self.impact_single_var.get()
            if selected_index != -1:
                selected_options = options[selected_index]
            else:
                selected_options = []
        
        return selected_options
