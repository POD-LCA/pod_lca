from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart3(Plotter):
    """
    A bar chart to visualize the impact (of a given impact category) for mutiple models with data categorized
    by the life cycle stage.

    """   
    
    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot.
        """
        
        impact_by_stage = self.calculator.get_barchart3_data(self.impact_category, self.active_models)

        width = 0.6  
        bottom = np.zeros(len(self.impact_category)) 

        for stage, impacts in impact_by_stage.items():
            p = self.ax.bar(self.impact_category, impacts, width, label=stage, bottom=bottom)
            bottom += impacts  
            self.ax.bar_label(p, label_type='center')
            
        self.ax.legend() 

    def set_labels(self): 
        """ Set plot title and axis label.
        """
                
        self.ax.set_title('Environmental Impacts by Stage')
        
    def set_grid(self):
        """ Set grids of the plot.
            Updates the y-axis height based on the maximum bar height.
        """
        pass
        
    def set_legend(self):
        """ Set legend of the plot.
        """
        pass


if __name__ == '__main__':
    pass
