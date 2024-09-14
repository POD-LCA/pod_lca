from GUI.GUI_outputManager import GUIOutputManager

from matplotlib import pyplot
import mplcursors
from numpy import log10, power, ceil

class Plots:

    def set_plot_data(self):

        self.plot_data = GUIOutputManager.get_output_data(self.project, self.impact_categories)

        return self.plot_data
    
    def get_plot_data(self):

        return self.plot_data
    
    def clear_plot_data(self):

        self.plot_data.clear()
        for impact in self.impact_categories.keys():
            self.plot_data[impact] = {'A1':0.0, 'A2':0.0, 'A3':0.0}

    def create_plot(self):
        
        plot_data = self.get_plot_data()[self.plot_impact_cat]
        life_cycle_stages = list(plot_data.keys())
        values = list(plot_data.values())
        
        fig, ax = pyplot.subplots(figsize = (10, 5))

        ax.bar(life_cycle_stages, values, color ='#8f2ab0', width = 0.4)

        ax.set_xlabel("Life Cycle Stage")
        ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        ax.set_title("title")
        ax.set_ylim([0, 10])

        crs = mplcursors.cursor(ax,hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(f'Value: {sel.target[1]:.2f}'))

        self.ax = ax
        pyplot.grid(True)

        return fig
    
    def update_plot(self):

        plot_data = self.get_plot_data()[self.plot_impact_cat]  
        life_cycle_stages = list(plot_data.keys())
        values = list(plot_data.values())
        
        self.ax.clear()
        pyplot.grid(True)  
        
        self.ax.bar(life_cycle_stages, values, color='#8f2ab0', width=0.4)
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        self.ax.set_title("title")
        self.ax.set_ylim([0, max(power(10,ceil(log10(max(values)))),10)])

        crs = mplcursors.cursor(self.ax, hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(f'{life_cycle_stages[int(sel.index)]} : {sel.artist[sel.target.index].get_height():.1f}'))
        
        
        self.canvas_plot.draw() 

    def _update_plot_from_combo(self, event):
        
        self.plot_impact_cat = event.widget.get()
        self.update_plot()
