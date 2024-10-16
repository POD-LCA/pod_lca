from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart2(Plotter):
    """
    A bar chart to visualize the impact (of a given impact category) for mutiple models with data categorized
    by the life cycle stage.

    """   
    
    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot.
        """

        data_name, data_qty, data_len, impacts = self.calculator.get_barchart2_data(self.impact_category, self.active_models)

        stages = ('A1', 'A2', 'A3')
        width = 0.6  
        bottom = np.zeros(3)

        for stage, impact in impacts.items():
            p = self.ax.bar(stages, impact, width, label=stage, bottom=bottom)
            bottom += impact
            self.ax.bar_label(p, label_type='center')

        self.ax.set_title('Life cycle stages')
        self.ax.legend()   

    def set_labels(self): 
        """ Set plot title and axis label.
        """
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(f'{self.impact_category} Impact')
        
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
