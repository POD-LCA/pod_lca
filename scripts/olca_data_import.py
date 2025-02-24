from utilities.data.transfer import DataHandler
from utilities.data.olca import openLCA
from utilities.units.common_units import JOULE, KILOGRAM
from utilities.units.metric_prefixes import MEGA


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu"
__version__ = "0.1.0"


openLCA_client = openLCA.set_connection()

process_list_all = openLCA.get_process_list(openLCA_client)

# different options for process list
my_process_list = process_list_all
# my_process_list = process_list_all[125:135]
# my_process_list = ['f41111d1-1668-325a-abd2-a40af161e35d', 'd4031d82-ca6e-3548-b07c-2acd79f47a3f']

impact_categories = DataHandler.json_to_dict('./data/impact_categories.json')
inventories = DataHandler.json_to_dict('./data/inventories.json')

# different options for grouping
group_by = {'Electricity': '2211', 'Waste': [5621, 5622,5629]}
# group_by = {'fuel combustion':['6c96a609-cd7e-3f19-a151-27deb823d3e4' , '5198d618-7bc8-3639-b4a1-de71d6d5f49a']}

results = openLCA.generate_impacts_dir(openLCA_client, my_process_list, impact_categories | inventories, group_by)

save_path = './data/USLCI_Categorized_uuid.csv'
DataHandler.dict_to_csv(results, save_path) 

# dict_A = DataHandler.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv', 'UUID')
# dict_B = DataHandler.csv_to_dict('./data/USLCI_Elec.csv', 'UUID')
# print(openLCA.compare_dicts(dict_A, dict_B))
