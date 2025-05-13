
from plotters.plots.bar_chart import BarChart
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

data = {"cat_A" : 3.5, "cat_B" : 2.0, "cat_C" : 1.5, "cat_D" : 7.0}

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Parameter by category", "Category", "Parameter (unit)")
graph.show()
