from plotters.matplotlib_plotter import Plotter

import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart2(Plotter):
    """ Bar chart to visualize impacts (of a given impact category) for multiple models by life cycle stage---i.e., a bar for life cycle stage of a given model, 
       and bars grouped by life cycle stage. In each bar, the contribution from different items are identified. #TODO: identify only hotspots and rest categorized as 'others'.
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
            _, _, _, impacts = self.calculator.get_barchart2_data(self.impact_category, model)
            bottom = np.zeros(3)

            for stage, impact in impacts.items():

                rounded_impact = self.round_to_significant(impact)
                p = self.ax.bar(
                    stages_nos - (1.0 - gap - width)/2 + (model_no * width), rounded_impact, width, 
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

