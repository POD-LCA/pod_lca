from lca_modules.material.project_manager import Project 
from lca_modules.location.location import Location
from utilities.units.common_units import WATT_HOUR
from utilities.units.metric_prefixes import MEGA, KILO

my_manufacturing_project = Project()

my_factory_location = Location.from_US_zip("61336")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1, unit=MEGA * WATT_HOUR)
electricity.set_year(2025) # repick region after setting year
electricity.set_scenario('LowNGPrice') # repick region after setting scenario
electricity.set_spatial_resolution("Regional")

impacts = electricity.get_impacts()
print(impacts)