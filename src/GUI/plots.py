from GUI.GUI_outputManager import GUIOutputManager

from matplotlib import pyplot
from numpy import linspace

class Plots:

    def set_plot_data(self):

        self.plot_data = GUIOutputManager.get_output_data(self.project, self.impact_categories)

        return self.plot_data
    
    def get_plot_data(self):

        return self.plot_data

    def create_plot(self):
        
        plot_data = self.get_plot_data()[self.plot_impact_cat]
        life_cycle_stages = list(plot_data.keys())
        values = list(plot_data.values())
        
        fig, ax = pyplot.subplots(figsize = (10, 5))

        ax.bar(life_cycle_stages, values, color ='red', width = 0.4)

        ax.set_xlabel("Life Cycle Stage")
        ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        ax.set_title("title")

        self.ax = ax

        return fig
    
    def update_plot(self):

        plot_data = self.get_plot_data()[self.plot_impact_cat]  
        life_cycle_stages = list(plot_data.keys())
        values = list(plot_data.values())
        
        self.ax.clear()  
        
        self.ax.bar(life_cycle_stages, values, color='red', width=0.4)
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        self.ax.set_title("title")
        
        self.canvas_plot.draw() 

    def _update_plot_from_combo(self, event):
        
        self.plot_impact_cat = event.widget.get()
        self.update_plot()
