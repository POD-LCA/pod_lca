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
    A bar chart to visualize the impact of a given impact category for multiple models,
    with data categorized by life cycle stage.
    """

    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """
        Calls the calculator to generate data and sets it for plotting.
        Each model's impact by life cycle stage is displayed as grouped bars.
        """
        num_models = len(self.active_models) 
        width = 0.8 / num_models

        for i, model in enumerate(self.active_models):
            print(f"Processing Model {i}: {model}")

            impact_by_stage = self.calculator.get_barchart3_data(self.impact_category, model)
            bottom = np.zeros(len(self.impact_category))

            x_positions = np.arange(len(self.impact_category)) + i * width

            for stage, impacts in impact_by_stage.items():
                rounded_impacts = self.round_to_significant(impacts)

                p = self.ax.bar(
                    x_positions, rounded_impacts, width, 
                    label=f"{model} - {stage}", bottom=bottom
                )

                bottom += rounded_impacts 

                self.ax.bar_label(p, labels=self.format_labels(rounded_impacts), label_type='center')

        self.ax.set_xticks(np.arange(len(self.impact_category)) + width * (num_models - 1) / 2)
        self.set_x_labels()
        self.ax.legend()
        self.ax.figure.tight_layout()

    def set_x_labels(self):

        """ Set x-tick labels with impact categories and their units. """

        if isinstance(self.impact_category, list):

            labels = [
                f"{category} ({self.IMPACT_UNITS.get(category, '')})"
                for category in self.impact_category
            ]
        else:

            unit = self.IMPACT_UNITS.get(self.impact_category, '')
            labels = [f"{self.impact_category} ({unit})"]

        self.ax.set_xticklabels(labels)

    def set_labels(self):
        """ Set plot title and axis labels. """
        self.ax.set_ylabel("Impact Value")
        self.ax.set_title('Environmental Impacts by Stage')

    def set_grid(self):
        """ Set grid lines for the plot. """
        pass  # Implement as needed

    def set_legend(self):
        """ Set the legend of the plot. """
        pass  # Implement as needed


if __name__ == '__main__':
    pass
