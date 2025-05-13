
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.impacts.olca_data import openLCA
from pod_lca.utilities import DataImporter
from pod_lca.units import JOULE
from pod_lca.units import MEGA

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

impact_categories = DataImporter.json_to_dict('./data/impacts_flcac_categories.json')
inventories = DataImporter.json_to_dict('./data/impacts_flcac_emission-inventories.json')

impact_method_uuid = '0ed73bce-2198-4148-8c4d-8b2ce68b6e1a'

renewable_fuels_process_list = DataImporter.csv_to_list('./data/impacts_flcac_renewable-fuels-group.csv', column_header='UUID')
nonrenewable_fuels_process_list = DataImporter.csv_to_list('./data/impacts_flcac_nonrenewable-fuels-group.csv', column_header='UUID')
heating_values = DataImporter.csv_to_dict('./data/impacts_flcac_heating-values.csv', 'UUID')

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

save_path = './data/impacts_flcac_categorized-data.csv'
DataImporter.dict_to_csv(results, save_path) 
