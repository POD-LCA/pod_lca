from material.visualizer.bar_chart import BarChart
from material.visualizer.bar_chart2 import BarChart2
from material.visualizer.bar_chart3 import BarChart3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import RIGHT

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
    
    def replace_figure(self, plot_frame, impact_cat, plot_type):

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
        self.canvas_plot.figure =  plot.fig
        self.canvas_plot.draw()

    def update_plot(self):

        model_lst = []
        for model in self.plot_models:
            if self.plot_models[model].get():
                model_lst.append(model)

        self.plot.set_active_models(model_lst)
        self.plot.draw()
        self.canvas_plot.draw()

    def _update_plot_from_combo(self, event):
        
        self.plot.set_impact_category(event.widget.get())
        self.update_plot()
