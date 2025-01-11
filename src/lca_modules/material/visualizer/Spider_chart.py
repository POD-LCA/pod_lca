from plotters.matplotlib_plotter import Plotter
from lca_modules.material.calculator import Calculator

import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class Spiderchart(Plotter):
    """ A radar plot indicating the impact (of a given impact category) for multiple models, at a given life cycle stage.

    """

    def __init__(self, project):
        super().__init__(project)
        self.lca_stage = 'all' # default value

    def set_data(self):
        """
        Calls the calculator to generate data and sets it for plotting.
        """

        if isinstance(self.impact_category, list):
            self.impact_category = self.impact_category[0]
            print("A list of impact categories given. Graph plotted for the first category in the list.")
        
        data_dict = Calculator.get_spider_chart_data([self.impact_category], self.active_models, self.lca_stage)
        values = list(data_dict[self.impact_category].values())

        # Calculate the angle for each model
        num_models = len(self.active_models)
        angles = np.linspace(0, 2 * np.pi, num_models, endpoint=False).tolist()
        
        # Close the circle by repeating the first value at the end
        values += values[:1]
        angles += angles[:1]
        
        # Clear and create polar axes
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, polar=True)
        
        # Plot data for the category
        self.ax.plot(angles, values, label=self.impact_category)
        self.ax.fill(angles, values, alpha=0.25)
        
        # Set model names as labels on the radar chart
        self.ax.set_xticks(angles[:-1])
   
    def set_labels(self):
        """ Set plot title and axis labels. """

        self.ax.set_title(f"Radar Plot for {self.impact_category} in LC stage: {self.lca_stage}")
        self.ax.set_xticklabels(self.active_models)

    def set_grid(self):
        """ Set grid lines for the plot. """
        pass

    def set_legend(self):
        """ Set the legend of the plot. """
        pass


if __name__ == '__main__':
    pass
