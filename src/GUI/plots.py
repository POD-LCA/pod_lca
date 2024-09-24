from GUI.GUI_outputManager import GUIOutputManager

from matplotlib import pyplot
from numpy import log10, power, ceil, arange

class Plots:

    def set_plot_data(self):
        
        plot_data = {}
        for model in self.plot_models:
            if self.plot_models[model].get():
                plot_data[model] = GUIOutputManager.get_output_data(self.project, self.impact_categories, model)

        self.plot_data = plot_data
    
    def get_plot_data(self):

        self.set_plot_data()

        return self.plot_data
    
    def clear_plot_data(self):

        self.plot_data.clear()
        for impact in self.impact_categories.keys():
            self.plot_data[impact] = {'A1':0.0, 'A2':0.0, 'A3':0.0}

    def create_plot(self):
        
        plot_data = self.get_plot_data()
        stages = []
        grouped_data = {}
        for model in plot_data:
            grouped_data[model] = []
            for stage in plot_data[model][self.plot_impact_cat]:
                grouped_data[model].append(plot_data[model][self.plot_impact_cat][stage])
                stages.append(stage)
        
        fig, ax = pyplot.subplots(layout='constrained')

        x = arange(len(set(stages)))
        width = 0.4
        multiplier = 0

        for model, value  in grouped_data.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, value, width, label=model)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        ax.set_xlabel("Life Cycle Stage")
        ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        ax.set_xticks(x + width, set(stages))
        ax.set_title("title")
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim([0, 10])

        self.ax = ax
        pyplot.grid(True)

        return fig
    
    def update_plot(self):

        plot_data = self.get_plot_data() 
        stages = []
        grouped_data = {}
        for model in plot_data:
            grouped_data[model] = []
            for stage in plot_data[model][self.plot_impact_cat] :
                grouped_data[model].append(plot_data[model][self.plot_impact_cat][stage])
                stages.append(stage)

        self.ax.clear()
        pyplot.grid(True)  

        x = arange(len(set(stages)))
        width = 0.4
        multiplier = 0

        max_val = 0.0
        for model, value  in grouped_data.items():
            offset = width * multiplier
            rects = self.ax.bar(x + offset, value, width, label=model)
            self.ax.bar_label(rects, padding=3)
            multiplier += 1
            max_val = max(max_val, max(value))
        
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(self.plot_impact_cat + " (" + self.impact_categories[self.plot_impact_cat] + ")")
        self.ax.set_title("title")
        self.ax.set_xticks(x + width, set(stages))
        self.ax.legend(loc='upper left', ncols=3)
        if max_val > 0.0:
            self.ax.set_ylim([0, max(power(10,ceil(log10(max_val))),10)])
        else:
            self.ax.set_ylim([0, 10])
            
        self.canvas_plot.draw() 

    def _update_plot_from_combo(self, event):
        
        self.plot_impact_cat = event.widget.get()
        self.update_plot()
