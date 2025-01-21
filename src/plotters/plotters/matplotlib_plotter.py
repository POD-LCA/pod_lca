from plotters.plotters.abstract_plotter import AbstractPlotter

from matplotlib.patches import Patch
import matplotlib.pyplot as plt

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class MatplotlibPlotter(AbstractPlotter):
    """
    A plotter implemented from Matplotlib package.

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
        """ Clear the plot"""

        self.ax.clear()

        return self

    def show(self):
        """Display the plot."""
        
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

    def draw_histogram(self, data, no_bins, color, alpha):
        """ Draw a histogram.
        
            Parameters
            ----------
            data : list
                List of all data points.
            no_bins : int
                Number of bins in the histogram
            color : str
                Color of the radar plot as a named or hex string.
            alpha : float
                Transparency of the radar (value between 0 and 1).
        """        

        self.ax.hist(data, bins=no_bins, density=True, alpha=alpha, label='Histogram', color=color)

        return self
    
    def draw_line(self, x_data, y_data, label):
        """ Draw a line plot through (x, y) data pairs.
        
            Parameters
            ----------
            x_data : list
                List of x values.
            y_data : list
                f(x) for all the y values.
            label : str
                label for the function plotted
        """

        self.ax.plot(x_data, y_data, 'k', linewidth=2, label=label)

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

    def set_xticks(self, tick, labels):
        """Set and label ticks along the x-axis of the plot.
        
            Parameters
            ----------
            tick : 1D array-like
                List of x values where ticks to be added.
            labels : list
                List of labels for the ticks.
        """
        self.ax.set_xticks(tick, labels)

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
        """Set grid lines of the plot."""
        self.ax.grid(True)

        return self


if __name__ == '__main__':
    pass
       