
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

data = {
    "Fruits": {
        "Nutrients": {'Carbs': 12000,  # mg
                      'Protein': 800},  # mg
        "Minerals": {'Potassium': 250,  # mg
                     'Magnesium': 15,  # mg
                     'Calcium': 10}  # mg
    },
    "Vegetables": {
        "Nutrients": {'Carbs': 7500,  # mg
                      'Protein': 2100,  # mg
                      'Fiber': 3400},  # mg
        "Minerals": {'Potassium': 300,  # mg
                     'Iron': 2.7}  # mg
    }
}

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Nutrient and Mineral Content of Fruits vs. Vegetables (mg per 100g).", "", "quantity (in miligrams)")
graph.show()
