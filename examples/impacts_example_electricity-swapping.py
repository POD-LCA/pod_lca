__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.units import KILOGRAM, POUND

project = Project()

factory = Location.from_US_state("Washington")
project.set_location(factory)
project.set_databases()
project.set_year(2025)

CLT_model = project.add_model("CLT_01")

epoxy = CLT_model.add_product(
    name="Aluminum, primary, ingot, at plant, 1998",
    stage="A1",
    qty=1,
    unit=KILOGRAM,
    impacts_from="Aluminum, primary, ingot, at plant, 1998",
)

print(epoxy.get_impacts())

epoxy.set_electricity_source(source="by_location")
print(epoxy.get_impacts())

epoxy.set_qty(200)
epoxy.set_unit(POUND)
print(epoxy.get_impacts())

epoxy.get_electricity().set_geographical_scope("Regional")
print(epoxy.get_impacts())

epoxy.set_production_year(2035)
print(epoxy.get_impacts())

epoxy.get_electricity().set_location(state="Texas")
print(epoxy.get_impacts())

epoxy.set_electricity_source(source="from_database")
print(epoxy.get_impacts())
