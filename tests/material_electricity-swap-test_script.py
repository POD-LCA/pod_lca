
# This script compares the swaping out of electricity impacts of materials values from the Excel tool (given in aa CSV file) with the values calculated using the Python Framework.

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Project 
from pod_lca.units import UNITS_MAP
from pod_lca.utilities import DataImporter
from pod_lca.utilities import config

test_data = "tests\\material_electricity-swap-test_test-values.csv"
output_file = "tests\\material_electricity-swap-test_report.csv"
test_dict = DataImporter.csv_to_dict(test_data, 'test_name')

my_manufacturing_project = Project()

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_data.csv', grouped_data='Electricity')
my_manufacturing_project.set_database(custom_impact_database)

output_dict = {}
impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
emission_inventories = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']
inventories = impact_categories | emission_inventories
for test in tqdm(test_dict):
    my_factory_location = Location.from_US_zip(test_dict[test]['zip code'])
    my_manufacturing_project.set_location(my_factory_location)
    model_one = my_manufacturing_project.add_model("model_01")

    qty = test_dict[test]['qty']
    if isinstance(qty, str):
        qty = float(qty.replace(',', ''))

    year = test_dict[test]['production year']
    if isinstance(year, str):
        year = int(year)

    product = model_one.add_product(name=test, 
                                    stage="A1", 
                                    qty=qty, 
                                    unit=UNITS_MAP[test_dict[test]['unit']], 
                                    impacts_from=test_dict[test]['material'])

    product.set_production_year(year)
    product.set_electricity_source(source=test_dict[test]['electricity_source'])
    if product.electricity['by_location'] is not None:
        product.electricity['by_location'].get_supplier().set_scenario(test_dict[test]['cambium scenario'])
        product.electricity['by_location'].get_supplier().set_geographical_scope(test_dict[test]['regionality'])

    output_dict[test] = { 'test name':test,
                          'material':test_dict[test]['material'],
                          'qty':qty, 
                          'unit':test_dict[test]['unit'],
                          'production_year':year,
                          'electricity_source':test_dict[test]['electricity_source'],
                          'zip_code': my_factory_location.get_zip(), 
                          'regionality': test_dict[test]['regionality'], 
                          'cambium_scenario': test_dict[test]['cambium scenario']
                        }
                                               
    impacts = product.get_impacts()
    emissions = product.get_emissions()
    test_status = True
    for inventory in inventories:
        if inventory in impact_categories:
            records = impacts
        elif inventory in emission_inventories:
            records = emissions
        else:
            raise KeyError(f"Inventory '{inventory}' not found in IMPACT_CATEGORIES or EMISSION_INVENTORIES.")
        if inventory in test_dict[test]:
            output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Python tool'] = records.get_record(inventory)
            output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Excel tool'] = test_dict[test][inventory]

            if (records.get_record(inventory) == 0.0) and (float(test_dict[test][inventory]) == 0):
                dif = 0
            else:
                dif = abs(records.get_record(inventory) - float(test_dict[test][inventory])) / ((records.get_record(inventory) + float(test_dict[test][inventory])) / 2 )  # symmetric difference
                
            output_dict[test][inventory + '_difference (%)'] = dif * 100

            if dif * 100 > 0.5:
                test_status = False
                # print(f"{test} failed on {inventory} with a difference of {dif * 100:.2f}%")
                # print(f"computed impact value: {records.get_record(inventory)} {inventories[inventory]}")
                # print(f"expected impact value: {test_dict[test][inventory]} {inventories[inventory]}")

    output_dict[test]['test status'] = 'PASS' if test_status else 'FAIL'

DataImporter.dict_to_csv(output_dict, output_file)
