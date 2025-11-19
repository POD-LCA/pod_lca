# CLT model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import exp
from numpy import linspace
from numpy import log
from numpy import sqrt
from scipy import stats
import time

from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.uncertainty import DataDistribution
from pod_lca.uncertainty import MonteCarloSimulator
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import WATT_HOUR
from pod_lca.visualizer import Histogram
from pod_lca.visualizer import MatplotlibPlotter

project = Project()

factory = Location.from_str("98126, seattle")
project.set_location(factory)

project.set_impact_database(r"data/impacts_podlca_material-data.csv")
project.set_transportation_mode_impact_database(r"data/transportation_podlca_emission.csv")

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=562.75, unit=KILOGRAM, impacts_from="Lumber_[CORRIM_LCA]")
meth_diphenyl_d = CLT_model.add_product(
    name="Methylene diphenyl diisocyanate resin",
    stage="A1",
    qty=3.22,
    unit=KILOGRAM,
    impacts_from="Methylene diphenyl diisocyanate resin_[FHWA_MTU]",
)
prop_glycol = CLT_model.add_product(
    name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, impacts_from="Propylene glycol_[ecoinvent]"
)
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
electricity = CLT_model.add_electricity(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR)
natural_gas = CLT_model.add_energy(
    name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, impacts_from="Natural gas_insustrial_equipment_[USLCI]"
)

print(CLT_model)

mean_val, sdev_val = 562.750, 0.729
sigma = sqrt(log(1 + (sdev_val**2 / mean_val**2)))
mu = log(mean_val) - 0.5 * sigma**2

dist = stats.lognorm(s=sigma, loc=0, scale=exp(mu))
data_set = DataDistribution.from_distributions(dist, is_cts=True)
lumber.set_data_distribution(data_set, "qty")

MCS = MonteCarloSimulator.from_model(CLT_model)
MCS.set_iterations(1000)
start = time.time()
MCS.run()
elapsed = time.time() - start
print("elapsed time", elapsed)
print(MCS)

graph = Histogram.from_plotter(MatplotlibPlotter)
graph.draw(
    MCS.result.get_data(),
    no_bins=25,
    title="Distribution from Monte Carlo Simulation.",
    x_label="qty",
    y_label="probability density",
)

MCS.result.set_distribution()
results_data = MCS.result.get_data()
x = linspace(min(results_data), max(results_data), 100)
p = MCS.result.get_distribution().pdf(x)

graph.draw_pdf(x, p, label="fitted distribution")
graph.show()

# MCS.set_scenario({lumber: 'low'})
# MCS.run()
# MCS.plot_hist(bin_size=25)
