from utilities.data.transfer import DataHandler
from utilities.data.olca import openLCA
from utilities.units.common_units import JOULE, KILOGRAM
from utilities.units.metric_prefixes import MEGA


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"


openLCA_client = openLCA.set_connection()
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/elci_6_2024 for uslci_q2_2024_final.zip', duplicates='update')
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/National_Renewable_Energy_Laboratory-USLCI_Database_Public.zip', duplicates='update')
# openLCA.import_from_zip(openLCA_client, r'C:/Users/kiun/ISO21930-LCIA-US (POD_LCA).zip', duplicates='update')

process_list_all = openLCA.get_process_list(openLCA_client)

# different options for process list
# my_process_list = process_list_all
my_process_list = process_list_all[606:610]
# my_process_list = ['f41111d1-1668-325a-abd2-a40af161e35d', 'd4031d82-ca6e-3548-b07c-2acd79f47a3f']

impact_categories = DataHandler.json_to_dict('./data/impact_categories.json')
inventories = DataHandler.json_to_dict('./data/inventories.json')

impact_method_uuid = '68c8e8cd-e64a-49b1-954e-bec0da4e4574'

# different options for grouping
# group_by = [{'name':'Electricity','ids': 2211}, 
#             {'name':'Waste', 'ids': [5621, 5622,5629]}]
# group_by = {'name':'fuel combustion', 'ids':['6c96a609-cd7e-3f19-a151-27deb823d3e4' , '5198d618-7bc8-3639-b4a1-de71d6d5f49a']}
renewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_renewable_fuels.csv', 1)
nonrenewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_nonrenewable_fuels.csv', 1)
heating_values = DataHandler.csv_to_dict('./data/USLCI_heating_values.csv', 'UUID')
group_by = [{'name':'electricity','ids':2211},
            {'name':'nonrenewable fuel combustion','ids':nonrenewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}, 
            {'name':'renewable fuel combustion', 'ids':renewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}]

results = openLCA.generate_impacts_dir(openLCA_client, my_process_list, impact_categories | inventories, impact_method_uuid, group_by)

save_path = './data/USLCI_Categorized_all.csv'
DataHandler.dict_to_csv(results, save_path) 

# dict_A = DataHandler.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv', 'UUID')
# dict_B = DataHandler.csv_to_dict('./data/USLCI_Elec.csv', 'UUID')
# print(openLCA.compare_dicts(dict_A, dict_B))
