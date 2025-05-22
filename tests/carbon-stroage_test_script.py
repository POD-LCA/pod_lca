
# This script compares the GWP impacts adjusted for carbon storage from the Excel tool (given in aa CSV file) with the values calculated using the Python Framework.

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.impacts import ImpactsDatabase
from pod_lca.material_screening import Project
from pod_lca.units import KILOGRAM
from pod_lca.units import UNITS_MAP
from pod_lca.utilities import DataImporter

test_data = "tests\\carbon-storage_test_test-values.csv"
output_file = "tests\\carbon-storage_test_report.csv"
test_dict = DataImporter.csv_to_dict(test_data, 'test name')

project = Project()

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_data.csv')
project.set_database(custom_impact_database)

my_model = project.add_model("Test")

output_dict = {}
for test in tqdm(test_dict):
    qty = test_dict[test]['Qty']
    if isinstance(qty, str):
        qty = float(qty.replace(',', ''))

    product = my_model.add_product(name=test, 
                                   stage="A1", 
                                   qty=qty, 
                                   unit=UNITS_MAP[test_dict[test]['Unit']], 
                                   impacts_from=test_dict[test]['Material'])
    
    if test_dict[test]['set_mineral_carbon'] == "YES":
        product.get_carbon_storage().set_mineral_carbon(qty=float(test_dict[test]['mineral_C_Qty']), 
                                                        unit=UNITS_MAP[test_dict[test]['mineral_C_Unit']])

    output_dict[test] = { 'test name':test,
                          'Qty': qty, 
                          'Unit': test_dict[test]['Unit'],
                          'set_mineral_carbon': test_dict[test]['set_mineral_carbon'],
                          'mineral_C_Qty': test_dict[test]['mineral_C_Qty'],
                          'mineral_C_Unit': test_dict[test]['mineral_C_Unit']
                          }
                                               
    GWP_Python = product.get_impacts().get_record('GWP')
    GWP_Excel_tool = float(test_dict[test]['GWP'])
    dif_GWP = 2 * abs(GWP_Python - GWP_Excel_tool) / abs(GWP_Python + GWP_Excel_tool)
    
    output_dict[test]['GWP_Python tool'] = GWP_Python
    output_dict[test]['GWP_Excel tool'] = GWP_Excel_tool
    output_dict[test]['GWP_difference (%)'] = dif_GWP * 100

    GWP_adjusted_Python = product.get_impacts().get_adjusted_GWP()
    GWP_adjusted_Excel_tool = float(test_dict[test]['GWP_adjusted'])
    dif_adjusted_GWP = 2 * abs(GWP_adjusted_Python - GWP_adjusted_Excel_tool) / abs(GWP_adjusted_Python + GWP_adjusted_Excel_tool)
    
    output_dict[test]['GWP_adjusted_Python tool'] = GWP_adjusted_Python
    output_dict[test]['GWP_adjusted_Excel tool'] = GWP_adjusted_Excel_tool
    output_dict[test]['GWP_adjusted_difference (%)'] = dif_adjusted_GWP * 100 

    if (dif_GWP * 100 < 0.5) and (dif_adjusted_GWP * 100 < 0.5):
        test_status = True
    else:
        test_status = False
        print(f"{test} failed")

    output_dict[test]['test status'] = 'PASS' if test_status else 'FAIL'

DataImporter.dict_to_csv(output_dict, output_file)
