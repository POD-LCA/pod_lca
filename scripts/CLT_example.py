from lca_modules.material.project_manager import Project
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from lca_modules.uncertainity.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainity.sensitivity_analysis import SensitivityAnalysis
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

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impact_data.csv')
custom_impact_database.set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                      {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})
project.set_database(custom_impact_database)

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=562.75, unit=KILOGRAM, impacts_from="Lumber_[CORRIM_LCA]")
meth_diphenyl_d = CLT_model.add_product(name="Methylene diphenyl diisocyanate resin", stage="A1", qty=3.22, unit=KILOGRAM, impacts_from="Methylene diphenyl diisocyanate resin_[FHWA_MTU]")
prop_glycol = CLT_model.add_product(name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, impacts_from="Propylene glycol_[ecoinvent]")
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
electricity = CLT_model.add_product(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR, impacts_from="Electricity_NWPP(eGrid)_[USLCI]")
natural_gas = CLT_model.add_product(name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, impacts_from="Natural gas_insustrial_equipment_[USLCI]")

lumber_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=302, unit=KILOMETER, impacts_from="Transportation_combination_truck_short-haul_diesel_NW_[USLCI]")
lumber_by_truck.set_transported_product(lumber)

PUR1_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=2160, unit=KILOMETER, impacts_from="Transportation_combination_truck_diesel_US_[USLCI]")
PUR1_by_truck.set_transported_product(dummy_PUR_1)

PUR2_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=64800, unit=KILOMETER, impacts_from="Transportation_freight_train_diesel_US_[ecoinvent]")
PUR2_by_truck.set_transported_product(dummy_PUR_2)

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
hotspot_analysis.print_results()

# Data Quality Assessment
data_quality_assessment = DataQualityAnalysis.from_model(CLT_model)
print(electricity.get_pedigree_score())
electricity.get_pedigree_score().update_pedigree_scores({'reliability': 1,'completeness': 1,'temporal correlation': 4,'geographical correlation': 1,'technological representativeness': 3})
lumber.get_pedigree_score().update_pedigree_scores({'reliability': 1,'completeness': 2, 'temporal correlation': 2, 'geographical correlation': 2, 'technological representativeness': 4})
lumber_by_truck.get_pedigree_score().update_pedigree_scores({'reliability': 1, 'completeness': 3, 'temporal correlation': 4, 'geographical correlation': 3, 'technological representativeness': 3})
DQS, nDQS = data_quality_assessment.calculate_model_DQS('GWP')
data_quality_assessment.print_results()

# # Sensitivity Analysis
result_range = SensitivityAnalysis.compute_sensitivity_of_param(electricity, 'impact_database_entry',
                                                                 impact_cat='GWP', 
                                                                 options=['Electricity_NWPP(eGrid)_[USLCI]', 'Electricity_UnknownHigh_[USLCI]', 'Electricity_UnknownLow_[USLCI]'])
result_range = SensitivityAnalysis.compute_sensitivity_of_param(lumber,  'qty', 
                                                                 impact_cat='GWP', 
                                                                 range=(506.48, 619.03))
result_range = SensitivityAnalysis.compute_sensitivity_of_params(CLT_model, 
                                                                  [{'obj': lumber_by_truck,  'param': 'transported_distance', 'range': (226.57, 453.13)},
                                                                   {'obj': PUR1_by_truck,  'param': 'transported_distance', 'range': (1620, 3240)},
                                                                   {'obj': PUR2_by_truck,  'param': 'transported_distance', 'range': (48600, 97200)}],
                                                                   impact_cat='GWP')


mean_val, sdev_val = 562.750, 0.729
sigma = sqrt(log(1 + (sdev_val**2 / mean_val**2)))
mu = log(mean_val) - 0.5 * sigma**2

dist = stats.lognorm(s=sigma, loc=0, scale=exp(mu))
data_set = DataDistribution.from_distributions(dist, is_cts=True)
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
start = time.time()
MCS.run()
elapsed = time.time() - start
print("elapsed time", elapsed)
MCS.print_results()
MCS.plot_hist(bin_size=25)

MCS.set_scenario({lumber: 'low'})
MCS.run()
MCS.plot_hist(bin_size=25)
