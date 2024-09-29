
from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart(Plotter):
    """
    A bar chart to visualize the impact (of a given impact category) for mutiple models with data categorized
    by the life cycle stage.

    """   
    
    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot.
        """
        
        stages, bar_height_dict = self.calculator.get_barchart_data(self.impact_category, self.active_models)

        width = 0.4
        model_no = 0
        for model, model_data  in bar_height_dict.items():
            stage_no = 0
            color=self.bar_colors[model_no]
            for stage, value in model_data.items():
                rects = self.ax.bar(stage_no + model_no*width, value, width, label=f'{stage}({model})', color=color)
                self.ax.bar_label(rects, padding=3)
                stage_no += 1
            model_no += 1

        self.ax.set_xticks(range(len(stages)), stages)

    def set_labels(self): 
        """ Set plot title and axis label.
        """
                
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(f'{self.impact_category} Impact')
        self.ax.set_title('Life Cycle Stages')
        
    def set_grid(self):
        """ Set grids of the plot.
            Updates the y-axis height based on the maximum bar height.
        """

        max_val = max([rect.get_height() for rect in self.ax.patches])
        if max_val > 0.0:
            self.ax.set_ylim([0, max(np.power(10,np.ceil(np.log10(max_val))),10)])
        else:
            self.ax.set_ylim([0, 10])
        plt.grid(True)
        
    def set_legend(self):
        """ Set legend of the plot.
        """

        self.ax.legend(title='Life cycle stage color', loc='upper left', ncols=3)


if __name__ == '__main__':
    pass
