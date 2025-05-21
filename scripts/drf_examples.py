

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "; mhtaba@uw.edu"
__version__ = "0.1.0"

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.visualizer import LinePlot
from pod_lca.visualizer import MatplotlibPlotter

print(DynamicRadiativeForcing.get_pertubation_lifetime("CO2"))
print(DynamicRadiativeForcing.get_radiative_efficiency("CO2", ref_unit='Wm-2kg-1'))

print(DynamicRadiativeForcing.get_instantaneous_concentration("CO2", 12))
print(DynamicRadiativeForcing.get_instantaneous_radiative_forcing("CO2", 12))
print(DynamicRadiativeForcing.get_cumulative_radiative_forcing("CO2", 12))

x_data, y_data = DynamicRadiativeForcing.get_radiative_forcing_time_series("CO2", 100, 1, cumulative=False)

graph = LinePlot.from_plotter(MatplotlibPlotter)
graph.draw([x_data, y_data], "Instantaneous Dynamic Radiative Forcing", "Year", "dynamic radiative forcing (Wm-2)")
graph.show()
