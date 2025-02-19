from utilities.data.transfer import DataHandler
from utilities.data.olca import openLCA


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu"
__version__ = "0.1.0"

#To evaluate Federal LCA Commons (FLCAC) data, use the following impact_categories and inventories
impact_categories = DataHandler.json_to_dict('./data/impact_categories.json')
inventories = DataHandler.json_to_dict('./data/inventories.json')

#To evaluate ecoinvent data, use the following impact_categories and inventories
#impact_categories = DataHandler.json_to_dict('./data/impact_categories_ecoinvent.json')
#inventories = DataHandler.json_to_dict('./data/inventories_ecoinvent.json')

save_path = './data/USLCI_Elec.csv'
results = openLCA.generate_impacts_dir(impact_categories | inventories, seperate_elec=False)
DataHandler.dict_to_csv(results, save_path) 

#dict_A = DataHandler.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv', 'UUID')
#dict_B = DataHandler.csv_to_dict('./data/USLCI_Elec.csv', 'UUID')
#print(openLCA.compare_dicts(dict_A, dict_B))
