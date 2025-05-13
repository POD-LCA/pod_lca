
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.visualizer import MatplotlibPlotter
from pod_lca.visualizer import RadarChart

data = {
    "Cristiano Ronaldo": {'Speed': 90, 'Strength': 85, 'Endurance': 85, 'Agility': 85, 'Skill': 92},
    "Lionel Messi": {'Speed': 85, 'Strength': 70, 'Endurance': 80, 'Agility': 95, 'Skill': 96},
    "Kylian Mbappé": {'Speed': 95, 'Strength': 80, 'Endurance': 88, 'Agility': 94, 'Skill': 85},
    "Neymar Jr": {'Speed': 87, 'Strength': 72, 'Endurance': 85, 'Agility': 91, 'Skill': 93}
}

graph = RadarChart.from_plotter(MatplotlibPlotter)
graph.draw(data, "Comparison of Key Attributes of Top Footballers")
graph.show()
