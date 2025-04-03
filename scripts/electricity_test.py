from lca_modules.material.project_manager import Project 
from lca_modules.location.location import Location
from utilities.units.common_units import WATT_HOUR
from utilities.units.metric_prefixes import MEGA, KILO

my_manufacturing_project = Project()
tests = {'test_01': {'location': 'USA', 'elec_qty': 1, 'yr': 2025, 'sp_res': 'National', 'scenario': 'MidCase'},
         'test_02': {'location': 'USA', 'elec_qty': 1, 'yr': 2037, 'sp_res': 'National', 'scenario': 'MidCase'},
         'test_03': {'location': '60601, USA', 'elec_qty': 6000, 'yr': 2025, 'sp_res': 'Local', 'scenario': 'MidCase'},
         'test_04': {'location': '90210, USA', 'elec_qty': 6000, 'yr': 2025, 'sp_res': 'Regional', 'scenario': 'MidCase'},
         'test_05': {'location': '30025, USA', 'elec_qty': 2500, 'yr': 2060, 'sp_res': 'Regional', 'scenario': 'Decarb95by2050'}}

for test in tests:

    my_factory_location = Location.from_str(tests[test]['location'])

    my_manufacturing_project.set_location(my_factory_location)

    model_one = my_manufacturing_project.add_model("model_01")

    electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=tests[test]['elec_qty'], unit=MEGA * WATT_HOUR)
    electricity.set_year(tests[test]['yr'])
    electricity.set_spatial_resolution(tests[test]['sp_res'])
    electricity.set_scenario(tests[test]['scenario'])

    impacts = electricity.get_impacts()
    print(impacts)
