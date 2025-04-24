from lca_modules.location.location import Location
from lca_modules.material.project_manager import Project
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.uncertainty.hotspots import HotSpotAnalysis
from utilities.units.common_units import KILOGRAM, WATT_HOUR, KILO


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# Concrete model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

project = Project()

concrete_yard = Location.from_str("98126, Seattle")
project.set_location(concrete_yard)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impact_data.csv')
project.set_database(custom_impact_database)

concrete_model = project.add_model("concrete_01")

portland_cement = concrete_model.add_product(name="Portland cement", stage="A1", qty=367.410, unit=KILOGRAM, impacts_from="Portland Cement")
fly_ash = concrete_model.add_product(name="Fly ash", stage="A1", qty=367.410, unit=KILOGRAM, impacts_from="Fly Ash")
slag_cement = concrete_model.add_product(name="Slag cement", stage="A1", qty=11.340, unit=KILOGRAM, impacts_from="Slag cement")
water_mixing = concrete_model.add_product(name="Water for mixing", stage="A1", qty=185.519, unit=KILOGRAM, impacts_from="Tap water_ROW_[ecoinvent]")
water_process = concrete_model.add_product(name="Water for processing", stage="A1", qty=239.681, unit=KILOGRAM, impacts_from="Tap water_ROW_[ecoinvent]")
crushed_coarse_aggregate = concrete_model.add_product(name="Crushed coarse aggregate", stage="A1", qty=71.668, unit=KILOGRAM, impacts_from="Gravel_crushed_ROW_[ecoinvent]")
natural_coarse_aggregate = concrete_model.add_product(name="Natural coarse aggregate", stage="A1", qty=900.381, unit=KILOGRAM, impacts_from="Gravel_round_ROW_[ecoinvent]")
crushed_fine_aggregate = concrete_model.add_product(name="Crushed fine aggregate", stage="A1", qty=42.184, unit=KILOGRAM, impacts_from="Gravel_crushed_ROW_[ecoinvent]")
natural_fine_aggregate = concrete_model.add_product(name="Natural fine aggregate", stage="A1", qty=712.140, unit=KILOGRAM, impacts_from="Gravel_round_ROW_[ecoinvent]")
air_entraining_admixture = concrete_model.add_product(name="Air entraining admixtures", stage="A1", qty=0.037, unit=KILOGRAM, impacts_from="Air entrainers_[EFCA]")
plasticizers_superplasticizers = concrete_model.add_product(name="Plasticizers and superplasticizers", stage="A1", qty=0.255, unit=KILOGRAM, impacts_from="Plasticizer and Superplasticizers_[EFCA]")
set_accelerators = concrete_model.add_product(name="Set accelerators", stage="A1", qty=0.369, unit=KILOGRAM, impacts_from="Set accelerators_[EFCA]")

electricity = concrete_model.add_electricity(name="Electricity", stage="A3", qty=4.72, unit=KILO * WATT_HOUR)
# TODO: Add transportation processes

print(concrete_model)
print(project)
print(electricity)

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(concrete_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
print(hotspot_analysis)
