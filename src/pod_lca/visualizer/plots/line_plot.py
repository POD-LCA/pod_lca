
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from ...utilities import config
from ...visualizer import AbstractPlot


class LinePlot(AbstractPlot):
    """Line chart with multiple lines.
    """

    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================ 
    def draw(self, data, title, x_label, y_label, colors=None):
        """ Draw the line plot.
        
        Parameters
        ----------
        data : dict or list
            Data to be plotted, given in one of the following dictionaries: \n
            - standard line plot, in pairs - [(**x_value** (:class:`float`), **y_value** (:class:`float`))];
            - standard line plot, in lists - [[**x_values** (:class:`float`)], [**y_values** (:class:`float`)]]
            - multiple line plot - {**category** (:class:`str`) : [(**x_value** (:class:`float`), **y_value** (:class:`float`))]};
        title : str
            Title of the barchart.
        x_label : str
            X-label of the barchart.
        y_label : str
            Y-label of the barchart.
        colors : str or list of str
            Colors of the line plots.
        """
        self.get_plot().clear_plot()

        if isinstance(data, dict):
            if colors is None:
                colors = config['Preferences']['COLOUR_ORDER_LIST']
            counter = 0
            for label, xy_data in data.items():
                x_data, y_data = zip(*xy_data)
                colors = config['Preferences']['COLOUR_ORDER_LIST']
                self.get_plot().draw_line(x_data, y_data, label, colors[counter])
                counter += 1
        elif isinstance(data, list):
            if colors is None:
                colors = config['Preferences']['COLOUR_ORDER_LIST'][0]
            self.get_plot().draw_line(data[0], data[1], None, colors)
                
        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()
        self.get_plot().set_legend()


if __name__ == '__main__':
    pass
       