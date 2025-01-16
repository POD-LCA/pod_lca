
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
        """ Create a bar chart from a plotter.
        
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

        chart.set_plot(plotter)

        return chart
    
    # ================================
    # Setters and Getters
    # ================================  
    def set_plot(self, plotter):
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