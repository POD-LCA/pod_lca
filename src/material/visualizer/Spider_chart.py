from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class Spiderchart(Plotter):
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

        data_dict = self.calculator.get_spider_chart_data(
            self.impact_category, self.active_models, self.lca_stage)

        categories = list(data_dict.keys())  # Environmental impact categories
        models = list(data_dict[categories[0]].keys())  # Model names
        
        # Set up a radar plot for each category
        for category in categories:
            # Data for this category
            values = list(data_dict[category].values())
            
            # Number of models
            num_models = len(models)
            
            # Calculate the angle for each model
            angles = np.linspace(0, 2 * np.pi, num_models, endpoint=False).tolist()
            
            # Close the circle by repeating the first value at the end
            values += values[:1]
            angles += angles[:1]
            
            # Create the radar plot for this category
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            
            # Plot data for the category
            ax.plot(angles, values, label=category)
            ax.fill(angles, values, alpha=0.25)
            
            # Set model names as labels on the radar chart
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(models)
            
            # Add title for the category
            plt.title(f"Radar Plot for {category}")

            #plt.show()


    
    def set_x_labels(self):

        """ Set x-tick labels with impact categories and their units. """


    def set_labels(self):
        """ Set plot title and axis labels. """


    def set_grid(self):
        """ Set grid lines for the plot. """
        pass  # Implement as needed

    def set_legend(self):
        """ Set the legend of the plot. """
        pass  # Implement as needed


if __name__ == '__main__':
    pass
