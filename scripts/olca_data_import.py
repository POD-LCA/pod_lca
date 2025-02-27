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
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/National_Renewable_Energy_Laboratory-USLCI_Database_Public.zip')
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/ISO21930-LCIA-US (POD_LCA).zip')
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/elci_6_2024 for uslci_q2_2024_final.zip')

process_list_all = openLCA.get_process_list(openLCA_client)

# different options for process list
my_process_list = process_list_all
# my_process_list = process_list_all[125:135]
# my_process_list = ['f41111d1-1668-325a-abd2-a40af161e35d', 'd4031d82-ca6e-3548-b07c-2acd79f47a3f']

# filter my_process_list by one or more category numbers (USLCI categories follow NAICS classification)
filter_by = [2213]
if not filter_by is None:
    if isinstance(filter_by, int):
        filter_by = [filter_by]    
    my_process_list = [process for process in my_process_list if any(str(filter) in process.category for filter in filter_by)]

#To evaluate Federal LCA Commons (FLCAC) data, use the following impact_categories and inventories
impact_categories = DataHandler.json_to_dict('./data/impact_categories.json')
inventories = DataHandler.json_to_dict('./data/inventories.json')

#To evaluate ecoinvent data, use the following impact_categories and inventories
#impact_categories = DataHandler.json_to_dict('./data/impact_categories_ecoinvent.json')
#inventories = DataHandler.json_to_dict('./data/inventories_ecoinvent.json')

impact_method_uuid = '68c8e8cd-e64a-49b1-954e-bec0da4e4574'

# different options for grouping
# group_by = {'Electricity': 2211, 'Waste': [5621, 5622,5629]}
# group_by = {'fuel combustion':['6c96a609-cd7e-3f19-a151-27deb823d3e4' , '5198d618-7bc8-3639-b4a1-de71d6d5f49a']}
renewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_renewable_fuels.csv', 1)
nonrenewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_nonrenewable_fuels.csv', 1)
group_by = {'electricity': 2211,'nonrenewable fuel combustion': nonrenewable_fuels_process_list, 'renewable fuel combustion':renewable_fuels_process_list}

#If conversion of fuel groups to units of energy is required, specify the csv file of heating values
heating_values = DataHandler.csv_to_dict('./data/USLCI_heating_values.csv', 'UUID')

results = openLCA.generate_impacts_dir(openLCA_client, my_process_list, impact_categories | inventories, impact_method_uuid, group_by, heating_values)

save_path = './data/USLCI_Categorized_uuid.csv'
DataHandler.dict_to_csv(results, save_path) 

# dict_A = DataHandler.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv', 'UUID')
# dict_B = DataHandler.csv_to_dict('./data/USLCI_Elec.csv', 'UUID')
# print(openLCA.compare_dicts(dict_A, dict_B))
