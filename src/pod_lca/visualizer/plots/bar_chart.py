
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from numpy import arange

from ...utilities import config
from ...utilities import MathFuncs
from ...visualizer import AbstractPlot


class BarChart(AbstractPlot):
    """Bar chart with data upto three levels: category, group, and component levels.
    """

    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================ 
    def draw(self, data, title, x_label, y_label):
        """ Draw the bar chart.
        
        Parameters
        ----------
        data : dict
            Data to be plotted, given in one of the following dictionaries:
            standard bar chart - {category (str) : value (float)};
            grouped bar chart - {category (str) : {group (str) : value (float)}};
            grouped bar chart with components - {category (str) : {group (str) : {component (str) : value (float)}}}.
        title : str
            Title of the barchart.
        x_label : str
            X-label of the barchart.
        y_label : str
            Y-label of the barchart.
        """
        self.get_plot().clear_plot()

        COLOUR_BASE = config['Preferences']['COLOUR_BASE']
        COLOUR_PALETTES = config['Preferences']['COLOUR_PALETTES']
        COLOUR_ORDER_LIST = config['Preferences']['COLOUR_ORDER_LIST']

        categories = list(data.keys())
        if not (isinstance(data[categories[0]], float) or isinstance(data[categories[0]], int)):
            groups = list(next(iter(data.values())).keys())
        else:
            groups = None

        gap = 0.2
        x = arange(len(categories))
          
        for i, (category, category_data) in enumerate(data.items()):
            if isinstance(category_data, float) or isinstance(category_data, int):
                width = (1.0 - gap)
                height = MathFuncs.round_to_significant([category_data])[0]
                self.get_plot().draw_bar(x[i], height, width, label=f'{category}', color=COLOUR_PALETTES[COLOUR_ORDER_LIST[i]][COLOUR_BASE], label_pos='center')  
            else:
                width = (1.0 - gap) / len(categories)
                for j, (group, group_data) in enumerate(category_data.items()):
                    pos = j - ((len(categories) - 1) *(width)/2) + (i * width)
                    if isinstance(group_data, float) or isinstance(group_data, int):
                        height = MathFuncs.round_to_significant([group_data])[0]
                        self.get_plot().draw_bar(pos, height, width, label=None, color=COLOUR_PALETTES[COLOUR_ORDER_LIST[i]][COLOUR_BASE], label_pos='center')
                    else:
                        bottom = 0
                        counter = 0
                        sorted_group_data = dict(sorted(group_data.items(), key=lambda item: item[1], reverse=True))
                        for component_name, value in sorted_group_data.items():
                            height = MathFuncs.round_to_significant([value])[0]
                            self.get_plot().draw_bar(pos, height, width, bottom=bottom, label=f'{component_name} - ({category})', color=COLOUR_PALETTES[COLOUR_ORDER_LIST[i]][counter], label_pos='center')
                            bottom += height
                            counter += 1
                    
        if isinstance(category_data, float) or isinstance(category_data, int):
            self.get_plot().set_xticks(range(len(categories)), categories)
            self.get_plot().set_legend(title=x_label)
        else:
            if isinstance(group_data, float) or isinstance(group_data, int):
                self.get_plot().set_xticks(range(len(groups)), groups)
                colors = [COLOUR_PALETTES[COLOUR_ORDER_LIST[i]][COLOUR_BASE] for i in arange(len(categories))]
                labels = categories
                self.get_plot().set_legend(colors, labels)
            else:
                self.get_plot().set_xticks(range(len(groups)), groups)
                self.get_plot().set_legend(title=x_label)

        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()


if __name__ == '__main__':
    pass
       