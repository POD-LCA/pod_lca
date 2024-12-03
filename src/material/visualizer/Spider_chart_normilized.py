from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class Spiderchart_n(Plotter):
    """
    A radar chart to visualize the impact of a given impact category for multiple models,
    with data categorized by life cycle stage.
    
    Attributes
    ----------
    normalization_factors : Dict
        Normalization factors for impacts.
        REF:The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. 
            DOI: http://hdl.handle.net/1773/41885

    """

    def __init__(self, project):
        super().__init__(project)
        self.lca_stage = 'all' # default value 

        self.normalization_factors = {
            'GWP': 24223.71, 
            'AP': 90.86,
            'EP': 0.21, 
            'ODP': 0.16, 
            'SFP': 1392.05 
        }

        self.impact_category = list(self.normalization_factors.keys())

    def set_data(self):
        """
        Sets up the data for a single radar plot with multiple models.
        Each impact category is plotted around the radar with each model represented in a different color.
        """

        # Obtain data from the calculator
        data_dict = self.calculator.get_spider_chart_data(
            self.impact_category, self.active_models, self.lca_stage)

        # Normalize the data
        data_dict = {
            impact: {
                model: self.round_to_significant(value / self.normalization_factors[impact], sig_figs=3)
                for model, value in models.items()
            }
            for impact, models in data_dict.items() if impact in self.normalization_factors
        }

        num_categories = len(self.impact_category)

        # Set up radar chart with equally spaced angles
        angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
        angles += angles[:1]  # Complete the loop

        # Clear and create polar axes
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, polar=True)

        # Plot each model on the same radar chart with different colors
        for model in self.active_models:
            # Retrieve the values for this model across all categories
            values = [data_dict[category][model] for category in self.impact_category]
            values += values[:1]  # Repeat the first value to close the loop

            # Plot this model's values on the radar chart
            self.ax.plot(angles, values, label=model)
            self.ax.fill(angles, values, alpha=0.25)  # Add fill for visibility

        # Set category labels around the radar chart
        self.ax.set_xticks(angles[:-1])     

    def set_labels(self):
        """ Set plot title. """
        self.ax.set_title("Normilized Impact Comparison Across Models", pad=20, fontsize=14)
        self.ax.tick_params(axis='x', labelsize=10)
        self.ax.set_xticklabels(self.impact_category, fontsize=10)

    def set_grid(self):
        """ Set grid lines for the plot. """
        self.ax.grid(True, linestyle='--', linewidth=0.5)

    def set_legend(self):
        """ Set the legend of the plot. """
        self.ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=10)


if __name__ == '__main__':
    pass
