
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from matplotlib.patches import Patch
import matplotlib.pyplot as plt

from ...visualizer import AbstractPlotter
from ...utilities import config


class MatplotlibPlotter(AbstractPlotter):
    """ A plotter implemented from Matplotlib package.

    Attributes
    ----------
    fig : matplotlib.figure.Figure
        Figure being plotted.
    ax : matplotlib.axes.Axes
        Axes of the figure being plotted.
    """

    def __init__(self):
        super().__init__()
        self.fig = None 
        self.ax = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def create_plot(cls, polar=False):
        """ Creates a new matplotlib plot.
        
        Parameters
        ----------
        Polar : bool
            If true, create a plot with polar axis.
        """
        plt.close('all')

        plot = cls()
        if polar:
            plot.fig, plot.ax = plt.subplots(layout='constrained', subplot_kw={'projection': 'polar'})
        else:
            plot.fig, plot.ax = plt.subplots(layout='constrained')
        
        return plot

    # ================================
    # Plot actions
    # ================================      
    def clear_plot(self):
        """ Clear the plot
        """
        self.ax.clear()

        return self

    def show(self):
        """Display the plot.
        """
        plt.show()

    # ================================
    # Draw methods
    # ================================ 
    def draw_bar(self, pos, height, width, bottom=0., color='blue', label=None, label_pos='center'):
        """ draw a bar in a bar chart.
        
        Parameters
        ----------
        pos : float
            Position (center) of the bar on the x-axis.
        height : float
            Height of the bar.
        width : float
            Width of the bar.
        bottom : float
            Position (bottom) of the bar on y-axis.
        label : str
            Labeling of the bar.
        label_pos : str
            Label position on the bar.
        """
        rect = self.ax.bar(pos, height, width, bottom, color=color, label=label)
        self.ax.bar_label(rect, label_type=label_pos)

        return self
    
    def draw_radar(self, angles, values, label, color, alpha=0.5):
        """ Draw radar lines in a polar plot.
        
        Parameters
        ----------
        angles : list
            List of angles for the radar lines.
        values : list
            List of values to be marked in each radar line.
        label : str
            Label for the radar created.
        color : str
            Color of the radar plot as a named or hex string.
        alpha : float
            Transparency of the radar (value between 0 and 1).
        """

        self.ax.plot(angles, values, color=color, label=label)
        self.ax.fill(angles, values, color=color, alpha=alpha)

    def draw_histogram(self, data, no_bins, label, color, alpha, unitize):
        """ Draw a histogram.
        
        Parameters
        ----------
        data : list
            List of all data points.
        no_bins : int
            Number of bins in the histogram
        label : str
            Identifier of the histogram.
        color : str
            Color of the radar plot as a named or hex string.
        alpha : float
            Transparency of the radar (value between 0 and 1).
        unitize : bool
            If true, the area under of the histogram is set to 1.
        """        
        self.ax.hist(data, bins=no_bins, density=unitize, alpha=alpha, label=label, color=color)

        return self
    
    def draw_line(self, x_data, y_data, label, color=None):
        """ Draw a line plot through (x, y) data pairs.
        
        Parameters
        ----------
        x_data : list
            List of x values.
        y_data : list
            f(x) for all the y values.
        label : str
            label for the function plotted
        color : str
            Color of the radar plot as a named or hex string.
        """
        if color is None:
            COLOUR_BASE = config['Preferences']['COLOUR_BASE']
            COLOUR_PALETTES = config['Preferences']['COLOUR_PALETTES']
            COLOUR_ORDER_LIST = config['Preferences']['COLOUR_ORDER_LIST']
            color = COLOUR_PALETTES[COLOUR_ORDER_LIST[0]][COLOUR_BASE]

        self.ax.plot(x_data, y_data, color=color, linewidth=2, label=label)

    def draw_stackplot(self, x_data, y_data, labels, colors=None):
        """ Draw a stackplot.

        Parameters
        ----------
        x_data : array-like
            X data; shape (N,)
        y_data : array-like
            Y data; shape(M, N)
        labels : list of str
            Labels for y data series.
        colors : list of str or tuples
            Colors of named, hex string, or RGB tuples.
        """
        self.ax.stackplot( x_data, *y_data, labels=labels, colors=colors)

    def draw_boxplot(self, data):
        """ Draw a boxplot.
    
        Parameters
        ----------
        data : list
            List of all data points.
        color : str
            Color of the radar plot as a named or hex string.
        label : str
            Identifier of the histogram.
        """
        self.ax.boxplot(data, patch_artist=True)

        return self
    
    def draw_violinplot(self, data):
        """ Draw a violinplot.
        
        Parameters
        ----------
        data : list
            List of all data points.
        color : str
            Color of the radar plot as a named or hex string.
        label : str
            Identifier of the histogram.
        """
        self.ax.violinplot(data, showmedians=True)

        return self

    # ================================
    # Set plot components
    # ================================
    def set_title(self, title):
        """ Set title of the plot.
        
        Parameters
        ----------
        title : str
            Title of the plot.
        """
        self.ax.set_title(title)

        return self

    def set_labels(self, x_label='', y_label=''):
        """Set plot title and axis labels.
        
        Parameters
        ----------
        x_label : str
            X-axis label.
        y_label : str
            Y-axis labe
        """
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

        return self

    def set_legend(self, colors=None, labels=None, title=None):
        """Set the legend of the plot. If colors and labels are given, override with patches.
        
        Parameters
        ----------
        colors : list
            List of colors, if patches are being used.
        labels : str
            List of labels, if patches are being used.
        title : str
            Title of the legend.
        """
        if (colors is None) and (labels is None):
            self.ax.legend(title=title)
        else:
            if len(colors) == len(labels):
                legend_patches = [Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
                self.ax.legend(handles=legend_patches, title=title)
            else:
                raise IndexError("Number of colors and labels should match")

    def set_xticks(self, ticks, labels=None):
        """Set and label ticks along the x-axis of the plot.
        
        Parameters
        ----------
        ticks : 1D array-like
            List of x values where ticks to be added.
        labels : list
            List of labels for the ticks.
        """
        if labels is None:
            labels = ticks
        self.ax.set_xticks(ticks, labels)

        return self

    def set_xlim(self, min, max):
        """Set limits of the x-axis of the plot.
        
        Parameters
        ----------
        min : float
            Minimum value on x-axis.
        max : float
            Maximum value on x-axis.
        """
        self.ax.set_xlim([min, max])

        return self
    
    def set_ylim(self, min, max):
        """Set limits of the y-axis of the plot.
        
        Parameters
        ----------
        min : float
            Minimum value on y-axis.
        max : float
            Maximum value on y-axis.
        """
        self.ax.set_ylim([min, max])

        return self
    
    def set_grid(self):
        """Set grid lines of the plot.
        """
        self.ax.grid(True)

        return self


if __name__ == '__main__':
    pass
       