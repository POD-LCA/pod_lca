
from lca_modules.impacts.olca_data import openLCA
from utilities.data_imports.data_importer import Data_Importer
from utilities.units.common_units import JOULE
from utilities.units.metric_prefixes import MEGA

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

# ================================================
# INSTRUCTIONS
# ================================================
# The following steps shall be followed to create the connection between POD|LCA Python framework and the OpenLCA application. 

# 1. Open the OpenLCA application
# 2. Import the database into OpenLCA. The following is the procedure to import source data from a zip file (for importing a database from zolca files or other means, refer to the OpenLCA manual).
#    It is also necessary to import and customize the desired LCIA impact evaluation methods to the database
#       2a. Database > New Database > From scratch
#       2b. In the pop-up enter the database name and set ‘Database content’ as ‘Complete reference units’
#       2c. On the navigation panel, select and right-click on the database created and select import > Other…
#       2d. Select ‘Linked Data (JSON-LD)’ and follow the instructions to import the *.zip file. Select ‘update data sets with newer versions’
# 3. Start up the Inter-Process Communication (IPC) server.
#    The database intended for impact evaluation must be open before starting the IPC server.
#       3a. Tools > Developer Tools > IPC Server 
#       3b. Set Port to 8080 
#       3c. Click the green arrow
# 4. Run this script

openLCA_client = openLCA.set_connection()

process_list_all = openLCA.get_process_list(openLCA_client)
filter_by = ['01', '02', '13', '16', '17', '19', '20', '22', '23', '24', '25', '27', '35', '36', '38', 'F', 'H', '8292']
process_list = openLCA.filter_processes_by(process_list_all, filter_by)

impact_categories = Data_Importer.json_to_dict('./data/impacts_ecoinvent391_categories.json')
emission_inventories = Data_Importer.json_to_dict('./data/impacts_ecoinvent391_emission-inventories.json')

impact_method_uuid = '5d5b2a0c-0a99-48d4-93e9-2f2b9d852655'

electricity_process_list = Data_Importer.csv_to_list('./data/impacts_ecoinvent391_electricity-group.csv', column_header='UUID')
renewable_fuels_process_list = Data_Importer.csv_to_list('./data/impacts_ecoinvent391_renewable-fuels-group.csv', column_header='UUID')
nonrenewable_fuels_process_list = Data_Importer.csv_to_list('./data/impacts_ecoinvent391_nonrenewable-fuels-group.csv', column_header='UUID')
heating_values = Data_Importer.csv_to_dict('./data/impacts_ecoinvent391_heating-values.csv', 'UUID')
group_by = [{'name':'electricity','ids': electricity_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values},
            {'name':'nonrenewable fuel combustion','ids':nonrenewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}, 
            {'name':'renewable fuel combustion', 'ids':renewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}]


results = openLCA.generate_impacts_dir( openLCA_client, process_list, 
                                        impact_categories | emission_inventories, 
                                        impact_method_uuid, 
                                        group_by)

# Note: When using ecoinvent391, renewable fuel group contributions need to be recalculated for all processes that use wood chips as a raw material (instead of fuel). 
# wood chips: (uuids: d47a4435-3089-4263-af99-8611eed2698c, 7fe99768-d571-4bc2-a272-7df585bd0d48) 
uuid_list_with_wood_chips = Data_Importer.csv_to_list('./data/impacts_ecoinvent391_uuid-list-with-wood-chips.csv', column_header='UUID')
process_list = openLCA.get_process_list(openLCA_client, uuid_list_with_wood_chips)

renewable_fuels_process_list = Data_Importer.csv_to_list('./data/impacts_ecoinvent391_renewable-fuels-group-no-wood-chips.csv', column_header='UUID')

group_by = [{'name':'renewable fuel combustion', 'ids':renewable_fuels_process_list, 'unit': MEGA * JOULE, 'conversion_map':heating_values}]

results_with_wood_chips = openLCA.generate_impacts_dir( openLCA_client, process_list, 
                                                        impact_categories | emission_inventories, 
                                                        impact_method_uuid, 
                                                        group_by)

for uuid in results_with_wood_chips:
    if uuid in results:
        for inventory in impact_categories | emission_inventories:
            results[uuid]['renewable fuel combustion_'+ inventory] = results_with_wood_chips[uuid]['renewable fuel combustion_'+ inventory]

# save results
save_path = './data/impacts_ecoinvent391_categorized-data.csv'
Data_Importer.dict_to_csv(results, save_path)
