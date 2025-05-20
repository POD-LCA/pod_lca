
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Project
from pod_lca.uncertainty import HotSpotAnalysis
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import KILOMETER
from pod_lca.units import WATT_HOUR

project = Project()

factory = Location.from_str("98126, seattle")
project.set_location(factory)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_data.csv', grouped_data='Electricity')
project.set_database(custom_impact_database)

CLT_model = project.add_model("CLT_01")

epoxy = CLT_model.add_product(name="Epoxy", stage="A1", qty=100, unit=KILOGRAM, impacts_from="Epoxy; at plant")

print(epoxy.get_impacts())

epoxy.set_electricity_source(source='by_location')
print(epoxy.get_impacts())

epoxy.set_electricity_source(source='from_database')
print(epoxy.get_impacts())

epoxy.set_electricity_source(source='by_location')
print(epoxy.get_impacts())

epoxy.set_qty(200)
print(epoxy.get_impacts())

epoxy.get_electricity().set_spatial_resolution("National")
epoxy.update_inventory_records()
print(epoxy.get_impacts())
