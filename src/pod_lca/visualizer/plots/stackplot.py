
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from ...utilities import config
from ...visualizer import AbstractPlot


class Stackplot(AbstractPlot):
    """Stackplot.
    """

    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================ 
    def draw(self, x_data, y_data, title, x_label, y_label, colors=None):
        """ Draw the bar chart.
        
        Parameters
        ----------
        x_data : list or array
            X data.
        y_data : dict or list
            Data to be plotted, given in one of the following dictionaries. The length of each list should match the dimensions of **x_data** list. \n
            - list of lists - [[y1], [y2], ... , [yn]];
            - dict - {**data label** (:class:`str`): [y1], ... , **data label** (:class:`str`): [yn]}
        title : str
            Title of the barchart.
        x_label : str
            X-label of the barchart.
        y_label : str
            Y-label of the barchart.
        colors : list of str
            Colors of each stack.
        """
        self.get_plot().clear_plot()
 
        if isinstance(y_data, dict):
            label_lst = []
            y_data_lst = []
            for label, lst in y_data.items():
                y_data_lst.append(lst)
                label_lst.append(label)
            y_data = y_data_lst

        if colors is None:
            color_idxs =  [i % len(config['Preferences']['COLOUR_ORDER_LIST']) for i in range(len(y_data))]
            colors = [config['Preferences']['COLOUR_ORDER_LIST'][i] for i in color_idxs]

        self.get_plot().draw_stackplot(x_data, y_data, label_lst, colors)
        
        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()
        self.get_plot().set_legend()


if __name__ == '__main__':
    pass