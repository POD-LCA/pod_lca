
# CLT model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import exp
from numpy import log
from numpy import sqrt
from scipy import stats

from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Project
from pod_lca.uncertainty import DataDistribution
from pod_lca.uncertainty import MonteCarloSimulator
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import KILOMETER
from pod_lca.units import WATT_HOUR
from pod_lca.utilities import config
from pod_lca.visualizer import Histogram
from pod_lca.visualizer import MatplotlibPlotter

project = Project()

factory = Location.from_str("98126, seattle")
project.set_location(factory)

project.set_impact_database(r'data/impacts_podlca_material-data.csv')
project.set_transportation_mode_impact_database(r'data/transportation_podlca_emission.csv')

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=562.75, unit=KILOGRAM, impacts_from="Lumber_[CORRIM_LCA]")
meth_diphenyl_d = CLT_model.add_product(name="Methylene diphenyl diisocyanate resin", stage="A1", qty=3.22, unit=KILOGRAM, impacts_from="Methylene diphenyl diisocyanate resin_[FHWA_MTU]")
prop_glycol = CLT_model.add_product(name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, impacts_from="Propylene glycol_[ecoinvent]")
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
electricity = CLT_model.add_electricity(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR)
natural_gas = CLT_model.add_energy(name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, impacts_from="Natural gas_insustrial_equipment_[USLCI]")

print(CLT_model)
print(project)

MCS = MonteCarloSimulator.from_model(CLT_model, no_iter=10000, impact_cat='GWP')

# uncertainty of lumber quantity
mean_val, sdev_val = 562.750, 1.5
sigma = sqrt(log(1 + (sdev_val**2 / mean_val**2)))
mu = log(mean_val) - 0.5 * sigma**2

dist = stats.lognorm(s=sigma, loc=0, scale=exp(mu))

data_set = DataDistribution.from_distributions(dist, is_cts=True)
lumber.set_data_distribution(data_set, 'qty')

# uncertainity of resin quantity
data = [3.78191187, 2.75914279, 1.95508751, 2.96100281, 1.8551113 ,2.62276916, 2.38929469, 3.34390811, 2.11003882, 0.58102906,3.28672522, 2.30193206, 3.45025548, 4.92072669, 2.99540316,
        1.76820646, 2.93650962, 6.24726201, 3.668859  , 1.06279295, 4.87829566, 4.22748717, 2.5929637 , 2.13076645, 3.98635723, 3.71329549, 2.95218779, 3.86155413, 2.52430829, 3.98351926,
        3.75261862, 4.32160263, 0.84863997, 2.4135882 , 6.53763601]

data_set = DataDistribution.from_data(data, is_cts=True)
meth_diphenyl_d.set_data_distribution(data_set, 'qty')

# uncertainty of electricity source
data = ["Electricity_New", "Electricity_NWPP(eGrid)_[USLCI]"]

data_set = DataDistribution.from_data(data, is_cts=False)
electricity.set_data_distribution(data_set, 'impact_database_entry')

# set colors for the histogram
COLOUR_BASE = config['Preferences']['COLOUR_BASE']
COLOUR_PALETTES = config['Preferences']['COLOUR_PALETTES']
COLOUR_ORDER_LIST = config['Preferences']['COLOUR_ORDER_LIST']
# run different cases
cases = [1, 2]
graph = Histogram.from_plotter(MatplotlibPlotter)
for case in cases:
    if case ==1: 
        MCS.set_var_params([lumber.get_data_distribution(attr='qty')])
    elif case ==2: 
        MCS.set_var_params([meth_diphenyl_d.get_data_distribution(attr='qty')])
    elif case == 3: 
        MCS.set_var_params([electricity.get_data_distribution(attr='impact_database_entry')])
    elif case == 4: # uncertainty of electricity source, with known likelyhoods
        xk = ["Electricity_New", "Electricity_NWPP(eGrid)_[USLCI]"]
        pk = [0.7, 0.3]

        dist = stats.rv_discrete(name='custm', values=(xk, pk))

        data_set = DataDistribution.from_distributions(dist, is_cts=False)
        electricity.set_data_distribution(data_set, 'impact_database_entry')

        MCS.set_var_params([electricity.get_data_distribution(attr='impact_database_entry')])
    elif case == 5:
        MCS.set_var_params([lumber.get_data_distribution(attr='qty'), meth_diphenyl_d.get_data_distribution(attr='qty')])
    else:
        MCS.set_var_params()

    MCS.run()
    print(MCS)
    graph.draw(MCS.result.get_data(), no_bins=100, title="Distribution from Monte Carlo Simulation.", x_label='Impact', y_label="count", label='case '+str(case), color=COLOUR_PALETTES[COLOUR_ORDER_LIST[case]][1], unitize=True)

graph.show()
