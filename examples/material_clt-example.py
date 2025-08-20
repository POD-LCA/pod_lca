
# CLT model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.uncertainty import HotSpotAnalysis
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import KILOMETER
from pod_lca.units import WATT_HOUR
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

project = Project()

factory = Location.from_str("Seattle, Washington")
project.set_location(factory)
project.set_year(2025)

pod_lca_impact_database = ImpactsDatabase.new("pod_lca_impact_database")
pod_lca_impact_database.set_data(r'data/impacts_podlca_data.csv', 
                                 grouped_data='Electricity', 
                                 density_headers=["Density (dry basis)", "Density unit"])
project.set_impact_database(pod_lca_impact_database)

project.set_transportation_mode_impact_database(r'data/transportation_podlca_emission.csv')

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=1.21, unit=CUBIC_METER, 
                               impacts_from="Sawn lumber; softwood; planed; kiln dried; packaged; at planer; PNW", sctg_code=26)
meth_diphenyl_d = CLT_model.add_product(name="Methylene diphenyl diisocyanate resin", stage="A1", qty=3.22, unit=KILOGRAM, 
                                        impacts_from="Methylene diphenyl diisocyanate, MDI, at plant, US PNW", sctg_code=28)
prop_glycol = CLT_model.add_product(name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, 
                                    impacts_from="Ethylene glycol, materials production, organic compound, at plant, kg", sctg_code=28)
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None, sctg_code=28)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None, sctg_code=28)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None, sctg_code=28)

electricity = CLT_model.add_electricity(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR)

natural_gas = CLT_model.add_energy(name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, 
                                   impacts_from="Natural gas, combusted in industrial equipment")

print(CLT_model)
print(project)

# CLT_model.set_products_electricity_source('by_location') # TODO: integrate electricity
drf_record = CLT_model.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('instantaneous radiative forcing')

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
print(hotspot_analysis)

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(CLT_model.get_impacts_by_LCstages('GWP'), "Parameter by category", "Category", "Parameter (unit)")
graph.show()
