__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from ...visualizer import AbstractPlot


class BoxPlot(AbstractPlot):
    """Line chart with multiple lines."""

    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================
    def draw(self, data, title, x_label, y_label):
        """Draw the bar chart.

        Parameters
        ----------
        data : array
            Data in a 1D or 2D array.
            If 1D, it will be plotted as a single boxplot.
            If 2D, each column will be plotted as a separate boxplot.
        title : str
            Title of the barchart.
        x_label : str
            X-label of the barchart.
        y_label : str
            Y-label of the barchart.
        """
        self.get_plot().clear_plot()

        self.get_plot().draw_boxplot(data)

        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()


if __name__ == "__main__":
    pass
