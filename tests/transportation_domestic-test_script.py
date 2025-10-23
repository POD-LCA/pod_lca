
# This script compares the transportation impact values from the manual method (given in as a CSV file) with the values calculated using the Python Framework.

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm
import time

import pandas as pd

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import WATT_HOUR
from pod_lca.transportation import USDomesticTransportationManager
from pod_lca.materials_screening import Product
from pod_lca.units import UNITS_MAP
from pod_lca.location import Location
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter
from pod_lca.utilities import config

test_data = "tests\\transportation-domestic_test_test-values.csv"
output_file = "tests\\transportation-domestic_test_report.csv"
test_dict = DataImporter.csv_to_dict(test_data, 'test name')

project = USDomesticTransportationManager.new("Building A")
project.set_data_generator_mode()
project.set_impact_database(r'data/transportation_podlca_emission.csv')
electricity_report_unit = KILO * WATT_HOUR

output_dict = {}
impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
emission_inventories = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']
inventories = impact_categories | emission_inventories
for test in tqdm(test_dict):
    product = Product()
    product.set_name(test_dict[test]['product'])
    product.set_qty(float(test_dict[test]['qty']))
    product.set_unit(UNITS_MAP[test_dict[test]['unit']])
    product.set_sctg_code(test_dict[test]['sctg_code'])

    origin_state_obj = None if test_dict[test]['origin'] == '' else Location.from_US_state(test_dict[test]['origin'])
    destination_state_obj = None if test_dict[test]['destination'] == '' else Location.from_US_state(test_dict[test]['destination']) 
    scenario = None if test_dict[test]['transport_scenario'] == '' else test_dict[test]['transport_scenario']
    mode = None if test_dict[test]['mode'] == '' else test_dict[test]['mode']
    efficiency = None if test_dict[test]['efficiency'] == '' else test_dict[test]['efficiency']

    project.add_good(good=product, 
                     shipping_dest=destination_state_obj, 
                     shipping_org=origin_state_obj,
                     transport_scenario=scenario,
                     distance_unit=KILOMETER,
                     mode_name=mode,
                     mode_efficiency=efficiency) 
    
    output_dict[test] = {
        'test name': test,
        'product': test_dict[test]['product'],
        'sctg_code': test_dict[test]['sctg_code'],
        'qty': test_dict[test]['qty'],
        'unit': test_dict[test]['unit'],
        'destination': test_dict[test]['destination'],
        'origin': test_dict[test]['origin'],
        'mode': test_dict[test]['mode'],
        'efficiency': test_dict[test]['efficiency'],
        'transport_scenario': test_dict[test]['transport_scenario']
    }

    test_status = True
    transport_leg = project.get_transportation_leg(product)[0]
    conversion_factor = KILOMETER.convert_to(UNITS_MAP[test_dict[test]['distance_unit']])
    try:
        distance = transport_leg.get_travel_dist() * conversion_factor
    except Exception as e:
        # set results to N/A
        output_dict[test]['distance (Python tool)'] = 'N/A'
        output_dict[test]['distance (Manual calc)'] = test_dict[test]['distance']
        output_dict[test]['distance_unit'] = test_dict[test]['distance_unit']
        output_dict[test]['distance_difference (%)'] = 'N/A'
        for inventory in inventories:
            if inventory in test_dict[test]:
                output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Python tool'] = 'N/A'
                output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Manual calc'] = test_dict[test][inventory]
                output_dict[test][inventory + '_difference (%)'] = 'N/A'
        output_dict[test]['test status'] = 'N/A'
        # Note error
        output_dict[test]['Notes'] = e
        continue

    # check distance
    dif = abs(distance - float(test_dict[test]['distance'])) / ((distance + float(test_dict[test]['distance'])) / 2 )  # symmetric difference
    
    output_dict[test]['distance (Python tool)'] = distance
    output_dict[test]['distance (Manual calc)'] = test_dict[test]['distance']
    output_dict[test]['distance_unit'] = test_dict[test]['distance_unit']
    output_dict[test]['distance_difference (%)'] = dif * 100   
    if dif * 100 > 0.5:
        test_status = False
        print(f"{test} failed on distance with a difference of {dif * 100:.2f}%")
        print(f"computed distance value: {distance}")
        print(f"expected distance value: {test_dict[test]['distance']}")      

    impacts = project.get_impacts(product)
    emissions = project.get_emissions(product)
    # check inventories
    for inventory in inventories:
        if inventory in impact_categories:
            records = impacts
        elif inventory in emission_inventories:
            records = emissions
        else:
            raise KeyError(f"Inventory '{inventory}' not found in IMPACT_CATEGORIES or EMISSION_INVENTORIES.")
        if inventory in test_dict[test]:
            dif = abs(records.get_record(inventory) - float(test_dict[test][inventory])) / ((records.get_record(inventory) + float(test_dict[test][inventory])) / 2 )  # symmetric difference
            
            output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Python tool'] = records.get_record(inventory)
            output_dict[test][inventory + '(' + inventories[inventory] + ')' + ' Manual calc'] = test_dict[test][inventory]
            output_dict[test][inventory + '_difference (%)'] = dif * 100

            if dif * 100 > 0.5:
                test_status = False
                print(f"{test} failed on {inventory} with a difference of {dif * 100:.2f}%")
                print(f"computed impact value: {records.get_record(inventory)} {inventories[inventory]}")
                print(f"expected impact value: {test_dict[test][inventory]} {inventories[inventory]}")

    output_dict[test]['test status'] = 'PASS' if test_status else 'FAIL'
    output_dict[test]['Notes'] = ''

DataExporter.dict_to_csv(output_dict, output_file)
