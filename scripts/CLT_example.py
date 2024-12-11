from lca_modules.material.projectManager import Project
from lca_modules.material.visualizer.bar_chart import BarChart
from lca_modules.material.visualizer.bar_chart2 import BarChart2
from lca_modules.material.visualizer.bar_chart3 import BarChart3
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from lca_modules.uncertainity.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainity.sensitivity_analysis import compute_sensitivity

# Smoothie example

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data.csv')

model_0 = project.get_current_model()

lumber = model_0.create_product("Lumber", "A1")
lumber.update_qty(562.75)
lumber.set_unit('kg')
lumber.set_impact_database_entry("Lumber_[CORRIM_LCA]")

meth_diphenyl_d = model_0.create_product("Methylene diphenyl diisocyanate resin", "A1")
meth_diphenyl_d.update_qty(3.22)
meth_diphenyl_d.set_unit('kg')
meth_diphenyl_d.set_impact_database_entry("Methylene diphenyl diisocyanate resin_[FHWA_MTU]")

prop_glycol = model_0.create_product("Propylene glycol", "A1")
prop_glycol.update_qty(2.77)
prop_glycol.set_unit('kg')
prop_glycol.set_impact_database_entry("Propylene glycol_[ecoinvent]")

dummy_PUR_1 = model_0.create_product("PUR_1", "A1")
dummy_PUR_1.update_qty(0.05)
dummy_PUR_1.set_unit('kg')

dummy_PUR_2 = model_0.create_product("PUR_2", "A1")
dummy_PUR_2.update_qty(0.01)
dummy_PUR_2.set_unit('kg')

dummy_PUR_3 = model_0.create_product("PUR_3", "A1")
dummy_PUR_3.update_qty(0.01)
dummy_PUR_3.set_unit('kg')

electricity = model_0.create_energy("Electricity", "A3")
electricity.update_qty(128.75)
electricity.set_unit('kWh')
electricity.set_impact_database_entry("Electricity_NWPP(eGrid)_[USLCI]")

natural_gas = model_0.create_energy("Natural gas", "A3")
natural_gas.update_qty(2.63)
natural_gas.set_unit('m3')
natural_gas.set_impact_database_entry("Natural gas_insustrial_equipment_[USLCI]")

lumber_by_truck = model_0.create_transportation_process("Lumber Transportation", "A2")
lumber_by_truck.set_transported_product(lumber)
lumber_by_truck.set_transported_distance(302)
lumber_by_truck.set_transported_distance_unit('km')
lumber_by_truck.set_impact_database_entry("Transportation_combination_truck_short-haul_diesel_NW_[USLCI]")

PUR1_by_truck = model_0.create_transportation_process("Lumber Transportation", "A2")
PUR1_by_truck.set_transported_product(dummy_PUR_1)
PUR1_by_truck.set_transported_distance(2160)
PUR1_by_truck.set_transported_distance_unit('km')
PUR1_by_truck.set_impact_database_entry("Transportation_combination_truck_diesel_US_[USLCI]")

PUR2_by_truck = model_0.create_transportation_process("Lumber Transportation", "A2")
PUR2_by_truck.set_transported_product(dummy_PUR_2)
PUR2_by_truck.set_transported_distance(64800)
PUR2_by_truck.set_transported_distance_unit('km')
PUR2_by_truck.set_impact_database_entry("Transportation_freight_train_diesel_US_[ecoinvent]")

hotspot_analysis = HotSpotAnalysis(project)
hot_spots_GWP = hotspot_analysis.run(model_name='Model_0', impact_category= "GWP", printout=True)

data_quality_assessment = DataQualityAnalysis(project)
data_quality_assessment.setPedigreeScores(model_name='Model_0')
data_quality_assessment.update_pedigree_scores('Model_0', electricity, {'reliability': 1,
                                                                        'completeness': 1,
                                                                        'temporal correlation': 4, 
                                                                        'geographical correlation': 1,
                                                                        'technology correlation': 3})
data_quality_assessment.update_pedigree_scores('Model_0', lumber, {'reliability': 1,
                                                                    'completeness': 2,
                                                                    'temporal correlation': 2, 
                                                                    'geographical correlation': 2,
                                                                    'technology correlation': 4})
data_quality_assessment.update_pedigree_scores('Model_0', lumber_by_truck, {'reliability': 1,
                                                                            'completeness': 3,
                                                                            'temporal correlation': 4, 
                                                                            'geographical correlation': 3,
                                                                            'technology correlation': 3})
DQS = data_quality_assessment.calculate_DQS('Model_0')
