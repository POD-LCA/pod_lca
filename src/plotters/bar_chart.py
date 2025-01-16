from plotters.matplotlib_plotter import Plotter
from lca_modules.material.calculator import Calculator

from numpy import arange
import matplotlib.pyplot as plt

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart(Plotter):
    """Bar chart with data upto three levels: category, group, and component levels.
    """

    def show(self, data, title, x_label, y_lablel):

        self.ax.clear()

        categories = list(data.keys())
        if not isinstance(data[categories[0]], float):
            groups = list(next(iter(data.values())).keys())
            no_groups = len(groups)
        else:
            groups = None
            no_groups = 1

        gap = 0.2
        x = arange(len(categories))
        width = (1.0 - gap) / no_groups
        
        for i, (category, category_data) in enumerate(data.items()):
            if isinstance(category_data, float):
                height = self.round_to_significant([category_data])[0]
                rect = self.ax.bar(x[i], height, width, label=f'{category}')
                self.ax.bar_label(rect, label_type='center')
                self.ax.set_xticks(range(len(categories)), categories)
            else:
                for j, (group, group_data) in enumerate(category_data.items()):
                    pos = j - (1.0 - gap - width)/2 + (i * width)
                    if isinstance(group_data, float):
                        height = self.round_to_significant([group_data])[0]
                        rect = self.ax.bar(pos, height, width, label=f'{group} ({category})')
                        self.ax.bar_label(rect, label_type='center')
                    else:
                        bottom = 0
                        sorted_group_data = dict(sorted(group_data.items(), key=lambda item: item[1], reverse=True))
                        for component_name, value in sorted_group_data.items():
                            height = self.round_to_significant([value])[0]
                            rect = self.ax.bar(pos, height, width, bottom, label=f'{component_name}')
                            self.ax.bar_label(rect, label_type='center')
                            bottom += height
                    self.ax.set_xticks(range(no_groups), groups)

        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_lablel)
        self.ax.set_title(title)

        self.set_grid()
        self.set_legend()

        plt.show()

        #TODO setting colors