
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
    A bar chart to visualize the impact (of a given impact category) for multiple models 
    with data categorized by the life cycle stage.
    """

    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot. """
        stages, bar_height_dict = self.calculator.get_barchart_data(
            self.impact_category, self.active_models
        )

        width = 0.4
        model_no = 0

        for model, model_data in bar_height_dict.items():
            stage_no = 0
            color = self.bar_colors[model_no]

            for stage, value in model_data.items():
                rounded_value = self.round_to_significant([value])[0]

                rects = self.ax.bar(
                    stage_no + model_no * width, rounded_value, width, 
                    label=f'{stage}({model})', color=color
                )

                self.ax.bar_label(rects, labels=self.format_labels([rounded_value]), padding=3)

                stage_no += 1

            model_no += 1

        self.ax.set_xticks(range(len(stages)), stages)

    def set_labels(self): 
        """ Set plot title and axis labels including the unit for the impact category. """
        self.ax.set_xlabel("Life Cycle Stage")

        unit = self.IMPACT_UNITS.get(self.impact_category, '')
        self.ax.set_ylabel(f'{self.impact_category} Impact ({unit})')

        self.ax.set_title('Life Cycle Stages')

    def set_legend(self):
        """ Set the legend of the plot. """
        self.ax.legend(title='Life cycle stage color', loc='upper left', ncols=3)


if __name__ == '__main__':
    pass
