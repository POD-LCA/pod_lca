
from plotters.plotters.abstract_plotter import AbstractPlotter

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class AbstractPlot():
    """An abstract class for specific implementation of graphs and charts.
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
            plotter : AbstractPlotter Obj.
                Plotter.

            Returns
            -------
            BarChart Obj.
                Plot created.
        """

        chart = cls()

        chart.set_plot_from_plotter(plotter)

        return chart
    
    @classmethod
    def from_plot(cls, plot):
        """ Create a plot from an existing plot.
        
            Parameters
            ----------
            plot : Object
                Plot created by an AbstractPlotter Obj.

            Returns
            -------
            BarChart Obj.
                Plot created.        
        
        """

        chart = cls()

        chart.set_plot(plot)

        return chart
    
    # ================================
    # Setters and Getters
    # ================================  
    def set_plot(self, plot):
        """ Set the plot.
        
            Parameters
            ----------
            plot : Object
                Plot created by an AbstractPlotter Obj.        
        """

        self.plot = plot

        return self

    def set_plot_from_plotter(self, plotter):
        """ Set the plot.
        
            Parameters
            ----------
            plotter : AbstractPlotter Obj.
                Plotter.        
        """

        self.plot = plotter.create_plot()

        return self
    
    def get_plot(self):
        """ Get the plot.
        
            Returns
            ----------
            AbstractPlotter Obj.
                Plotter.        
        """
        return self.plot

    # ================================
    # Methods
    # ================================ 
    def draw(self):
        """ Draw the plot."""
        pass

    def show(self):
        """ Display the barchart."""
        
        self.get_plot().show()
        
#TODO allow setting further properties with **kwargs

if __name__ == '__main__':
    pass