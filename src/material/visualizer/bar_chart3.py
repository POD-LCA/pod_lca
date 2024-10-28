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
        num_models = len(self.active_models)  # Number of models
        width = 0.8 / num_models  # Adjust width to avoid overlapping bars
        print ("acccctiv", self.active_models)
        # Iterate over models and log their data for inspection
        for i, model in enumerate(self.active_models):
            print(f"Processing Model {i}: {model}")

            # Get impact data categorized by life cycle stage
            impact_by_stage = self.calculator.get_barchart3_data(self.impact_category, model)
            print(f"Impact Data for Model {i}: {impact_by_stage}")

            # Initialize the bottom positions for stacking bars
            bottom = np.zeros(len(self.impact_category))

            # Calculate the x-position offset for each model
            x_positions = np.arange(len(self.impact_category)) + i * width

            # Plot each stage's impact data as a stacked bar
            for stage, impacts in impact_by_stage.items():
                print(f"Stage: {stage}, Impacts: {impacts}")  # Debug output

                p = self.ax.bar(
                    x_positions, impacts, width, label=f"{model} - {stage}", bottom=bottom
                )
                bottom += impacts  # Update bottom for the next stacked bar
                self.ax.bar_label(p, label_type='center')  # Center labels

        # Align x-ticks to the center of grouped bars
        self.ax.set_xticks(np.arange(len(self.impact_category)) + width * (num_models - 1) / 2)
        self.ax.set_xticklabels(self.impact_category)

        # Add legend after plotting all models
        self.ax.legend()

        # Adjust layout to prevent overlap
        self.ax.figure.tight_layout()

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
