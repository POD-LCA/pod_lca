from lca_modules.material.project_manager import Project
from lca_modules.uncertainty.hotspots import HotSpotAnalysis
from lca_modules.uncertainty.data_quality_assessment import DataQualityAnalysis
from lca_modules.uncertainty.sensitivity_analysis import compute_sensitivity_of_param

# CLT example #TODO add reference

project = Project()
project.get_database().import_data_from_CSV(r'data/impact_data.csv')

model_0 = project.get_current_model()

portland_cement = model_0.create_product("Portland cement", "A1")
portland_cement.set_qty(367.410)
portland_cement.set_unit('kg')
portland_cement.set_impact_database_entry("Portland Cement")

fly_ash = model_0.create_product("Fly ash", "A1")
fly_ash.set_qty(367.410)
fly_ash.set_unit('kg')
fly_ash.set_impact_database_entry("Fly Ash")

slag_cement = model_0.create_product("Slag cement", "A1")
slag_cement.set_qty(11.340)
slag_cement.set_unit('kg')
slag_cement.set_impact_database_entry("Slag cement")

water_mixing = model_0.create_product("Water for mixing", "A1")
water_mixing.set_qty(185.519)
water_mixing.set_unit('kg')
water_mixing.set_impact_database_entry("Tap water_ROW_[ecoinvent]")

water_process = model_0.create_product("Water for processing", "A1")
water_process.set_qty(239.681)
water_process.set_unit('kg')
water_process.set_impact_database_entry("Tap water_ROW_[ecoinvent]")

crushed_coarse_aggregate = model_0.create_product("Crushed coarse aggregate", "A1")
crushed_coarse_aggregate.set_qty(71.668)
crushed_coarse_aggregate.set_unit('kg')
crushed_coarse_aggregate.set_impact_database_entry("Gravel_crushed_ROW_[ecoinvent]")

natural_coarse_aggregate = model_0.create_product("Natural coarse aggregate", "A1")
natural_coarse_aggregate.set_qty(900.381)
natural_coarse_aggregate.set_unit('kg')
natural_coarse_aggregate.set_impact_database_entry("Gravel_round_ROW_[ecoinvent]")

crushed_fine_aggregate = model_0.create_product("Crushed fine aggregate", "A1")
crushed_fine_aggregate.set_qty(42.184)
crushed_fine_aggregate.set_unit('kg')
crushed_fine_aggregate.set_impact_database_entry("Gravel_crushed_ROW_[ecoinvent]")

natural_fine_aggregate = model_0.create_product("Natural fine aggregate", "A1")
natural_fine_aggregate.set_qty(712.140)
natural_fine_aggregate.set_unit('kg')
natural_fine_aggregate.set_impact_database_entry("Gravel_round_ROW_[ecoinvent]")

air_entraining_admixture = model_0.create_product("Air entraining admixtures", "A1")
air_entraining_admixture.set_qty(0.037)
air_entraining_admixture.set_unit('kg')
air_entraining_admixture.set_impact_database_entry("Air entrainers_[EFCA]")

plasticizers_superplasticizers = model_0.create_product("Plasticizers and superplasticizers", "A1")
plasticizers_superplasticizers.set_qty(0.255)
plasticizers_superplasticizers.set_unit('kg')
plasticizers_superplasticizers.set_impact_database_entry("Plasticizer and Superplasticizers_[EFCA]")

set_accelerators = model_0.create_product("Set accelerators", "A1")
set_accelerators.set_qty(0.369)
set_accelerators.set_unit('kg')
set_accelerators.set_impact_database_entry("Set accelerators_[EFCA]")

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis(project)
hot_spots_GWP = hotspot_analysis.run(model_name='Model_0', impact_category= "GWP", printout=True)