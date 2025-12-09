__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.units import CUBIC_METER

project = Project.new()

factory = Location.from_str("Seattle, Washington")
project.set_location(factory)
project.set_year(2025)

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(
    name="Lumber",
    stage="A1",
    qty=1,
    unit=CUBIC_METER,
    impacts_from="Sawn lumber; softwood; planed; kiln dried; packaged; at planer; PNW",
    sctg_code=26,
)

print(lumber.get_carbon_storage())
print(lumber.get_impacts())
