
from pod_lca.impacts import TranportationModeImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Master
from pod_lca.transportation import ProjectLogisticManager
from pod_lca.units import M_TON

project = ProjectLogisticManager.new(name="Building A")
#TODO: SCTG code mapping to database

transport_impact_database = TranportationModeImpactsDatabase.new("POD|LCA transport data")
transport_impact_database.set_data(r'data/transportation_podlca_emission.csv')
project.set_database(transport_impact_database)

product = Master()
product.set_name("FireSprinklers")
product.set_qty(1)
product.set_unit(M_TON)

destination_state = Location.from_US_state('Georgia')

project.add_good(product, shipping_dest=destination_state, shipping_org=None, mode_name="Truck", transport_scenario="Local")

print(project.get_impacts(product))
print (project.get_link(product)[0].get_travel_dist())
