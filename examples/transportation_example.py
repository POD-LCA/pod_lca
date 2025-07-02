
from pod_lca.transportation import ProjectLogisticManager
from pod_lca.impacts import TranportationModeImpactsDatabase
from pod_lca.material_screening import Master
from pod_lca.units import KILOGRAM

project = ProjectLogisticManager.new(name="Building A")
#TODO: SCTG code mapping to database

transport_impact_database = TranportationModeImpactsDatabase.new("POD|LCA transport data")
transport_impact_database.set_data(r'data/transportation_podlca_emission.csv')
project.set_database(transport_impact_database)

product = Master()
product.set_name("CeilingPanel")
product.set_qty(1.5)
product.set_unit(KILOGRAM)

project.add_goods([product], shipping_dest='Arizona', shipping_org='Seattle')

print(project.get_impacts(product))
print (project.get_link(product).get_travel_dist())
