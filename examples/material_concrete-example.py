# Concrete model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.uncertainty import HotSpotAnalysis
from pod_lca.units import KILO
from pod_lca.units import KILOGRAM
from pod_lca.units import WATT_HOUR

project = Project()

concrete_yard = Location.from_str("Seattle, Washington")
project.set_location(concrete_yard)

project.set_impact_database(r"src/pod_lca/data/impacts_podlca_material-data.csv")
project.set_transportation_mode_impact_database(r"src/pod_lca/data/transportation_podlca_emission.csv")

concrete_model = project.add_model("concrete_01")

portland_cement = concrete_model.add_product(
    name="Portland cement", stage="A1", qty=367.410, unit=KILOGRAM, impacts_from="Portland Cement", sctg_code=32
)
fly_ash = concrete_model.add_product(
    name="Fly ash", stage="A1", qty=367.410, unit=KILOGRAM, impacts_from="Fly Ash", sctg_code=19
)
slag_cement = concrete_model.add_product(
    name="Slag cement", stage="A1", qty=11.340, unit=KILOGRAM, impacts_from="Slag cement", sctg_code=32
)
water_mixing = concrete_model.add_product(
    name="Water for mixing",
    stage="A1",
    qty=185.519,
    unit=KILOGRAM,
    impacts_from="Tap water_ROW_[ecoinvent]",
    sctg_code=20,
)
water_process = concrete_model.add_product(
    name="Water for processing",
    stage="A1",
    qty=239.681,
    unit=KILOGRAM,
    impacts_from="Tap water_ROW_[ecoinvent]",
    sctg_code=20,
)
crushed_coarse_aggregate = concrete_model.add_product(
    name="Crushed coarse aggregate",
    stage="A1",
    qty=71.668,
    unit=KILOGRAM,
    impacts_from="Gravel_crushed_ROW_[ecoinvent]",
    sctg_code=31,
)
natural_coarse_aggregate = concrete_model.add_product(
    name="Natural coarse aggregate",
    stage="A1",
    qty=900.381,
    unit=KILOGRAM,
    impacts_from="Gravel_round_ROW_[ecoinvent]",
    sctg_code=31,
)
crushed_fine_aggregate = concrete_model.add_product(
    name="Crushed fine aggregate",
    stage="A1",
    qty=42.184,
    unit=KILOGRAM,
    impacts_from="Gravel_crushed_ROW_[ecoinvent]",
    sctg_code=31,
)
natural_fine_aggregate = concrete_model.add_product(
    name="Natural fine aggregate",
    stage="A1",
    qty=712.140,
    unit=KILOGRAM,
    impacts_from="Gravel_round_ROW_[ecoinvent]",
    sctg_code=31,
)
air_entraining_admixture = concrete_model.add_product(
    name="Air entraining admixtures",
    stage="A1",
    qty=0.037,
    unit=KILOGRAM,
    impacts_from="Air entrainers_[EFCA]",
    sctg_code=28,
)
plasticizers_superplasticizers = concrete_model.add_product(
    name="Plasticizers and superplasticizers",
    stage="A1",
    qty=0.255,
    unit=KILOGRAM,
    impacts_from="Plasticizer and Superplasticizers_[EFCA]",
    sctg_code=28,
)
set_accelerators = concrete_model.add_product(
    name="Set accelerators", stage="A1", qty=0.369, unit=KILOGRAM, impacts_from="Set accelerators_[EFCA]", sctg_code=28
)

electricity = concrete_model.add_electricity(name="Electricity", stage="A3", qty=4.72, unit=KILO * WATT_HOUR)

print(concrete_model)
print(project)
print(electricity)

concrete_model.set_products_electricity_source("by_location")

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(concrete_model)
hot_spots_GWP = hotspot_analysis.run(impact_category="GWP")
print(hotspot_analysis)
