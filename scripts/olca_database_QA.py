from utilities.data.olca import openLCA
import olca_schema as schema

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
'''
my_uuid_list = ['6e687c52-4256-374e-b56f-6520c390a00e', '10499ec7-eb9b-3e1a-80ac-3dd3dcfa3830']
my_process_list = []
for uuid in my_uuid_list:
    process_ref = openLCA_client.get_descriptor(schema.Process, uuid)
    my_process_list.append(process_ref)
'''


#Fix last_internal_id of all processes in my_process_list
openLCA.fix_last_internal_ids(openLCA_client, my_process_list)