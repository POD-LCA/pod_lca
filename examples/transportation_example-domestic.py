
from pod_lca.impacts import TranportationModeImpactsDatabase
from pod_lca.location import Location
from pod_lca.materials_screening import Product
from pod_lca.transportation import USDomesticTransportationManager
from pod_lca.units import M_TON

project = USDomesticTransportationManager.new(name="Building A")
project.set_impact_database(r'data/transportation_podlca_emission.csv')

product = Product()
product.set_name("Crushed stone")
product.set_qty(1)
product.set_unit(M_TON)
product.set_sctg_code('11')

project.force_mode = False
project.force_location = False

project.add_good(product, 
                 shipping_dest=Location.from_US_state('Maryland'), 
                 shipping_org=None, 
                 mode_name=None,
                 transport_scenario=None,
                 mode_efficiency=None)

transport_leg = project.get_transportation_leg(product)[0]
distance = transport_leg.get_travel_dist()
RTT =  project.transport_legs[product][0].get_return_trip_factor()
impacts = project.get_impacts(product)
emissions = project.get_emissions(product)

print(distance)
print(transport_leg.get_transport_scenario())
print (impacts)
print (emissions)
