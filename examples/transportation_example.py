
from pod_lca.impacts import TranportationModeImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Product
from pod_lca.transportation import USDomesticLogisticProject
from pod_lca.units import M_TON

project = USDomesticLogisticProject.new(name="Building A")
project.set_impact_database(r'data/transportation_podlca_emission.csv')

product = Product()
product.set_name("FireSprinklers")
product.set_qty(1)
product.set_unit(M_TON)
product.set_sctg_code()

destination_state = Location.from_US_state('Georgia')

project.add_good(product, shipping_dest=destination_state, shipping_org=None, mode_name="Truck", transport_scenario="Local")

link = project.get_link(product)[0]
distance = link.get_travel_dist()
RTT =  project.links[product][0].get_return_trip_factor()
impacts = project.get_impacts(product)
emissions = project.get_emissions(product)

print(distance)
print (impacts)
print (emissions)
