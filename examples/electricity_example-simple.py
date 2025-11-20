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

my_factory_location = Location.from_US_zip("81049")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1, unit=MEGA * WATT_HOUR)
electricity.set_year(2040)  # repick region after setting year
electricity.set_scenario("HighDemandGrowth")  # repick region after setting scenario
electricity.set_geographical_scope("Regional")

impacts = electricity.get_impacts()
print(impacts)
