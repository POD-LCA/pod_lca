from lca_modules.material.project_manager import Project 
from lca_modules.location.location import Location
from utilities.units.common_units import WATT_HOUR, KILO  

my_manufacturing_project = Project()

my_factory_location = Location.from_str("98126, seattle")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

# user adding electricity to the model
electricity = model_one.add_energy(name="Electricity", stage="A3", qty=1000, unit=KILO * WATT_HOUR)

# Advanced operations
electricity_supplier = electricity.get_supplier()
print(electricity_supplier)

impacts = electricity_supplier.get_impacts()
print(impacts) # FIXME: units missmatch

electricity_supplier.set_year(2045)
electricity_supplier.set_spatial_resolution('Regional')
print(electricity_supplier)
print(impacts)

# electricity_supplier.set_scenario('Decarb95by2050')
# set different mix
# directly set a producer
