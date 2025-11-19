__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.visualizer import LinePlot
from pod_lca.visualizer import MatplotlibPlotter

print("Pertubation lifetime of N2O (in years):", DynamicRadiativeForcing().get_pertubation_lifetime("N2O"))
print("Pertubation lifetime of CH4 (in years):", DynamicRadiativeForcing().get_pertubation_lifetime("CH4"))
print("=" * 15)
print(
    "Radiative efficiency of CO2 (in Wm-2ppb-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CO2", ref_unit="Wm-2ppb-1"),
)
print(
    "Radiative efficiency of CH4 (in Wm-2ppb-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CH4", ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=False),
)
print(
    "Radiative efficiency of N2O (in Wm-2ppb-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("N2O", ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=False),
)
print("=" * 15)
print(
    "Radiative efficiency of CO2 (in Wm-2kg-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CO2", ref_unit="Wm-2kg-1"),
)
print(
    "Radiative efficiency of CH4 (in Wm-2kg-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CH4", ref_unit="Wm-2kg-1", adjust_for_indirect_effects=False),
)
print(
    "Radiative efficiency of N2O (in Wm-2kg-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("N2O", ref_unit="Wm-2kg-1", adjust_for_indirect_effects=False),
)
print("=" * 15)
print(
    "Radiative efficiency of CH4, adjusted for indirect effects (in Wm-2kg-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CH4", ref_unit="Wm-2kg-1", adjust_for_indirect_effects=True),
)
print(
    "Radiative efficiency of N2O, adjusted for indirect effects (in Wm-2kg-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("N2O", ref_unit="Wm-2kg-1", adjust_for_indirect_effects=True),
)
print("=" * 15)
print(
    "Radiative efficiency of CH4, adjusted for indirect effects (in Wm-2ppb-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("CH4", ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True),
)
print(
    "Radiative efficiency of N2O, adjusted for indirect effects (in Wm-2ppb-1):",
    DynamicRadiativeForcing().get_radiative_efficiency("N2O", ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True),
)
# print("Atmospheric concentration of CO2, after 12 years of emitting 1 kg (in )", DynamicRadiativeForcing.get_atmospheric_concentration("CO2", at_year=12)) # TODO: in what units
# print("Instantaneous radiative forcing of CO2, after 12 years of emitting 1 kg (in W/m2):", DynamicRadiativeForcing.get_radiative_forcing("CO2", at_year=12, cumulative=False))
# print("Cumulative radiative forcing of CO2, after 12 years of emitting 1 kg (in W/m2):", DynamicRadiativeForcing.get_radiative_forcing("CO2", at_year=12, cumulative=True))

# print("Cumulative radiative forcing of CH4, after 12 years of emitting 1 kg (in W/m2):", DynamicRadiativeForcing.get_radiative_forcing("CH4", at_year=12, cumulative=True, CH4_oxidation=False))
# print("Cumulative radiative forcing of CH4 fossil, after 12 years of emitting 1 kg (in W/m2):", DynamicRadiativeForcing.get_radiative_forcing("CH4", at_year=25, cumulative=False, CH4_oxidation=True, alpha=1.0))
print("=" * 15)
print("GWP - 20yr - CO2: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CO2", 20)))
print("GWP - 20yr - CH4: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CH4", 20)))
print("GWP - 20yr - CH4 fossil: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CH4 fossil", 20)))
print("GWP - 20yr - N2O: {:.0f}".format(DynamicRadiativeForcing().get_GWP("N2O", 20)))
print("=" * 15)
print("GWP - 100yr - CO2: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CO2", 100)))
print("GWP - 100yr - CH4: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CH4", 100)))
print("GWP - 100yr - CH4 fossil: {:.0f}".format(DynamicRadiativeForcing().get_GWP("CH4 fossil", 100)))
print("GWP - 100yr - N2O: {:.0f}".format(DynamicRadiativeForcing().get_GWP("N2O", 100)))

x_data_CH4, _, y_data_CH4 = DynamicRadiativeForcing().get_radiative_forcing_time_series(
    "CH4", time_horizon=500, time_step=1.0, cumulative=True, CH4_oxidation=False
)
x_data_CH4fossil, _, y_data_CH4fossil = DynamicRadiativeForcing().get_radiative_forcing_time_series(
    "CH4", time_horizon=500, time_step=1.0, cumulative=True, CH4_oxidation=True, alpha=1.0
)

graph = LinePlot.from_plotter(MatplotlibPlotter)
graph.draw(
    {"CH4_fossil": list(zip(x_data_CH4fossil, y_data_CH4fossil)), "CH4": list(zip(x_data_CH4, y_data_CH4))},
    "Instantaneous Dynamic Radiative Forcing CO2",
    "Year",
    "dynamic radiative forcing (Wm-2)",
)
graph.show()
