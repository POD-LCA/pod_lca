from plotters.plots.abstract_plot import AbstractPlot
from utilities.settings import config


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class LinePlot(AbstractPlot):
    """Line chart with multiple lines.
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
                standard line plot - [(x_value (float), y_value (float))];
                multiple line plot - {category (str) : [(x_value (float), y_value (float))]};
            title : str
                Title of the barchart.
            x_label : str
                X-label of the barchart.
            y_label : str
                Y-label of the barchart.
        """

        self.get_plot().clear_plot()

        if isinstance(data, dict):
            counter = 0
            for label, xy_data in data.items():
                x_data, y_data = zip(*xy_data)
                self.get_plot().draw_line(x_data, y_data, label, config['Preferences']['COLOUR_ORDER_LIST'][counter])
                counter += 1
                
        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()
        self.get_plot().set_legend()

if __name__ == '__main__':
    pass
       