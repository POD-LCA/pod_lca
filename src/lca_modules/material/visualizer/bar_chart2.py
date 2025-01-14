from plotters.matplotlib_plotter import Plotter
from lca_modules.material.calculator import Calculator

import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart2(Plotter):
    """ Bar chart to visualize impacts (of a given impact category) for multiple models by life cycle stage---i.e., a bar for life cycle stage of a given model, 
       and bars grouped by life cycle stage. In each bar, the contribution from different items are identified.
    """

    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot. """

        if isinstance(self.impact_category, list):
            self.impact_category = self.impact_category[0]
            print("A list of impact categories given. Graph plotted for the first category in the list.")

        gap = 0.2 # gap between two groups of bars  
        stages = ('A1', 'A2', 'A3') 
        stages_nos = np.arange(len(stages))
        width = (1.0 - gap) / len(self.active_models)
        model_no = 0
        for model in self.active_models:
            _, _, _, impacts = Calculator.get_barchart2_data(self.impact_category, model)
            bottom = np.zeros(3)
            x_positions = stages_nos + model_no * width
            for label, impact in impacts.items():
                rounded_impact = self.round_to_significant(impact)
                p = self.ax.bar(
                    x_positions, rounded_impact, width, 
                    label=label, bottom=bottom
                )
                bottom += rounded_impact 
                self.ax.bar_label(p, labels=self.format_labels(rounded_impact), label_type='center')
            model_no += 1
        self.ax.set_xticks(stages_nos + width * (model_no - 1) / 2, stages)

    def set_labels(self):
        """ Set plot title and axis labels including the unit for the impact category. """

        self.ax.set_xlabel("Life Cycle Stage")
        unit = self.IMPACT_UNITS.get(self.impact_category, '')
        self.ax.set_ylabel(f'{self.impact_category} Impact ({unit})')

    def set_legend(self):
        """ Set the legend of the plot. """
        self.ax.legend(title='Life cycle stage color', loc='upper left', ncols=3)

