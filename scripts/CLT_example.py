from lca_modules.material.projectManager import Project
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from lca_modules.uncertainity.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainity import sensitivity_analysis

# CLT example #TODO add reference

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data.csv')

CLT_model = project.get_current_model()

lumber = CLT_model.create_product("Lumber", "A1")
lumber.set_qty(562.75)
lumber.set_unit('kg')
lumber.set_impact_database_entry("Lumber_[CORRIM_LCA]")

meth_diphenyl_d = CLT_model.create_product("Methylene diphenyl diisocyanate resin", "A1")
meth_diphenyl_d.set_qty(3.22)
meth_diphenyl_d.set_unit('kg')
meth_diphenyl_d.set_impact_database_entry("Methylene diphenyl diisocyanate resin_[FHWA_MTU]")

prop_glycol = CLT_model.create_product("Propylene glycol", "A1")
prop_glycol.set_qty(2.77)
prop_glycol.set_unit('kg')
prop_glycol.set_impact_database_entry("Propylene glycol_[ecoinvent]")

dummy_PUR_1 = CLT_model.create_product("PUR_1", "A1")
dummy_PUR_1.set_qty(0.05)
dummy_PUR_1.set_unit('kg')

dummy_PUR_2 = CLT_model.create_product("PUR_2", "A1")
dummy_PUR_2.set_qty(0.01)
dummy_PUR_2.set_unit('kg')

dummy_PUR_3 = CLT_model.create_product("PUR_3", "A1")
dummy_PUR_3.set_qty(0.01)
dummy_PUR_3.set_unit('kg')

electricity = CLT_model.create_energy("Electricity", "A3")
electricity.set_qty(128.75)
electricity.set_unit('kWh')
electricity.set_impact_database_entry("Electricity_NWPP(eGrid)_[USLCI]")

natural_gas = CLT_model.create_energy("Natural gas", "A3")
natural_gas.set_qty(2.63)
natural_gas.set_unit('m3')
natural_gas.set_impact_database_entry("Natural gas_insustrial_equipment_[USLCI]")

lumber_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
lumber_by_truck.set_transported_product(lumber)
lumber_by_truck.set_transported_distance(302)
lumber_by_truck.set_transported_distance_unit('km')
lumber_by_truck.set_impact_database_entry("Transportation_combination_truck_short-haul_diesel_NW_[USLCI]")

PUR1_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
PUR1_by_truck.set_transported_product(dummy_PUR_1)
PUR1_by_truck.set_transported_distance(2160)
PUR1_by_truck.set_transported_distance_unit('km')
PUR1_by_truck.set_impact_database_entry("Transportation_combination_truck_diesel_US_[USLCI]")

PUR2_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
PUR2_by_truck.set_transported_product(dummy_PUR_2)
PUR2_by_truck.set_transported_distance(64800)
PUR2_by_truck.set_transported_distance_unit('km')
PUR2_by_truck.set_impact_database_entry("Transportation_freight_train_diesel_US_[ecoinvent]")


# Hotspot analysis
hotspot_analysis = HotSpotAnalysis(project)
hot_spots_GWP = hotspot_analysis.run(model_name='Model_0', impact_category= "GWP", printout=True)
#TODO: convert these to model as opposed to model_name

# Data Quality Assessment
data_quality_assessment = DataQualityAnalysis(project)
data_quality_assessment.setPedigreeScores(model_name='Model_0')
data_quality_assessment.update_pedigree_scores('Model_0', electricity, {'reliability': 1,
                                                                        'completeness': 1,
                                                                        'temporal correlation': 4, 
                                                                        'geographical correlation': 1,
                                                                        'technological representativeness': 3})
data_quality_assessment.update_pedigree_scores('Model_0', lumber, {'reliability': 1,
                                                                    'completeness': 2,
                                                                    'temporal correlation': 2, 
                                                                    'geographical correlation': 2,
                                                                    'technological representativeness': 4})
data_quality_assessment.update_pedigree_scores('Model_0', lumber_by_truck, {'reliability': 1,
                                                                            'completeness': 3,
                                                                            'temporal correlation': 4, 
                                                                            'geographical correlation': 3,
                                                                            'technological representativeness': 3})
DQS = data_quality_assessment.calculate_DQS('Model_0', 'GWP')

# Sensitivity Analysis
result_range = sensitivity_analysis.compute_sensitivity_of_param(electricity, 'impact_database_entry',
                                                                 impact_cat='GWP', 
                                                                 options=['Electricity_NWPP(eGrid)_[USLCI]', 'Electricity_UnknownHigh_[USLCI]', 'Electricity_UnknownLow_[USLCI]'])
result_range = sensitivity_analysis.compute_sensitivity_of_param(lumber,  'qty', 
                                                                 impact_cat='GWP', 
                                                                 range=(422.063, 844.125))

result_range = sensitivity_analysis.compute_sensitivity_of_params(CLT_model, 
                                                                  [{'obj': lumber_by_truck,  'param': 'transported_distance', 'range': (226.57, 453.13)},
                                                                   {'obj': PUR1_by_truck,  'param': 'transported_distance', 'range': (1620, 3240)},
                                                                   {'obj': PUR2_by_truck,  'param': 'transported_distance', 'range': (48600, 97200)}],
                                                                   impact_cat='GWP')


# data = random.normal(4, 1, 5)  
# dataset_pickles_qty = DataSet('pickles', data)
# pickles.set_dataset(dataset_pickles_qty, 'qty')
# # best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, printout=True)
# # distribution = dataset.set_distribution(best_fit)
# # # TODO: Call Q-Q plots
# # dataset.plot_fit()

# MCS = MonteCarloSimulation(project)
# MCS.run('Model_0')