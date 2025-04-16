from plotters.plots.abstract_plot import AbstractPlot
from plotters.plots.colour_palettes import COLOUR_PALETTES, COLOUR_ORDER_LIST, COLOUR_BASE


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class Histogram(AbstractPlot):
    """Bar chart with data upto three levels: category, group, and component levels.
    """
    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================ 
    def draw(self, data, no_bins, title, x_label, y_label, label='', color=COLOUR_PALETTES[COLOUR_ORDER_LIST[0]][COLOUR_BASE], unitize=True):
        """ Draw the histogram.
        
            Parameters
            ----------
            data : list
                List of all data points.
            no_bins : int
                Number of bins in the histogram
            title : str
                Title of the barchart.
            x_label : str
                X-label of the barchart.
            y_label : str
                Y-label of the barchart.
        """

        self.get_plot().draw_histogram(data, no_bins, label=label, color=color, unitize=unitize, alpha=0.5)
        
        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()
        # self.get_plot().set_legend(title="legend")

    def draw_pdf(self, x_data, y_data, label, title=None, x_label=None, y_label=None):
        """ Overlay the probability distribution function on a histogram.
        
            Parameters
            ----------
            x_data : list
                List of x values.
            y_data : list
                f(x) for all the y values.
            label : str
                label for the function plotted
            title : str
                Title of the barchart.
            x_label : str
                X-label of the barchart.
            y_label : str
                Y-label of the barchart.
        """
        self.get_plot().draw_line(x_data, y_data, label)

        if title is not None:
            self.get_plot().set_title(title)
            self.get_plot().set_grid()
            self.get_plot().set_legend()
        if x_label is not None or y_label is not None:
            self.get_plot().set_labels(x_label, y_label)


if __name__ == '__main__':
    pass
       