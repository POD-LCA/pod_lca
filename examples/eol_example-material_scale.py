__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.location import Location
from pod_lca.units import CUBIC_METER
from pod_lca.units import MEGA
from pod_lca.units import METER
from pod_lca.units import WATT_HOUR

project = Project()

project.set_location(Location.from_str("Seattle, Washington"))
project.set_year(2025)
project.set_databases()

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(
    name="Lumber",
    stage="A1",
    qty=1.21,
    unit=CUBIC_METER,
    impacts_from="Sawn lumber; softwood; planed; kiln dried; packaged; at planer; PNW",
    sctg_code=26,
    eol_material="Wood",
)

print(lumber.get_carbon_storage())

# set material EOL
lumber.set_waste_product(expiry_year=2050)

print(lumber.waste_obj.get_emissions())

# # impacts by cycle stage
# impacts_dict = {}
# emissions_dict = {}
# for material in my_bamboo_roof.get_materials():
#     for lc_stage in ["C1", "C2", "C3", "C4", "D"]:
#         impacts_dict[lc_stage] = material.get_eol_impacts(lc_stage=lc_stage)
#         emissions_dict[lc_stage] = material.get_eol_emissions(lc_stage=lc_stage)


# for lc_stage, impact in impacts_dict.items():
#     print(f"Life cycle stage: {lc_stage}")
#     print(impact)
