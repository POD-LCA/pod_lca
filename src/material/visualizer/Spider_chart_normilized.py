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
    """

    def __init__(self, project):
        super().__init__(project)

        # Normalization values for each impact category
        self.normalization_factors = {
            'GWP': 80.71, #the real number is 24223.71
            'AP': 90.86,
            'EP': 80.62, #the real number is 0.21.62
            'ODP': 70.16, #the real number is 0.16
            'SFP': 80.05 #the real number is 1392.05
        }

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

        categories = list(data_dict.keys())  # Environmental impact categories
        models = list(data_dict[categories[0]].keys())  # Model names
        num_categories = len(categories)

        # Set up radar chart with equally spaced angles
        angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
        angles += angles[:1]  # Complete the loop

        # Initialize the plot
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        # Plot each model on the same radar chart with different colors
        for model in models:
            # Retrieve the values for this model across all categories
            values = [data_dict[category][model] for category in categories]
            values += values[:1]  # Repeat the first value to close the loop

            # Plot this model's values on the radar chart
            ax.plot(angles, values, label=model)
            ax.fill(angles, values, alpha=0.25)  # Add fill for visibility

        # Set category labels around the radar chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)

        # Customize the radar plot appearance
        self.set_x_labels(ax)
        self.set_labels(ax, "Normilized Impact Comparison Across Models")
        self.set_grid(ax)
        self.set_legend(ax)

        

    def set_x_labels(self, ax):
        """ Customize x-tick labels if needed. """
        ax.tick_params(axis='x', labelsize=10)

    def set_labels(self, ax=None, title="Normilized Impact Comparison Across Models"):
        """ Set plot title. """
        if ax is None:
            ax = self.ax  # Default to the stored axis if none provided
        ax.set_title(title, pad=20, fontsize=14)

    def set_grid(self, ax=None):
        """ Set grid lines for the plot. """
        if ax is None:
            ax = self.ax  # Use the stored axis if none provided
        ax.grid(True, linestyle='--', linewidth=0.5)

    def set_legend(self, ax=None):
        """ Set the legend of the plot. """
        if ax is None:
            ax = self.ax  # Default to self.ax if not provided
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=10)


if __name__ == '__main__':
    pass
