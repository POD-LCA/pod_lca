
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class AbstractPlot():
    """ An abstract class for specific implementation of graphs and charts. A plot is a set of instructions for plotting the graph.

    Attributes
    ----------
    plot : ~pod_lca.visualizer.AbstractPlot
        Plot.
    """

    def __init__(self):
        self.plot = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_plotter(cls, plotter):
        """ Create a plot from a plotter.
        
        Parameters
        ----------
        plotter : ~pod_lca.visualizer.AbstractPlotter
            Plotter.

        Returns
        -------
        ~pod_lca.visualizer.AbstractPlot
            Plot created.
        """
        chart = cls()

        chart.set_plot(plotter)

        return chart
    
    @classmethod
    def from_plot(cls, plot):
        """ Create a plot from an existing plot.
        
        Parameters
        ----------
        plot : ~pod_lca.visualizer.AbstractPlot
            Reference plot

        Returns
        -------
        ~pod_lca.visualizer.AbstractPlot
            Plot created.        
        """
        chart = cls()

        chart.plot = plot

        return chart
    
    # ================================
    # Setters and Getters
    # ================================  
    def set_plot(self, plotter):
        """ Set the plot.
        
        Parameters
        ----------
        plotter : ~pod_lca.visualizer.AbstractPlotter
            Plotter.        
        """
        self.plot = plotter.create_plot()

        return self
    
    def get_plot(self):
        """ Get the plot.
        
        Returns
        ----------
        ~pod_lca.visualizer.AbstractPlot
            Plotter.        
        """
        return self.plot

    # ================================
    # Methods
    # ================================ 
    def draw(self):
        """ Draw the plot.
        """
        pass

    def show(self):
        """ Display the barchart.
        """
        self.get_plot().show()


if __name__ == '__main__':
    pass
