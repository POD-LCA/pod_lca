import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class Plotter:
    """
    Plotter provides a prototype to generate various data visualizations.

    Attributes
    ----------
    calculator : Calculator Obj.
        Calculator from which the plotter obtains data to be visualised.
    active_models : list of str
        Names of the model considered for data visualuization.
    fig : Figure Obj. from Matplotlib
        Figure being plotted.
    ax : Axes Obj. from Matplotlib
        Set of axes of the figure being plotted.
    """

    # Shared dictionary to map impact categories to their units
    IMPACT_UNITS = {
        'GWP': 'kg CO₂-eq',    # Global Warming Potential
        'AP': 'kg SO₂-eq',     # Acidification Potential
        'EP': 'kg PO₄-eq',     # Eutrophication Potential
        'ODP': 'kg CFC-11-eq', # Ozone Depletion Potential
        'SFP': 'kg O₃-eq'      # Smog Formation Potential
    }

    def __init__(self, project):
        self.calculator = project.get_calculator()
        plt.close('all')
        self.fig, self.ax = plt.subplots(layout='constrained')

        self.impact_category = None
        self.active_models = None
        self.lca_stage = None

        self.bar_colors = ['tab:red', 'tab:blue', 'tab:orange']

    def set_impact_category(self, impact_cat):
        """ Set impact category.

            Parameters
            ----------
            impact_cat : str
                Impact catogery to be plotted
        """

        self.impact_category = impact_cat

    def set_active_models(self, active_models):
        """ Set models considered for plotting.

            Parameters
            ----------
            active_models : list of str
                Models considered for plotting.
        """

        self.active_models = active_models


    def set_lca_stage(self, lca_stage):
        """ Set lca stage for plotting.

            Parameters
            ----------
            lsa_stage : list of str
                lca stage to be plotted.
        """

        self.lca_stage = lca_stage
        
    def round_to_significant(self, values, sig_figs=3, apply_rounding=True):

        """ Optionally round a list of numbers to the given number of significant figures. """
        
        rounded_values = []
        
        for value in np.atleast_1d(values): 
            if np.isnan(value) or np.isinf(value):
                # If NaN or infinity, keep the original value
                rounded_values.append(value)
            elif value == 0:
                # Preserve zero without rounding
                rounded_values.append(0)
            elif apply_rounding:
                # Apply rounding to the specified number of significant figures
                rounded_value = round(float(value), sig_figs - int(np.floor(np.log10(abs(value)))))
                rounded_values.append(rounded_value)
            else:
                # Keep the original value without rounding
                rounded_values.append(value)

        return rounded_values

    def format_labels(self, values):
        """ Format labels for bar charts with 3 significant figures. """
        return [f"{v:.3g}" for v in values]
    

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot.
        """

        pass

    def set_labels(self):
        """ Set plot title and axis label.
        """

        pass

    def set_legend(self):
        """ Set legend of the plot.
        """

        pass

    def set_grid(self):
        """ Set grids of the plot.
            Default setting updates the y-axis height based on the maximum bar height.
        """

        max_val = max([rect.get_height() for rect in self.ax.patches])
        if max_val > 0.0:
            self.ax.set_ylim([0, max(np.power(10,np.ceil(np.log10(max_val))),10)])
        else:
            self.ax.set_ylim([0, 10])
        plt.grid(True)

    def draw(self):
        """ Updates an existing plot.
        """
        
        self.ax.clear()

        self.set_data()
        self.set_labels()
        self.set_grid()
        self.set_legend()
    
    def show(self):
        """ Draws a plot and display the figure.
        """

        self.ax.clear()

        self.set_data()
        self.set_labels()
        self.set_grid()
        self.set_legend()

        plt.grid(True)
        plt.show()

if __name__ == '__main__':
   pass
  