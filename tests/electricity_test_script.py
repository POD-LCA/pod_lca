
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from lca_modules.location.location import Location
from lca_modules.material.project_manager import Project 
from utilities.data_imports.data_importer import Data_Importer
from lca_modules.impacts.units_map import UNITS_MAP
from tqdm import tqdm

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# This script compares the electricity impact values from the Excel tool (given in aa CSV file) with the values calculated using the Python Framework.

test_data = "tests\\electricity_test_test-values.csv"
output_file = "tests\\electricity_test_report.csv"
test_dict = Data_Importer.csv_to_dict(test_data, 'test name')

my_manufacturing_project = Project()
output_dict = {}

for test in tqdm(test_dict):
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
    electricity.set_scenario(test_dict[test]['cambium_scenario'])
    electricity.set_spatial_resolution(test_dict[test]['spatial resolution'])
    output_dict[test] = { 'test name':test,
                          'Zip Code': my_factory_location.get_zip(), 
                          'spatial resolution': test_dict[test]['spatial resolution'], 
                          'year': year, 
                          'cambium_scenario': test_dict[test]['cambium_scenario'],
                          'qty': qty, 
                          'unit': test_dict[test]['unit']}
                                               
    impacts = electricity.get_impacts()
    test_status = True
       
    for impact_cat in IMPACT_CATEGOREIS:
        dif = abs(impacts.get_impact(impact_cat) - float(test_dict[test][impact_cat])) / ((impacts.get_impact(impact_cat) + float(test_dict[test][impact_cat])) / 2 )  # symmetric difference
        
        output_dict[test][impact_cat + '(' + IMPACT_CATEGOREIS[impact_cat] + ')' + ' Python tool'] = impacts.get_impact(impact_cat)
        output_dict[test][impact_cat + '(' + IMPACT_CATEGOREIS[impact_cat] + ')' + ' Excel tool'] = test_dict[test][impact_cat]
        output_dict[test][impact_cat + '_difference (%)'] = dif * 100

        if dif * 100 > 0.5:
            test_status = False
            print(f"{test} failed on {impact_cat} with a difference of {dif * 100:.2f}%")
            print(f"computed impact value: {impacts.get_impact(impact_cat)} {IMPACT_CATEGOREIS[impact_cat]}")
            print(f"expected impact value: {test_dict[test][impact_cat]} {IMPACT_CATEGOREIS[impact_cat]}")

    output_dict[test]['test status'] = 'PASS' if test_status else 'FAIL'


Data_Importer.dict_to_csv(output_dict, output_file)
