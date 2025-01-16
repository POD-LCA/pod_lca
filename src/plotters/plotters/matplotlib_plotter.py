from plotters.plotters.abstract_plotter import AbstractPlotter

import matplotlib.pyplot as plt
import numpy as np

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
        self.fig = None 
        self.ax = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def create_plot(cls, polar=False):
        """ Creates a new matplotlib plot"""

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
    def draw_bar(self, pos, height, width, bottom=0., label='', label_pos='center'):
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

        rect = self.ax.bar(pos, height, width, bottom, label=label)
        self.ax.bar_label(rect, label_type=label_pos)

        return self
    
    def draw_radar(self, angles, values, label, alpha=0.25):

        self.ax.plot(angles, values, label=label)
        self.ax.fill(angles, values, alpha=alpha)

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

    def set_legend(self):
        """Set the legend of the plot."""
        self.ax.legend()

    def set_xticks(self, tick, labels):
        """Set and label ticks along the x-axis of the plot.
        
            Parameters
            ----------
            list : 
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






    # def set_color_palette(self, palette):
    #     """Set color palette for the plot.

    #     Parameters
    #     ----------
    #     palette : str or list
    #         Predefined palette name or a custom list of colors.
    #     """
    #     if isinstance(palette, str):
    #         self.plot_colors = self.PALETTES.get(palette, self.PALETTES["default"])
    #     elif isinstance(palette, list) and all(isinstance(color, str) for color in palette):
    #         self.plot_colors = palette
    #     else:
    #         raise ValueError("Invalid palette. Provide a predefined name or a list of color strings.")

    # @staticmethod
    # def format_labels(values, decimal_places=3):
    #     """Format labels for bar charts."""
    #     labels = []
    #     for v in values:
    #         if v == 0.0:
    #             labels.append('')
    #         else:
    #             labels.append(f"{v:.{decimal_places}g}")

    #     return labels

#TODO setting colors