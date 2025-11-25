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

factory = Location.from_str("Seattle, Washington")
project.set_location(factory)
project.set_year(2025)

pod_lca_impact_database = ImpactsDatabase.new("pod_lca_impact_database")
pod_lca_impact_database.set_data(
    r"src/pod_lca/data/impacts_podlca_data.csv",
    grouped_data="Electricity",
    density_headers=["Wet Density", "Density unit"],
    additional_headers=["Biomaterial Species","Region","Biomaterial Form"],
)
project.set_impact_database(pod_lca_impact_database)

project.set_transportation_mode_impact_database(r"src/pod_lca/data/transportation_podlca_emission.csv")

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(
    name="Lumber",
    stage="A1",
    qty=1.21,
    unit=CUBIC_METER,
    impacts_from="Sawn lumber; softwood; planed; kiln dried; packaged; at planer; PNW",
    sctg_code=26,
)

# set material EOL
lumber.set_waste_product()

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
