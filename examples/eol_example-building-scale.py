__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import Floor
from pod_lca.building import Assembly
from pod_lca.building import Material
from pod_lca.location import Location
from pod_lca.units import KILOGRAM
from pod_lca.units import MEGA
from pod_lca.units import METER
from pod_lca.units import WATT_HOUR

# create building
my_building = Building()
my_building.set_location(Location.from_str("98126, Seattle"))
my_building.set_built_year(2025)
my_building.set_life_span(60)
my_building.set_building_type("residential")
my_building.set_databases('ASHRAE')
my_building.set_building_level_products(logistic_type='local',
                                             construction_electricity_consumption=0.0,
                                             electricity_unit=MEGA * WATT_HOUR)

my_building.add_floor(floor_no=1, 
                      floor_plan=[[0.0 , 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0]], 
                      floor_height=3, 
                      geometry_unit=METER,
                      below_grade=False, 
                      on_ground=True, 
                      is_last=True)

# create bamboo roof assembly and material
my_bamboo_roof = Assembly.create(
    name="Bamboo Roof", 
    building=my_building, 
)  
bamboo = Material.new(my_bamboo_roof, 
                      name="Bamboo Material", 
                      qty=538, 
                      unit=KILOGRAM, 
                      material_database_entry=None, 
                      product_year=my_building.get_built_year(),
                      service_life=None)
my_bamboo_roof.add_material(bamboo) 

# set material EOL
bamboo.set_eol_material("Bamboo")
bamboo.set_waste_product()

# impacts by cycle stage
impacts_dict = {}
emissions_dict = {}
for material in my_bamboo_roof.get_materials():
    for lc_stage in ["C1", "C2", "C3", "C4", "D"]:
        impacts_dict[lc_stage] = material.get_eol_impacts(lc_stage=lc_stage)
        emissions_dict[lc_stage] = material.get_eol_emissions(lc_stage=lc_stage)

for lc_stage, impact in impacts_dict.items():
    print(f"Life cycle stage: {lc_stage}")
    print(impact)

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')
