
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

project = Project()

factory = Location.from_str("98126, seattle")
project.set_location(factory)

impacts_header_map = {"GWP":"GWP",
                      "AP":"AP",
                      "EP":"EP",
                      "ODP":"ODP",
                      "SFP":"POCP"}
custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_material-data.csv', impact_headers_map=impacts_header_map)
project.set_database(custom_impact_database)

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=562.75, unit=KILOGRAM, impacts_from="Lumber_[CORRIM_LCA]")
meth_diphenyl_d = CLT_model.add_product(name="Methylene diphenyl diisocyanate resin", stage="A1", qty=3.22, unit=KILOGRAM, impacts_from="Methylene diphenyl diisocyanate resin_[FHWA_MTU]")
prop_glycol = CLT_model.add_product(name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, impacts_from="Propylene glycol_[ecoinvent]")
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None)
electricity = CLT_model.add_electricity(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR)
natural_gas = CLT_model.add_energy(name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, impacts_from="Natural gas_insustrial_equipment_[USLCI]")

lumber_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=302, unit=KILOMETER, impacts_from="Transportation_combination_truck_short-haul_diesel_NW_[USLCI]")
lumber_by_truck.set_transported_product(lumber)

PUR1_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=2160, unit=KILOMETER, impacts_from="Transportation_combination_truck_diesel_US_[USLCI]")
PUR1_by_truck.set_transported_product(dummy_PUR_1)

PUR2_by_truck = CLT_model.add_transportation_process(name="Lumber Transportation", stage="A2", transported_distance=64800, unit=KILOMETER, impacts_from="Transportation_freight_train_diesel_US_[ecoinvent]")
PUR2_by_truck.set_transported_product(dummy_PUR_2)

print(CLT_model)
print(project)

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
print(hotspot_analysis)
