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
    A bar chart to visualize the impact (of a given impact category) for multiple models 
    with data categorized by the life cycle stage.
    """

    def __init__(self, project):
        super().__init__(project)

    def set_data(self):

        """ Calls calculator to generate the data and then sets them in the plot. """

        stages = ('A1', 'A2', 'A3') 
        stages_nos = np.arange(len(stages))
        width = 0.4
        model_no = 0

        for model in self.active_models:
            _, _, _, impacts = self.calculator.get_barchart2_data(self.impact_category, model)
            bottom = np.zeros(3)

            for stage, impact in impacts.items():

                rounded_impact = self.round_to_significant(impact)
                p = self.ax.bar(
                    stages_nos + (model_no * width), rounded_impact, width, 
                    label=stage, bottom=bottom
                )
                bottom += rounded_impact 

                self.ax.bar_label(p, labels=self.format_labels(rounded_impact), label_type='center')

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
