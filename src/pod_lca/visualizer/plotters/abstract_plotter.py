
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class AbstractPlotter:
    """  A plotter provides a means of drawing and displaying plots (graphs, charts. etc.).
    """

    def __init__(self):
        pass

    # ================================
    # Constructors
    # ================================
    @classmethod
    def create_plot(cls):
        """ Creates a new plot.
        """
        pass

    # ================================
    # Plot actions
    # ================================    
    def clear_plot(self):
        """ Clear the plot.
        """
        pass

    def show(self):
        """Display the plot.
        """
        pass

    # ================================
    # Draw methods
    # ================================ 
    def draw_bar(self, pos, height, width, bottom=0., label='', label_type='center'):
        """ draw a bar in a bar chart.
        """
        pass

    # ================================
    # Set plot components
    # ================================
    def set_title(self, title):
        """ Set title of the plot.
        """
        pass

    def set_labels(self, x_label, y_label):
        """Set axis labels of the plot.
        """
        pass

    def set_legend(self):
        """Set the legend of the plot.
        """
        pass

    def set_xlim(self, min, max):
        """Set limits of the x-axis of the plot.
        """
        pass

    def set_ylim(self, min, max):
        """Set limits of the y-axis of the plot.
        """
        pass
        
    def set_xticks(self, tick, labels):
        """Set and label ticks along the x-axis of the plot.
        """
        pass
    
    def set_yticks(self, tick, labels):
        """Set and label ticks along the y-axis of the plot.
        """
        pass
    
    def set_grid(self):
        """Set grid lines of the plot.
        """
        pass


if __name__ == '__main__':
    pass
       