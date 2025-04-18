from utilities.data.transfer import DataHandler
from utilities.data.olca import openLCA
from utilities.units.common_units import JOULE
from utilities.units.metric_prefixes import MEGA

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

openLCA_client = openLCA.set_connection()

process_list_all = openLCA.get_process_list(openLCA_client)

impact_categories = DataHandler.json_to_dict('./data/impact_categories.json')
inventories = DataHandler.json_to_dict('./data/inventories.json')

impact_method_uuid = '68c8e8cd-e64a-49b1-954e-bec0da4e4574'

renewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_renewable_fuels.csv', 1)
nonrenewable_fuels_process_list = DataHandler.csv_to_list('./data/USLCI_nonrenewable_fuels.csv', 1)
heating_values = DataHandler.csv_to_dict('./data/USLCI_heating_values.csv', 'UUID')

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

save_path = './data/USLCI_Categorized_all.csv'
DataHandler.dict_to_csv(results, save_path) 
