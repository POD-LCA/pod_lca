from lca_modules.material.calculator import Calculator
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter
from plotters.plots.bar_chart import BarChart
from plotters.plots.radar_chart import RadarChart
from ui.material_screening_tool.GUI_inputManager import GUIInputManager

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import RIGHT, LEFT, Radiobutton, Checkbutton

class PlotsMixin:

    def create_figure(self, plot_frame, impact_cat, plot_type='Bar chart 1'):
        
        model_lst = []
        for model_name in self.plot_models:
            if self.plot_models[model_name].get():
                model = GUIInputManager.get_model(self.project, model_name)
                model_lst.append(model)
      
        if plot_type == 'Bar chart 1':
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_LCstages_models(impact_cat, model_lst), f"{impact_cat} by Life Cycle Stages", "Life Cycle Stages", f"{impact_cat}")
        elif plot_type == 'Bar chart 2':
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_LCstages_models_items(impact_cat, model_lst), f"{impact_cat} by Life Cycle Stages-categorized by ", "Life Cycle Stages", f"{impact_cat}")
        elif plot_type == 'Bar chart 3':
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_impactcategorys_models_LCstage(impact_cat, model_lst), "Impacts by stages", "Impact Category", "Impact Value")
        elif plot_type == 'Radar plot':
            graph = RadarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_normalized_impacts_by_category_models(model_lst), "Impacts by category")
        else:
            raise NotImplementedError

        self.plot = graph.get_plot()

        canvas_plot = FigureCanvasTkAgg(self.plot.fig, master=plot_frame)
        canvas_plot.draw()
        
        canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

        return canvas_plot
    
    def replace_figure(self, plot_frame, plot_type):

        self.canvas_plot.get_tk_widget().pack_forget()
        self.canvas_plot = None

        model_lst = []
        for model_name in self.plot_models:
            if self.plot_models[model_name].get():
                model = GUIInputManager.get_model(self.project, model_name)
                model_lst.append(model)
        
        if plot_type == 'Bar chart 1':
            self.allow_plot_multiple_impact_categories = False
            self.create_checkbuttons() 
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_LCstages_models(self.get_impact_selection(), model_lst), f"Impacts by Life Cycle Stages", "Life Cycle Stages", f"{self.get_impact_selection()}")
        elif plot_type == 'Bar chart 2':
            self.allow_plot_multiple_impact_categories = False
            self.create_checkbuttons()
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_LCstages_models_items(self.get_impact_selection(), model_lst), f"{self.get_impact_selection()} by Life Cycle Stages-categorized by ", "Life Cycle Stages", f"{self.get_impact_selection()}")
        elif plot_type == 'Bar chart 3':
            self.allow_plot_multiple_impact_categories = True
            self.create_checkbuttons(setall=True)
            graph = BarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_impacts_by_impactcategorys_models_LCstage(self.get_impact_selection(), model_lst), "Impacts by stages", "Impact Category", "Impact Value")
        elif plot_type == 'Radar plot':
            self.allow_plot_multiple_impact_categories = True
            self.create_checkbuttons(setall=True)
            graph = RadarChart.from_plotter(MatplotlibPlotter)
            graph.draw(Calculator.get_normalized_impacts_by_category_models(model_lst), "Impacts by category")
        else:
            raise NotImplementedError
        
        self.plot = graph.get_plot()

        self.canvas_plot = FigureCanvasTkAgg(self.plot.fig, master=plot_frame)
        self.canvas_plot.draw()
        
        self.canvas_plot.get_tk_widget().pack(side=RIGHT, padx=10, pady=10)

    def update_plot(self):
        
        if not self.resetting_plot:
            model_lst = []
            for model_name in self.plot_models:
                if self.plot_models[model_name].get():
                    model = GUIInputManager.get_model(self.project, model_name)
                    model_lst.append(model)

            if self.dropdown_plot.get() == 'Bar chart 1':
                graph = BarChart.from_plot(self.plot)
                graph.draw(Calculator.get_impacts_by_LCstages_models(self.get_impact_selection(), model_lst), f"Impacts by Life Cycle Stages", "Life Cycle Stages", f"{self.get_impact_selection()}")
            elif self.dropdown_plot.get() == 'Bar chart 2':
                graph = BarChart.from_plot(self.plot)
                graph.draw(Calculator.get_impacts_by_LCstages_models_items(self.get_impact_selection(), model_lst), f"{self.get_impact_selection()} by Life Cycle Stages-categorized by ", "Life Cycle Stages", f"{self.get_impact_selection()}")
            elif self.dropdown_plot.get() == 'Bar chart 3':
                graph = BarChart.from_plot(self.plot)
                graph.draw(Calculator.get_impacts_by_impactcategorys_models_LCstage(self.get_impact_selection(), model_lst), "Impacts by stages", "Impact Category", "Impact Value")
            elif self.dropdown_plot.get() == 'Radar plot':
                graph = RadarChart.from_plotter(MatplotlibPlotter)
                graph.draw(Calculator.get_normalized_impacts_by_category_models(model_lst), "Impacts by category")
            else:
                raise NotImplementedError
            
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
        options = list(GUIInputManager.get_impact_categories().keys())
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

        options = list(GUIInputManager.get_impact_categories().keys())

        if self.allow_plot_multiple_impact_categories:
            selected_options = [option for option, var in zip(options, self.impact_var_list) if var.get()]
        else:
            selected_index = self.impact_single_var.get()
            if selected_index != -1:
                selected_options = options[selected_index]
            else:
                selected_options = []
        
        return selected_options
