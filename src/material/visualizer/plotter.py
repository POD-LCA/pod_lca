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
        Names of the models considered for data visualization.
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
        """Set impact category."""
        self.impact_category = impact_cat

    def set_active_models(self, active_models):
        """Set models considered for plotting."""
        self.active_models = active_models

    def set_lca_stage(self, lca_stage):
        """Set LCA stage for plotting."""
        self.lca_stage = lca_stage

    @staticmethod
    def round_to_significant(values, sig_figs=3):
        """Round a list of numbers to the given number of significant figures."""
        return [
            0 if val == 0 else round(val, sig_figs - int(np.floor(np.log10(abs(val))))) if np.isfinite(val) else val
            for val in np.atleast_1d(values)
        ]

    @staticmethod
    def format_labels(values):
        """Format labels for bar charts."""
        return [f"{v:.3g}" for v in values]

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
        self.ax.set_ylim([0, max(10, np.power(10, np.ceil(np.log10(max_val))))])
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
