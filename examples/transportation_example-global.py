from pod_lca.location import Location
from pod_lca.materials_screening import Product
from pod_lca.transportation import USGlobalTransportationManager
from pod_lca.units import M_TON

project = USGlobalTransportationManager.new(name="Building A")
project.set_impact_database(r"data/transportation_podlca_emission.csv")

product = Product()
product.set_name("Coal")
product.set_qty(1)
product.set_unit(M_TON)
product.set_sctg_code("01")

destination_state = Location.from_US_state("Utah")
origin = Location.from_str("Rest of America")
# origin = Location.from_faf_regions(faf_region='Africa')

project.add_good(product, shipping_dest=None, shipping_org=None, mode_name=None, transport_scenario="Global")

transportation_leg = project.get_transportation_leg(product)[0]
distance = transportation_leg.get_travel_dist()
RTT = project.transport_legs[product][0].get_return_trip_factor()
impacts = project.get_impacts(product)
emissions = project.get_emissions(product)

print(distance)
print(impacts)
print(emissions)
