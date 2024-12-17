from lca_modules.material.projectManager import Project
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from lca_modules.uncertainity.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainity import sensitivity_analysis
from lca_modules.uncertainity.datasets import DataDistribution
from lca_modules.uncertainity.monte_carlo_simulation import MonteCarloSimulator
from utilities.units.common_units import KILOGRAM, JOULE, KILOMETER, WATT_HOUR, CUBIC_METER
from utilities.units.metric_prefixes import KILO, MEGA

from math import exp
from scipy import stats
from numpy import linspace, mean, std, sqrt, log
from matplotlib import pyplot
import time

# CLT example #TODO add reference

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data.csv')

CLT_model = project.get_current_model()

lumber = CLT_model.create_product("Lumber", "A1")
lumber.set_qty(562.75)
lumber.set_unit(KILOGRAM)
lumber.set_impact_database_entry("Lumber_[CORRIM_LCA]")

meth_diphenyl_d = CLT_model.create_product("Methylene diphenyl diisocyanate resin", "A1")
meth_diphenyl_d.set_qty(3.22)
meth_diphenyl_d.set_unit(KILOGRAM)
meth_diphenyl_d.set_impact_database_entry("Methylene diphenyl diisocyanate resin_[FHWA_MTU]")

prop_glycol = CLT_model.create_product("Propylene glycol", "A1")
prop_glycol.set_qty(2.77)
prop_glycol.set_unit(KILOGRAM)
prop_glycol.set_impact_database_entry("Propylene glycol_[ecoinvent]")

dummy_PUR_1 = CLT_model.create_product("PUR_1", "A1")
dummy_PUR_1.set_qty(0.05)
dummy_PUR_1.set_unit(KILOGRAM)

dummy_PUR_2 = CLT_model.create_product("PUR_2", "A1")
dummy_PUR_2.set_qty(0.01)
dummy_PUR_2.set_unit(KILOGRAM)

dummy_PUR_3 = CLT_model.create_product("PUR_3", "A1")
dummy_PUR_3.set_qty(0.01)
dummy_PUR_3.set_unit(KILOGRAM)

kilo_watt_hour = KILO * WATT_HOUR
electricity = CLT_model.create_energy("Electricity", "A3")
electricity.set_qty(128.75)
electricity.set_unit(kilo_watt_hour)
electricity.set_impact_database_entry("Electricity_NWPP(eGrid)_[USLCI]")

natural_gas = CLT_model.create_energy("Natural gas", "A3")
natural_gas.set_qty(2.63)
natural_gas.set_unit(CUBIC_METER)
natural_gas.set_impact_database_entry("Natural gas_insustrial_equipment_[USLCI]")

lumber_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
lumber_by_truck.set_transported_product(lumber)
lumber_by_truck.set_transported_distance(302)
lumber_by_truck.set_transported_distance_unit(KILOMETER)
lumber_by_truck.set_impact_database_entry("Transportation_combination_truck_short-haul_diesel_NW_[USLCI]")

PUR1_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
PUR1_by_truck.set_transported_product(dummy_PUR_1)
PUR1_by_truck.set_transported_distance(2160)
PUR1_by_truck.set_transported_distance_unit(KILOMETER)
PUR1_by_truck.set_impact_database_entry("Transportation_combination_truck_diesel_US_[USLCI]")

PUR2_by_truck = CLT_model.create_transportation_process("Lumber Transportation", "A2")
PUR2_by_truck.set_transported_product(dummy_PUR_2)
PUR2_by_truck.set_transported_distance(64800)
PUR2_by_truck.set_transported_distance_unit(KILOMETER)
PUR2_by_truck.set_impact_database_entry("Transportation_freight_train_diesel_US_[ecoinvent]")


# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP", printout=True)


# Data Quality Assessment
data_quality_assessment = DataQualityAnalysis(CLT_model)
data_quality_assessment.setPedigreeScores()
data_quality_assessment.update_pedigree_scores(electricity, {'reliability': 1,
                                                             'completeness': 1,
                                                             'temporal correlation': 4,
                                                             'geographical correlation': 1,
                                                             'technological representativeness': 3})
data_quality_assessment.update_pedigree_scores(lumber, {'reliability': 1,
                                                        'completeness': 2,
                                                        'temporal correlation': 2,
                                                        'geographical correlation': 2,
                                                        'technological representativeness': 4})
data_quality_assessment.update_pedigree_scores(lumber_by_truck, {'reliability': 1,
                                                                 'completeness': 3,
                                                                 'temporal correlation': 4,
                                                                 'geographical correlation': 3,
                                                                 'technological representativeness': 3})
DQS = data_quality_assessment.calculate_DQS('GWP')

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


mean_val, sdev_val = 562.750, 0.729
sigma = sqrt(log(1 + (sdev_val**2 / mean_val**2)))
mu = log(mean_val) - 0.5 * sigma**2

dist = stats.lognorm(s=sigma, loc=0, scale=exp(mu))
data_set = DataDistribution.from_distributions(dist)
lumber.set_data_distribution(data_set, 'qty')

# x = linspace(500, 600, 1)
# p = dist.pdf(x)
# pyplot.plot(x, p, 'k', linewidth=2, label='Fitted Normal')
# pyplot.xlabel('Value')
# pyplot.ylabel('Probability Density')
# pyplot.title('Distribution Plot')
# pyplot.grid(True)
# pyplot.show()

MCS = MonteCarloSimulator.from_model(CLT_model)
MCS.set_iterations(1000)
MCS.run()
MCS.plot_hist(bin_size=25)

MCS.set_scenario({lumber: 'low'})
MCS.run()
MCS.plot_hist(bin_size=25)
