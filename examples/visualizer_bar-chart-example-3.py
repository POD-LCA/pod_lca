__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

data = {
    "Fruits": {
        "Nutrients": {"Carbs": 12000, "Protein": 800},  # mg  # mg
        "Minerals": {"Potassium": 250, "Magnesium": 15, "Calcium": 10},  # mg  # mg  # mg
    },
    "Vegetables": {
        "Nutrients": {"Carbs": 7500, "Protein": 2100, "Fiber": 3400},  # mg  # mg  # mg
        "Minerals": {"Potassium": 300, "Iron": 2.7},  # mg  # mg
    },
}

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Nutrient and Mineral Content of Fruits vs. Vegetables (mg per 100g).", "", "quantity (in miligrams)")
graph.show()
