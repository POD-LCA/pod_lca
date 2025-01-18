from plotters.plots.bar_chart import BarChart
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

data = {"cat_A" : {"group_1": {'comp_A': 1}, "group_2": {'comp_B': 0.2, 'comp_C': 0.8}}, 
        "cat_B" : {"group_1": {'comp_D': 1, 'comp_E': 0.2, 'comp_F': 0.3}, "group_2": {'comp_G': 0.2, 'comp_H': 2.8}}}

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Parameter by category, grouped and identified by component.", "Group Name", "Parameter (unit)")
graph.show()