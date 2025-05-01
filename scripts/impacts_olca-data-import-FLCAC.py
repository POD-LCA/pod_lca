from utilities.data_imports.data_importer import Data_Importer
from lca_modules.impacts.olca_data import openLCA
from utilities.units.common_units import JOULE
from utilities.units.metric_prefixes import MEGA

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

openLCA_client = openLCA.set_connection()

process_list_all = openLCA.get_process_list(openLCA_client)[0:10]

impact_categories = Data_Importer.json_to_dict('./data/impact_categories.json')
inventories = Data_Importer.json_to_dict('./data/inventories.json')

impact_method_uuid = '0ed73bce-2198-4148-8c4d-8b2ce68b6e1a'

renewable_fuels_process_list = Data_Importer.csv_to_list('./data/FLCAC_renewable_fuels.csv', column_header='UUID')
nonrenewable_fuels_process_list = Data_Importer.csv_to_list('./data/FLCAC_nonrenewable_fuels.csv', column_header='UUID')
heating_values = Data_Importer.csv_to_dict('./data/FLCAC_heating_values.csv', 'UUID')

group_by = [{
                'name':'electricity',
                'ids':2211
                },
            {
                'name':'nonrenewable fuel combustion',
                'ids':nonrenewable_fuels_process_list, 
                'unit': MEGA * JOULE,
                'conversion_map':heating_values
                }, 
            {
                'name':'renewable fuel combustion',
                'ids':renewable_fuels_process_list,
                'unit': MEGA * JOULE,
                'conversion_map':heating_values
                }]

results = openLCA.generate_impacts_dir( openLCA_client, process_list_all, 
                                        impact_categories | inventories, 
                                        impact_method_uuid, 
                                        group_by)

save_path = './data/FLCAC_Categorized_all-TEST-TMP.csv'
Data_Importer.dict_to_csv(results, save_path) 
