
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.materials_screening import Project 
from pod_lca.location import Location
from pod_lca.units import MEGA
from pod_lca.units import WATT_HOUR

my_manufacturing_project = Project()

# =================================
# Set project location
# ================================= 
# Spatial resolution ('National', 'Regional', 'Local') will be automatically detected as the location is set
# If no location is set, the spatial resolution will be set to 'National' (and 'USA') by default.
# my_factory_location = Location.from_US_zip("98105")
# my_factory_location = Location.from_str("oklahoma")
my_factory_location = Location.from_str("USA")

my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

# =================================
# create electricity product
# =================================
electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=6000, unit=MEGA * WATT_HOUR)

# creating electricity product will automatically create a supplier
electricity_supplier = electricity.get_supplier()
print(electricity_supplier)

# =================================
# Electricity impacts
# =================================
# electiriciyt supplier would hold the unit impacts
unit_impacts = electricity_supplier.get_unit_impacts()
print(unit_impacts)

# electricity product would hold the product impacts
impacts = electricity.get_impacts()
print(impacts)

# =================================
# Change electricity supply year
# =================================
# changing the electricity supplier year would only change the unit impacts
# and not the electricity product impacts
electricity_supplier.set_year(2037)

unit_impacts = electricity_supplier.get_unit_impacts()
impacts = electricity.get_impacts()
print(unit_impacts)
print(impacts)

# to change the electricity product impacts, we need to set the year on the electricity product
# this will automatically update the supplier year as well
electricity.set_year(2045)
print(electricity.get_impacts())

# =================================
# Change electricity spatial resolution
# =================================
# changing the electricity supplier spatial resolution would only change the unit impacts
# and not the electricity product impacts
electricity_supplier.set_geographical_scope('Regional')

unit_impacts = electricity_supplier.get_unit_impacts()
impacts = electricity.get_impacts()
print(unit_impacts)
print(impacts)

# to change the electricity product impacts, we need to set the spatial resolution on the electricity product
# this will automatically update the supplier year as well
electricity.set_geographical_scope('Regional')

unit_impacts = electricity_supplier.get_unit_impacts()
impacts = electricity.get_impacts()
print(unit_impacts)
print(impacts)

# =================================
# Change electricity scenario
# =================================
# changing the electricity supplier scenario would only change the unit impacts
# and not the electricity product impacts
electricity_supplier.set_scenario('Decarb95by2050')

unit_impacts = electricity_supplier.get_unit_impacts()
impacts = electricity.get_impacts()
print(unit_impacts)
print(impacts)

# to change the electricity product impacts, we need to set the scenario on the electricity product
# this will automatically update the supplier year as well
electricity.set_scenario('Decarb95by2050')

unit_impacts = electricity_supplier.get_unit_impacts()
impacts = electricity.get_impacts()
print(unit_impacts)
print(impacts)
