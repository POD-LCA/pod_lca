import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """
    Plotter provides a prototype to generate various data visualizations.

    Attributes
    ----------
    calculator : Calculator object
        Calculator from which the plotter obtains data to be visualized.
    active_models : list of str
        Name(s) of the models considered for data visualization.
    impact_category : list or str
        Name(s) of the impact categories considered for data visualization.
    lca_stage : list or str
        LCA stage(s) considered for data visualization.
    fig : matplotlib.figure.Figure
        Figure being plotted.
    ax : matplotlib.axes.Axes
        Axes of the figure being plotted.
    plot_colors : list of str
        Colors for the plots, customizable for all derived classes.
    """

    IMPACT_UNITS = {
        'GWP': 'kg CO₂-eq',
        'AP': 'kg SO₂-eq',
        'EP': 'kg PO₄-eq',
        'ODP': 'kg CFC-11-eq',
        'SFP': 'kg O₃-eq'
    }

    PALETTES = {
        "default": ['tab:red', 'tab:blue', 'tab:orange'],
        "cool": ['#377eb8', '#4daf4a', '#984ea3'],
        "warm": ['#e41a1c', '#ff7f00', '#f781bf'],
        "grayscale": ['#444444', '#888888', '#bbbbbb']
    }

    def __init__(self, project, palette="default"):
        self.calculator = project.get_calculator()
        plt.close('all')
        self.fig, self.ax = plt.subplots(layout='constrained')

        self.impact_category = None
        self.active_models = None
        self.lca_stage = None

        # Set plot colors using the selected palette
        self.plot_colors = self.PALETTES.get(palette, self.PALETTES["default"])

    def set_color_palette(self, palette):
        """Set color palette for the plot.

        Parameters
        ----------
        palette : str or list
            Predefined palette name or a custom list of colors.
        """
        if isinstance(palette, str):
            self.plot_colors = self.PALETTES.get(palette, self.PALETTES["default"])
        elif isinstance(palette, list) and all(isinstance(color, str) for color in palette):
            self.plot_colors = palette
        else:
            raise ValueError("Invalid palette. Provide a predefined name or a list of color strings.")

    def set_impact_category(self, impact_cat):
        """Set impact category.

        Parameters
        ----------
        impact_cat : str or list
            Name(s) of the impact categories.
        """

        self.impact_category = impact_cat


    def set_active_models(self, active_models):
        """Set models considered for plotting.

        Parameters
        ----------
        active_models : str or list
            Name(s) of models.        
        
        """
        self.active_models = active_models

    def set_lca_stage(self, lca_stage):
        """Set LCA stage for plotting.
        
        Parameters
        ----------
        lca_stage : str or list
            LCA stages.             
        
        """
        self.lca_stage = lca_stage

    @staticmethod
    def round_to_significant(values, sig_figs=3):
        """Round a list of numbers to the given number of significant figures."""
        return [
            0 if val == 0 else round(val, sig_figs - int(np.floor(np.log10(abs(val))))) if np.isfinite(val) else val
            for val in np.atleast_1d(values)
        ]

    @staticmethod
    def format_labels(values, decimal_places=3):
        """Format labels for bar charts."""
        labels = []
        for v in values:
            if v == 0.0:
                labels.append('')
            else:
                labels.append(f"{v:.{decimal_places}g}")

        return labels

    def set_data(self):
        """Generate the data to be visualized."""
        pass

    def set_labels(self):
        """Set plot title and axis labels."""
        pass

    def set_legend(self):
        """Set the legend of the plot."""
        self.ax.legend()

    def set_grid(self):
        """Set grid lines and adjust y-axis height."""
        max_val = max((rect.get_height() for rect in self.ax.patches), default=10)
        if max_val > 0.0:
            self.ax.set_ylim([0, max(10, np.power(10, np.ceil(np.log10(max_val))))])
        else:
            self.ax.set_ylim([0, 10])
        self.ax.grid(True)

    def draw(self):
        """Update and redraw the plot."""
        self.ax.clear()
        self.set_data()
        self.set_labels()
        self.set_grid()
        self.set_legend()

    def show(self):
        """Display the plot."""
        self.draw()
        plt.show()
