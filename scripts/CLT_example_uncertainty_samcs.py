from lca_modules.material.project_manager import Project
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.uncertainty.datasets import DataDistribution
from lca_modules.uncertainty.monte_carlo_simulation import MonteCarloSimulator
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter
from plotters.plots.histogram import Histogram
from utilities.units.common_units import KILOGRAM, KILOMETER, WATT_HOUR, CUBIC_METER
from utilities.units.metric_prefixes import KILO

from math import exp
from scipy import stats
from numpy import linspace, sqrt, log
import time


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# CLT model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

project = Project()

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impact_data.csv')
custom_impact_database.set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                      {"GWP":0.233, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})
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

print(CLT_model)

mean_val, sdev_val = 562.750, 0.729
sigma = sqrt(log(1 + (sdev_val**2 / mean_val**2)))
mu = log(mean_val) - 0.5 * sigma**2

dist = stats.lognorm(s=sigma, loc=0, scale=exp(mu))
data_set = DataDistribution.from_distributions(dist, is_cts=True)
lumber.set_data_distribution(data_set, 'qty')

MCS = MonteCarloSimulator.from_model(CLT_model)
MCS.set_iterations(1000)
start = time.time()
MCS.run()
elapsed = time.time() - start
print("elapsed time", elapsed)
print(MCS)

graph = Histogram.from_plotter(MatplotlibPlotter)
graph.draw(MCS.result.get_data(), no_bins=25, title="Distribution from Monte Carlo Simulation.", x_label='qty', y_label="probability density")

MCS.result.set_distribution()
results_data = MCS.result.get_data()
x = linspace(min(results_data), max(results_data), 100)
p = MCS.result.get_distribution().pdf(x)

graph.draw_pdf(x, p, label="fitted distribution")
graph.show()

# MCS.set_scenario({lumber: 'low'})
# MCS.run()
# MCS.plot_hist(bin_size=25)
