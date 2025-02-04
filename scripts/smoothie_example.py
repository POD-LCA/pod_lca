from lca_modules.material.project_manager import Project
from lca_modules.material.calculator import Calculator
from lca_modules.impacts.impacts_database import ImpactsDatabase
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter
from plotters.plots.bar_chart import BarChart
from plotters.plots.radar_chart import RadarChart
from lca_modules.uncertainty.hotspots import HotSpotAnalysis
from lca_modules.uncertainty.datasets import DataSet
from lca_modules.uncertainty.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainty.sensitivity_analysis import compute_sensitivity

from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR
from utilities.units.metric_prefixes import KILO, MEGA

from numpy import random

# Smoothie example

project = Project.new("Smoothie Project")

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
custom_impact_database.set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                      {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})
print(custom_impact_database)

project.set_database(custom_impact_database)

model_0 = project.add_model("Model_0")
model_1 = project.add_model("Model_1")

sprinkles = model_0.add_product(name="Sprinkles", stage="A1", qty=2.0, unit=KILOGRAM, impacts_from="Sprinkles")
sand = model_1.add_product(name="Sand", stage="A1", qty=1.0, unit=KILOGRAM, impacts_from="Sand")
pickles = model_0.add_product(name="Pickles", stage="A1", qty=4.0, unit=KILOGRAM, impacts_from="Pickles")

mega_joule = MEGA * JOULE
propane = model_0.add_energy(name="Propane", stage="A1", qty=1.0, unit=mega_joule, impacts_from="Propane")
propane.set_density(0.02)
propane.set_weight_unit(KILOGRAM)

sprinkles_by_truck = model_0.add_transportation_process(name="Sprinkle Transportation", stage="A2", 
                                                        transported_distance=30, unit=KILOMETER,
                                                        impacts_from="Transportation by truck")
sprinkles_by_truck.set_transported_product(sprinkles)

sand_by_truck = model_1.add_transportation_process(name="Sand Transportation", stage="A2",
                                                    transported_distance=40, unit=KILOMETER,
                                                    impacts_from="Transportation by truck")
sand_by_truck.set_transported_product(sand)

pickles_by_truck = model_0.add_transportation_process(name="Pickles Transportation", stage="A2",
                                                      transported_distance=17.0, unit=KILOMETER,
                                                      impacts_from="Transportation by truck")
pickles_by_truck.set_transported_product(pickles)

propane_by_truck = model_0.add_transportation_process(name="Propane Transportation", stage="A2",
                                                      transported_distance=20.0, unit=KILOMETER,
                                                      impacts_from="Transportation by truck")
propane_by_truck.set_transported_product(propane)

electricity = model_0.add_energy(name="Electricity for Mixing", stage="A3", qty=3.0, unit=KILO * WATT_HOUR, impacts_from="Electricity_New")
propane_transported = model_0.add_energy(name="Propane for Mixing", stage="A3", qty=1.0, unit=mega_joule, impacts_from="Propane")

product_1 = model_0.add_product(name="Product of mixing", stage="A3", qty=3.0, unit=KILOGRAM, impacts_from=None)
product_2 = model_0.add_product(name="Product of mixing", stage="A3", qty=4.0, unit=KILOGRAM, impacts_from=None)

product1_by_truck = model_0.add_transportation_process(name="Product 01 Transportation", stage="A2",
                                                       transported_distance=3.0, unit=KILOMETER, 
                                                       impacts_from="Transportation by truck")
product1_by_truck.set_transported_product(product_1)

product2_by_truck = model_0.add_transportation_process(name="Product 02 Transportation", stage="A2",
                                                       transported_distance=14.0, unit=KILOMETER,
                                                       impacts_from="Transportation by truck")
product2_by_truck.set_transported_product(product_2)

electricity_2 = model_0.add_energy(name="Electricity for Chemical Reaction", stage="A3", qty=10.0, unit=KILO * WATT_HOUR, impacts_from="Electricity")


CO2 = model_0.add_emission(name="CO2", stage="A3", qty=0.5, unit=KILOGRAM, impacts_from="CO2")
CH4 = model_0.add_emission(name="CH4", stage="A3", qty=0.6, unit=KILOGRAM, impacts_from="CH4")
NH3 = model_0.add_emission(name="NH3", stage="A3", qty=0.7, unit=KILOGRAM, impacts_from="NH3")

waste = model_0.add_waste(name="Waste to landfill", stage="A3", qty=1.0, unit=KILOGRAM, impacts_from="Waste to landfill")

print(model_0)
print(project)

# hotspot_analysis = HotSpotAnalysis(project)
# hot_spots_GWP = hotspot_analysis.run(model_name='Model_0', impact_category= "GWP", printout=True)
# hot_spots_ODP = hotspot_analysis.run(model_name='Model_0', impact_category= "ODP", printout=True)
# hot_spots_wghtd = hotspot_analysis.run(model_name='Model_0', impact_category= "weighted", printout=True)

# data_quality_assessment = DataQualityAnalysis(project)
# data_quality_assessment.setPedigreeScores(model_name='Model_0')
# data_quality_assessment.update_pedigree_scores('Model_0', hot_spots_GWP[0], 'reliability', 2)
# data_quality_assessment.update_pedigree_scores('Model_0', hot_spots_GWP[1], {'completeness': 2,
#                                                                   'temporal correlation': 1, 
#                                                                   'geographical correlation': 3})
# DQS = data_quality_assessment.calculate_DQS('Model_0')


# result_range = compute_sensitivity(hot_spots_GWP[0], 
#                                    'qty', 
#                                    impact_cat='weighted', 
#                                    range=(8, 15))
# result_range = compute_sensitivity(product2_by_truck, 
#                                    'database_item', 
#                                    impact_cat='weighted', 
#                                    options=['Transportation by truck', 'Transportation by barge', 'Transportation by train'])

# data = random.normal(4, 1, 5)  
# dataset_pickles_qty = DataSet('pickles', data)
# pickles.set_dataset(dataset_pickles_qty, 'qty')
# best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, printout=True)
# distribution = dataset.set_distribution(best_fit)
# # TODO: Call Q-Q plots
# dataset.plot_fit()

# MCS = MonteCarloSimulation(project)
# MCS.run('Model_0')

graph = BarChart.from_plotter(MatplotlibPlotter)
# graph.draw(Calculator.get_impacts_by_LCstages("GWP", model_0), "GWP by Life Cycle Stages", "Life Cycle Stages", "GWP")
graph.draw(Calculator.get_impacts_by_LCstages_models("GWP", [model_0, model_1]), "GWP by Life Cycle Stages for all models", "Life Cycle Stages", "GWP")
# graph.draw(Calculator.get_impacts_by_LCstages_models_items("GWP", [model_0, model_1]), "GWP by Life Cycle Stages for all models", "Life Cycle Stages", "GWP")
# graph.draw(Calculator.get_impacts_by_impactcategorys_models_LCstage(["GWP","ODP"], [model_0, model_1]), "Impacts by stages", "Impact Category", "Impact Value")

# graph = RadarChart.from_plotter(MatplotlibPlotter)
# graph.draw(Calculator.get_impacts_by_category_models([model_0, model_1]), "Impacts by category")
# graph.draw(Calculator.get_normalized_impacts_by_category(model_1), "Impacts by category")

graph.show()