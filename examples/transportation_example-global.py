
from pod_lca.impacts import TranportationModeImpactsDatabase
from pod_lca.location import Location
from pod_lca.materials_screening import Product
from pod_lca.transportation import USGlobalTransportationManager
from pod_lca.units import M_TON

project = USGlobalTransportationManager.new(name="Building A")
project.set_impact_database(r'data/transportation_podlca_emission.csv')
project.set_data_generator_mode()

product = Product()
product.set_name("Coal")
product.set_qty(1)
product.set_unit(M_TON)
product.set_sctg_code('33')

# origin = Location.from_faf_regions('Mexico') # 'Canada', 'Mexico', 'Rest of Americas', 'Europe', 'Africa', 'SW & Central Asia', 'Eastern Asia', 'SE Asia & Oceania

project.add_good(product, 
                 shipping_dest=Location.from_US_state('Hawaii'), 
                 shipping_org=None, 
                 mode_name='Air', 
                 transport_scenario="Global")

transportation_leg = project.get_transportation_leg(product)[0]

domestic_transport_leg = transportation_leg.get_domestic_leg()
domestic_transport_leg.set_mode('Barge', efficiency=None)
# TODO force mode off

distance = transportation_leg.get_travel_dist()
RTT =  project.transport_legs[product][0].get_return_trip_factor()
impacts = project.get_impacts(product)
emissions = project.get_emissions(product)


print(distance)
print (RTT)
print(transportation_leg.get_domestic_leg().get_travel_dist())
# print (emissions)
