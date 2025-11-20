__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

data = {
    "Q1": {"2022": 1.0, "2023": 0.9},
    "Q2": {"2022": 1.3, "2023": 3.9},
    "Q3": {"2022": 0.6, "2023": 1.4},
    "Q4": {"2022": -0.25, "2023": 7.3},
}

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Profit in 2007 and 2008, by quarter", "Year", "Profit (in mil dollars)")
graph.show()
