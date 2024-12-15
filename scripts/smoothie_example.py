from lca_modules.material.projectManager import Project
from lca_modules.material.visualizer.bar_chart import BarChart
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR
from utilities.units.metric_prefixes import KILO, MEGA

from numpy import random

# Smoothie example

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data_smoothie.csv')

kilo_watt_hour = KILO * WATT_HOUR
project.get_database().set_custom_entry("Electricity_New", kilo_watt_hour, 
                                        {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

model_0 = project.get_current_model()

sprinkles = model_0.create_product("Sprinkles", "A1")
sprinkles.set_qty(2.0)
sprinkles.set_unit(KILOGRAM)
sprinkles.set_impact_database_entry("Sprinkles")

sand = model_0.create_product("Sand", "A1")
sand.set_qty(1.0)
sand.set_unit(KILOGRAM)
sand.set_impact_database_entry("Sand")

pickles = model_0.create_product("Pickles", "A1")
pickles.set_qty(4.0)
pickles.set_unit(KILOGRAM)
pickles.set_impact_database_entry("Pickles")

mega_joule = MEGA * JOULE
propane = model_0.create_energy("Propane", "A1")
propane.set_qty(1.0)
propane.set_unit(mega_joule)
propane.set_density(0.02)
propane.set_weight_unit(KILOGRAM)
propane.set_impact_database_entry("Propane")

sprinkles_by_truck = model_0.create_transportation_process("Sprinkle Transportation", "A2")
sprinkles_by_truck.set_transported_product(sprinkles)
sprinkles_by_truck.set_transported_distance(30.0)
sprinkles_by_truck.set_transported_distance_unit(KILOMETER)
sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

sand_by_truck = model_0.create_transportation_process("Sand Transportation", "A2")
sand_by_truck.set_transported_product(sand)
sand_by_truck.set_transported_distance(40.0)
sand_by_truck.set_transported_distance_unit(KILOMETER)
sand_by_truck.set_impact_database_entry("Transportation by truck")

pickles_by_truck = model_0.create_transportation_process("Pickles Transportation", "A2")
pickles_by_truck.set_transported_product(pickles)
pickles_by_truck.set_transported_distance(17.0)
pickles_by_truck.set_transported_distance_unit(KILOMETER)
pickles_by_truck.set_impact_database_entry("Transportation by truck")

propane_by_truck = model_0.create_transportation_process("Propane Transportation", "A2")
propane_by_truck.set_transported_product(propane)
propane_by_truck.set_transported_distance(20.0)
propane_by_truck.set_transported_distance_unit(KILOMETER)
propane_by_truck.set_impact_database_entry("Transportation by truck")

electricity = model_0.create_energy("Electricity for Mixing", "A3")
electricity.set_qty(3.0)
electricity.set_unit(kilo_watt_hour)
electricity.set_impact_database_entry("Electricity_New")

propane_transported = model_0.create_energy("Propane for Mixing", "A3")
propane_transported.set_qty(1.0)
propane_transported.set_unit(mega_joule)
propane_transported.set_impact_database_entry("Propane")

product_1 = model_0.create_product("Product of mixing", "A3")
product_1.set_qty(3.0)
product_1.set_unit(KILOGRAM)

product_2 = model_0.create_product("Product of mixing", "A3")
product_2.set_qty(4.0)
product_2.set_unit(KILOGRAM)

product1_by_truck = model_0.create_transportation_process("Product 01 Transportation", "A2")
product1_by_truck.set_transported_product(product_1)
product1_by_truck.set_transported_distance(3.0)
product1_by_truck.set_transported_distance_unit(KILOMETER)
product1_by_truck.set_impact_database_entry("Transportation by truck")

product2_by_truck = model_0.create_transportation_process("Product 02 Transportation", "A2")
product2_by_truck.set_transported_product(product_2)
product2_by_truck.set_transported_distance(14.0)
product2_by_truck.set_transported_distance_unit(KILOMETER)
product2_by_truck.set_impact_database_entry("Transportation by truck")

electricity_2 = model_0.create_energy("Electricity for Chemical Reaction", "A3")
electricity_2.set_qty(10.0)
electricity_2.set_unit(kilo_watt_hour)
electricity_2.set_impact_database_entry("Electricity")

CO2 = model_0.create_emission("CO2", "A3")
CO2.set_qty(0.5)
CO2.set_unit(KILOGRAM)
CO2.set_impact_database_entry("CO2")

CH4 = model_0.create_emission("CH4", "A3")
CH4.set_qty(0.6)
CH4.set_unit(KILOGRAM)
CH4.set_impact_database_entry("CH4")

NH3 = model_0.create_emission("NH3", "A3")
NH3.set_qty(0.7)
NH3.set_unit(KILOGRAM)
NH3.set_impact_database_entry("NH3")

waste = model_0.create_waste("Waste to landfill", "A3")
waste.set_qty(1.0)
waste.set_unit(KILOGRAM)
waste.set_impact_database_entry("Waste to landfill")

hotspot_analysis = HotSpotAnalysis(model_0)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP", printout=True)
hot_spots_ODP = hotspot_analysis.run(impact_category= "ODP", printout=True)
hot_spots_wghtd = hotspot_analysis.run(impact_category= "weighted", printout=True)

graph = BarChart(project)
graph.set_impact_category("GWP")
graph.set_active_models(['Model_0'])
graph.show()
