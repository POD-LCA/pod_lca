
from utilities.data_imports.data_importer import Data_Importer
from lca_modules.impacts.olca_data import openLCA
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
my_process_list = process_list_all[0:15]

# To evaluate a single process, copy uuid here
'''
my_process_list = []
my_process_ref = openLCA_client.get_descriptor(schema.Process, 'dae534d8-59de-45ad-9a47-1bd8d57538a5')
my_process_list.append(my_process_ref)
'''

#To evaluate a list of processes (list of uuids), copy list here
'''
my_process_list = []
my_uuid_list = ['7ad46f7a-6a93-46f0-9ca6-0c1b00bbd8cd','987ea0b0-8d72-459e-abc0-e10755375aeb','0e3bb10c-d971-41d3-84b0-3ac22fd69248','716b1db6-0d25-405f-99cf-35bc59422ccb','19518043-6a18-4200-bfc9-12799915d19a','c8ca8ff6-3b47-4e22-b533-4a066e84190b','30fe1dc5-81d5-424d-be6e-ba69fd245755','f1304342-7d93-4c8a-a54f-26fd23d45d70','48645326-0af2-4e47-a31b-4bc75d845ee2','f114ed11-fba1-4433-b92e-484fdc20ad74','6ab8360e-d09f-4e7f-be1f-155e15dbf17e','33c82cb9-2c1d-4302-9619-a32d99d30943','d1b276b6-52ab-40e8-87bc-4b03fa60526f','82fbb8a6-bdc3-484d-ba2a-7e26ed5aac3f','9332d568-52b7-4d9e-8311-7e237178e647','ce08b48e-4631-4f56-ac56-be1b4065c4e3','f566901a-a6cf-4ea5-a720-186be199e0ae','44849464-c55a-4699-9f6c-ce8047f24ec3','bfac5c76-3c33-400e-9ef1-034e47045c6c','fbd47f8c-f1f2-4866-bc22-0918ced9c648','d7028a74-7a89-4155-866e-0221c6eef2e0','646dd25e-c460-43c2-88f7-aaada4bee88d','b629771f-13bd-44f5-82aa-4a4af9a96c03','6fe7b1d5-1fb3-4296-aaec-da2c60e01938','73b75743-cb13-4cbd-adc6-1d9d7298e545','a5587d4a-5224-45d5-9890-5606706c1eda','7ac1d6a5-bc47-4346-a06a-df4ac27c7e43','85cb5190-97b9-42d6-a81a-5ee7e37533e7','8510b76d-3310-448b-8460-bcac238887b2','f7818ecd-d0d6-4f3d-8ce7-b96992159e5b','66c22647-9ed9-4e28-a0fb-6a85679d8781','93f539d3-0bd5-4a6b-9c46-a644aea6a4d8','aed5af60-86bb-47ba-8ad3-d1c5f355c208','1b9a9429-2755-4522-82c6-cc57f657c2be','44d06ceb-438e-4fde-a11c-4ffb89c2c39a','6f3f42f9-8d20-4dcb-91da-5bb9423b5cd6','989be583-94df-48b9-9560-4c608d120779','325ce67a-25c6-446a-8137-1c9b51f118f7','ba4e3baa-e110-4e6e-aa1c-6bbe29c810a5','243fed2c-e980-4f42-abf8-e378be6727af','8bc0a151-546a-4389-ad5c-97345b4e81e8','8440a12c-7fed-41a9-a6c3-74c562c40802','fd44641e-206a-4551-bb21-e24509aef8e8','55834172-c998-402d-9681-275c95541f68','acf3df8d-7890-4f91-a7d4-0a377d1164c6','98840d85-9491-4fc2-a3c2-afc23eef4981','331ea13a-3836-484b-a9e8-a3c30e8089f3','9ee33967-2341-4665-be31-3068547213f8','3df5c8d3-94ac-41b5-bad5-d0b845610abe','f24e88a0-f54e-40f3-bb91-36c40a7b36be','1727d2e6-9322-4ba9-ba59-d2c3b5bc7b59','6073fd6f-cb0b-4a4d-929d-e8a76cb724eb','78440773-83ac-4937-919b-94fe1dbf6c6e','7ab0e5c1-e6a0-4b39-8c30-d999e406941f','5e3ef887-191c-46e3-a871-98d54443a631','3152e3c6-321b-4c53-a0fd-51d7fb291dd5','e686c63a-443f-4653-8163-c0323352b55a','64354ee1-1c90-4596-b6cc-4c7afc814d96'] # copy list of uuids here
for uuid in my_uuid_list:
    my_process_ref = openLCA_client.get_descriptor(schema.Process, uuid)
    my_process_list.append(my_process_ref)
'''

# filter my_process_list by one or more category numbers (FLCAC: NAICS classification; ecoinvent: ISIC classification)
# filter_by = None
filter_by = 22
# filter_by = '8292:Packaging'
process_list_filtered = openLCA.filter_processes_by(process_list_all, filter_by)
# filter_by = ['8292:Packaging']
# if not filter_by is None:
#     if isinstance(filter_by, int):
#         filter_by = [filter_by]    
#     my_process_list = [process for process in my_process_list if any(str(filter) in process.category for filter in filter_by)]

impact_categories = Data_Importer.json_to_dict('./data/impact_categories.json')
inventories = Data_Importer.json_to_dict('./data/inventories.json')
impact_method_uuid = '68c8e8cd-e64a-49b1-954e-bec0da4e4574'

# different options for grouping
# group_by = [{'name':'Electricity','ids': 2211}, 
#             {'name':'Waste', 'ids': [5621, 5622,5629]}]
# group_by = {'name':'fuel combustion', 'ids':['6c96a609-cd7e-3f19-a151-27deb823d3e4' , '5198d618-7bc8-3639-b4a1-de71d6d5f49a']}
renewable_fuels_process_list = Data_Importer.csv_to_list('./data/FLCAC_renewable_fuels.csv', header_name='UUID')
nonrenewable_fuels_process_list = Data_Importer.csv_to_list('./data/FLCAC_nonrenewable_fuels.csv', column_index=1)
heating_values = Data_Importer.csv_to_dict('./data/FLCAC_heating_values.csv', 'UUID')
group_by = [{'name':'electricity','ids':2211},
            {'name':'nonrenewable fuel combustion','ids':nonrenewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}, 
            {'name':'renewable fuel combustion', 'ids':renewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}]

results = openLCA.generate_impacts_dir(openLCA_client, my_process_list, impact_categories | inventories, impact_method_uuid, group_by)

save_path = './data/USLCI_Categorized_all.csv'
Data_Importer.dict_to_csv(results, save_path) 

# dict_A = Data_Importer.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv', 'UUID')
# dict_B = Data_Importer.csv_to_dict('./data/USLCI_Elec.csv', 'UUID')
# print(openLCA.compare_dicts(dict_A, dict_B))


# Run this line to fix last_internal_id of all processes in my_process_list (data validation)
# openLCA.fix_last_internal_ids(openLCA_client, my_process_list)
