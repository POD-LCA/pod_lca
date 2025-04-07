
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from lca_modules.location.location import Location
from lca_modules.material.project_manager import Project 
from utilities.data_imports.csv import CSV_Importer
from lca_modules.impacts.units_map import UNITS_MAP

test_data = "data\\electricity_test_list.csv"
test_dict = CSV_Importer.csv_to_dict(test_data, 'test name')

my_manufacturing_project = Project()


for test in test_dict:
    my_factory_location = Location.from_US_zip(test_dict[test]['Zip Code'])
    my_manufacturing_project.set_location(my_factory_location)
    model_one = my_manufacturing_project.add_model("model_01")

    qty = test_dict[test]['qty']
    if isinstance(qty, str):
        qty = float(qty.replace(',', ''))

    year = test_dict[test]['year']
    if isinstance(year, str):
        year = int(year)

    electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=qty, unit=UNITS_MAP[test_dict[test]['unit']])
    electricity.set_year(year)
    electricity.set_spatial_resolution(test_dict[test]['spatial resolution'])
    electricity.set_scenario(test_dict[test]['cambium_scenario'])

    impacts = electricity.get_impacts()
    test_status = True
    for impact_cat in IMPACT_CATEGOREIS:
        dif = abs(impacts.get_impact(impact_cat) - float(test_dict[test][impact_cat])) / ((impacts.get_impact(impact_cat) + float(test_dict[test][impact_cat])) / 2 )  # symmetric difference
        if dif * 100 > 0.5:
            test_status = False
            print(f"{test} failed on {impact_cat} with a difference of {dif * 100:.2f}%")
            print(f"computed impact value: {impacts.get_impact(impact_cat)} {IMPACT_CATEGOREIS[impact_cat]}")
            print(f"expected impact value: {test_dict[test][impact_cat]} {IMPACT_CATEGOREIS[impact_cat]}")

    if test_status:
        print(f"{test} passesd")
