from lca_modules.material.projectManager.projectManager import Project
from lca_modules.material.visualizer.bar_chart import BarChart
from lca_modules.material.visualizer.bar_chart2 import BarChart2
from lca_modules.material.visualizer.bar_chart3 import BarChart3
from lca_modules.material.visualizer.Spider_chart import Spiderchart
from lca_modules.material.visualizer.Spider_chart_normilized import Spiderchart_n
from lca_modules.uncertainity.hotspots import HotSpotAnalysis

# Smoothie example

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

project.get_database().set_custom_entry("Electricity_New", "kWh", 
                                        {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})


sprinkles = project.current_model.create_product("Sprinkles", "A1")
sprinkles.update_qty(2.0)
sprinkles.set_unit('kg')
sprinkles.set_impact_database_entry("Sprinkles")

sand = project.current_model.create_product("Sand", "A1")
sand.update_qty(1.0)
sand.set_unit('kg')
sand.set_impact_database_entry("Sand")

pickles = project.current_model.create_product("Pickles", "A1")
pickles.update_qty(4.0)
pickles.set_unit('kg')
pickles.set_impact_database_entry("Pickles")

propane = project.current_model.create_energy("Propane", "A1")
propane.update_qty(1.0)
propane.set_unit('MJ')
propane.set_density(0.02)
propane.set_weight_unit('kg')
propane.set_impact_database_entry("Propane")

sprinkles_by_truck = project.current_model.create_transportation_process("Sprinkle Transportation", "A2")
sprinkles_by_truck.set_transported_product(sprinkles)
sprinkles_by_truck.set_transported_distance(30.0)
sprinkles_by_truck.set_transported_distance_unit('km')
sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

sand_by_truck = project.current_model.create_transportation_process("Sand Transportation", "A2")
sand_by_truck.set_transported_product(sand)
sand_by_truck.set_transported_distance(40.0)
sand_by_truck.set_transported_distance_unit('km')
sand_by_truck.set_impact_database_entry("Transportation by truck")

pickles_by_truck = project.current_model.create_transportation_process("Pickles Transportation", "A2")
pickles_by_truck.set_transported_product(pickles)
pickles_by_truck.set_transported_distance(17.0)
pickles_by_truck.set_transported_distance_unit('km')
pickles_by_truck.set_impact_database_entry("Transportation by truck")

propane_by_truck = project.current_model.create_transportation_process("Propane Transportation", "A2")
propane_by_truck.set_transported_product(propane)
propane_by_truck.set_transported_distance(20.0)
propane_by_truck.set_transported_distance_unit('km')
propane_by_truck.set_impact_database_entry("Transportation by truck")

electricity = project.current_model.create_energy("Electricity for Mixing", "A3")
electricity.update_qty(3.0)
electricity.set_unit('kWh')
electricity.set_impact_database_entry("Electricity_New")

propane_transported = project.current_model.create_energy("Propane for Mixing", "A3")
propane_transported.update_qty(1.0)
propane_transported.set_unit('MJ')
propane_transported.set_impact_database_entry("Propane")

product_1 = project.current_model.create_product("Product of mixing", "A3")
product_1.update_qty(3.0)
product_1.set_unit('kg')

product_2 = project.current_model.create_product("Product of mixing", "A3")
product_2.update_qty(4.0)
product_2.set_unit('kg')

product1_by_truck = project.current_model.create_transportation_process("Product 01 Transportation", "A2")
product1_by_truck.set_transported_product(product_1)
product1_by_truck.set_transported_distance(3.0)
product1_by_truck.set_transported_distance_unit('km')
product1_by_truck.set_impact_database_entry("Transportation by truck")

product2_by_truck = project.current_model.create_transportation_process("Product 02 Transportation", "A2")
product2_by_truck.set_transported_product(product_2)
product2_by_truck.set_transported_distance(14.0)
product2_by_truck.set_transported_distance_unit('km')
product2_by_truck.set_impact_database_entry("Transportation by truck")

electricity_2 = project.current_model.create_energy("Electricity for Chemical Reaction", "A3")
electricity_2.update_qty(10.0)
electricity_2.set_unit('kWh')
electricity_2.set_impact_database_entry("Electricity")

CO2 = project.current_model.create_emission("CO2", "A3")
CO2.update_qty(0.5)
CO2.set_unit('kg')
CO2.set_impact_database_entry("CO2")

CH4 = project.current_model.create_emission("CH4", "A3")
CH4.update_qty(0.6)
CH4.set_unit('kg')
CH4.set_impact_database_entry("CH4")

NH3 = project.current_model.create_emission("NH3", "A3")
NH3.update_qty(0.7)
NH3.set_unit('kg')
NH3.set_impact_database_entry("NH3")

waste = project.current_model.create_waste("Waste to landfill", "A3")
waste.update_qty(1.0)
waste.set_unit('kg')
waste.set_impact_database_entry("Waste to landfill")

#----------------------------------------------------

model2 = project.create_model('Model_02')
project.set_current_model('Model_02')

sprinkles = model2.create_product("Sprinkles", "A1")
sprinkles.update_qty(40.0)
sprinkles.set_unit('kg')
sprinkles.set_impact_database_entry("Sprinkles")

sand = model2.create_product("Sand", "A1")
sand.update_qty(10.0)
sand.set_unit('kg')
sand.set_impact_database_entry("Sand")

pickles = model2.create_product("Pickles", "A1")
pickles.update_qty(4.0)
pickles.set_unit('kg')
pickles.set_impact_database_entry("Pickles")

propane = model2.create_energy("Propane", "A1")
propane.update_qty(12.0)
propane.set_unit('MJ')
propane.set_density(0.02)
propane.set_weight_unit('kg')
propane.set_impact_database_entry("Propane")

sprinkles_by_truck = model2.create_transportation_process("Sprinkle Transportation", "A2")
sprinkles_by_truck.set_transported_product(sprinkles)
sprinkles_by_truck.set_transported_distance(30.0)
sprinkles_by_truck.set_transported_distance_unit('km')
sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

sand_by_truck = model2.create_transportation_process("Sand Transportation", "A2")
sand_by_truck.set_transported_product(sand)
sand_by_truck.set_transported_distance(100.0)
sand_by_truck.set_transported_distance_unit('km')
sand_by_truck.set_impact_database_entry("Transportation by truck")

pickles_by_truck = model2.create_transportation_process("Pickles Transportation", "A2")
pickles_by_truck.set_transported_product(pickles)
pickles_by_truck.set_transported_distance(17.0)
pickles_by_truck.set_transported_distance_unit('km')
pickles_by_truck.set_impact_database_entry("Transportation by truck")

propane_by_truck = model2.create_transportation_process("Propane Transportation", "A2")
propane_by_truck.set_transported_product(propane)
propane_by_truck.set_transported_distance(25.0)
propane_by_truck.set_transported_distance_unit('km')
propane_by_truck.set_impact_database_entry("Transportation by truck")

electricity = model2.create_energy("Electricity for Mixing", "A3")
electricity.update_qty(3.0)
electricity.set_unit('kWh')
electricity.set_impact_database_entry("Electricity_New")

propane_transported = model2.create_energy("Propane for Mixing", "A3")
propane_transported.update_qty(10.0)
propane_transported.set_unit('MJ')
propane_transported.set_impact_database_entry("Propane")

product_1 = model2.create_product("Product of mixing", "A3")
product_1.update_qty(3.0)
product_1.set_unit('kg')

product_2 = model2.create_product("Product of mixing", "A3")
product_2.update_qty(4.0)
product_2.set_unit('kg')

product1_by_truck = model2.create_transportation_process("Product 01 Transportation", "A2")
product1_by_truck.set_transported_product(product_1)
product1_by_truck.set_transported_distance(30.0)
product1_by_truck.set_transported_distance_unit('km')
product1_by_truck.set_impact_database_entry("Transportation by truck")

product2_by_truck = model2.create_transportation_process("Product 02 Transportation", "A2")
product2_by_truck.set_transported_product(product_2)
product2_by_truck.set_transported_distance(14.0)
product2_by_truck.set_transported_distance_unit('km')
product2_by_truck.set_impact_database_entry("Transportation by truck")

electricity_2 = model2.create_energy("Electricity for Chemical Reaction", "A3")
electricity_2.update_qty(10.0)
electricity_2.set_unit('kWh')
electricity_2.set_impact_database_entry("Electricity")

CO2 = model2.create_emission("CO2", "A3")
CO2.update_qty(0.5)
CO2.set_unit('kg')
CO2.set_impact_database_entry("CO2")

CH4 = model2.create_emission("CH4", "A3")
CH4.update_qty(0.6)
CH4.set_unit('kg')
CH4.set_impact_database_entry("CH4")

NH3 = model2.create_emission("NH3", "A3")
NH3.update_qty(0.1)
NH3.set_unit('kg')
NH3.set_impact_database_entry("NH3")

waste = model2.create_waste("Waste to landfill", "A3")
waste.update_qty(1.0)
waste.set_unit('kg')
waste.set_impact_database_entry("Waste to landfill")

#----------------------------------------------------
#model 03
model3 = project.create_model('Model_03')
project.set_current_model('Model_03')


sprinkles = model3.create_product("Sprinkles", "A1")
sprinkles.update_qty(24.0)
sprinkles.set_unit('kg')
sprinkles.set_impact_database_entry("Sprinkles")

sand = model3.create_product("Sand", "A1")
sand.update_qty(11.0)
sand.set_unit('kg')
sand.set_impact_database_entry("Sand")

pickles = model3.create_product("Pickles", "A1")
pickles.update_qty(4.0)
pickles.set_unit('kg')
pickles.set_impact_database_entry("Pickles")

propane = model3.create_energy("Propane", "A1")
propane.update_qty(16.0)
propane.set_unit('MJ')
propane.set_density(0.02)
propane.set_weight_unit('kg')
propane.set_impact_database_entry("Propane")

sprinkles_by_truck = model3.create_transportation_process("Sprinkle Transportation", "A2")
sprinkles_by_truck.set_transported_product(sprinkles)
sprinkles_by_truck.set_transported_distance(30.0)
sprinkles_by_truck.set_transported_distance_unit('km')
sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

sand_by_truck = model3.create_transportation_process("Sand Transportation", "A2")
sand_by_truck.set_transported_product(sand)
sand_by_truck.set_transported_distance(46.0)
sand_by_truck.set_transported_distance_unit('km')
sand_by_truck.set_impact_database_entry("Transportation by truck")

pickles_by_truck = model3.create_transportation_process("Pickles Transportation", "A2")
pickles_by_truck.set_transported_product(pickles)
pickles_by_truck.set_transported_distance(14.0)
pickles_by_truck.set_transported_distance_unit('km')
pickles_by_truck.set_impact_database_entry("Transportation by truck")

propane_by_truck = model3.create_transportation_process("Propane Transportation", "A2")
propane_by_truck.set_transported_product(propane)
propane_by_truck.set_transported_distance(27.0)
propane_by_truck.set_transported_distance_unit('km')
propane_by_truck.set_impact_database_entry("Transportation by truck")

electricity = model3.create_energy("Electricity for Mixing", "A3")
electricity.update_qty(35.0)
electricity.set_unit('kWh')
electricity.set_impact_database_entry("Electricity_New")

propane_transported = model3.create_energy("Propane for Mixing", "A3")
propane_transported.update_qty(10.0)
propane_transported.set_unit('MJ')
propane_transported.set_impact_database_entry("Propane")

product_1 = model3.create_product("Product of mixing", "A3")
product_1.update_qty(3.0)
product_1.set_unit('kg')

product_2 = model3.create_product("Product of mixing", "A3")
product_2.update_qty(4.0)
product_2.set_unit('kg')

product1_by_truck = model3.create_transportation_process("Product 01 Transportation", "A2")
product1_by_truck.set_transported_product(product_1)
product1_by_truck.set_transported_distance(35.0)
product1_by_truck.set_transported_distance_unit('km')
product1_by_truck.set_impact_database_entry("Transportation by truck")

product2_by_truck = model3.create_transportation_process("Product 02 Transportation", "A2")
product2_by_truck.set_transported_product(product_2)
product2_by_truck.set_transported_distance(12.0)
product2_by_truck.set_transported_distance_unit('km')
product2_by_truck.set_impact_database_entry("Transportation by truck")

electricity_2 = model3.create_energy("Electricity for Chemical Reaction", "A3")
electricity_2.update_qty(10.0)
electricity_2.set_unit('kWh')
electricity_2.set_impact_database_entry("Electricity")

CO2 = model3.create_emission("CO2", "A3")
CO2.update_qty(0.9)
CO2.set_unit('kg')
CO2.set_impact_database_entry("CO2")

CH4 = model3.create_emission("CH4", "A3")
CH4.update_qty(0.6)
CH4.set_unit('kg')
CH4.set_impact_database_entry("CH4")

NH3 = model3.create_emission("NH3", "A3")
NH3.update_qty(0.2)
NH3.set_unit('kg')
NH3.set_impact_database_entry("NH3")

waste = model3.create_waste("Waste to landfill", "A3")
waste.update_qty(3.0)
waste.set_unit('kg')
waste.set_impact_database_entry("Waste to landfill")


hotspot_analysis = HotSpotAnalysis(project)
hot_spots_GWP = hotspot_analysis.run(model_name='Model_0', impact_category= "GWP", printout=True)

graph = BarChart(project, palette="grayscale")
graph.set_impact_category(["GWP"])
graph.set_active_models(['Model_0', 'Model_02', 'Model_03'])
# graph.show()

graph2 = BarChart2(project)
graph2.set_impact_category(["GWP"])
graph2.set_active_models(['Model_0', 'Model_02', 'Model_03'])
graph2.show()

graph3 = BarChart3(project)
graph3.set_impact_category(["GWP","ODP"])
graph3.set_active_models(['Model_0', 'Model_02', 'Model_03' ])
# graph3.show()

graph4 = Spiderchart(project)
graph4.set_impact_category(["GWP"])
graph4.set_active_models(['Model_0', 'Model_02', 'Model_03' ])
# graph4.set_lca_stage('all')
# graph4.show()

graph5 = Spiderchart_n(project)
graph5.set_active_models(['Model_0', 'Model_02', 'Model_03' ])
graph5.set_lca_stage('all')
# graph5.show()
