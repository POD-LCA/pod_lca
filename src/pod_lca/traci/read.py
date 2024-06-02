from __future__ import print_function

import os
import json
import pod_lca

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


def read_traci_categories():
    path = os.path.join(pod_lca.TEMP, 'TRACI_2.1_json_v1.0.0', 'lcia_methods')
    file = 'ed2353f9-9db5-32b0-b6a8-7bf29f6f46c8.json'
    filepath = os.path.join(path, file)
    with open(filepath, 'r') as fp:
        traci = json.load(fp)

    ics = traci['impactCategories']
    category_dict = {}
    for ic in ics:
        name = ic['name']
        id = ic['@id']
        unit = ic['refUnit']
        category_dict[name] = {'id': id, 'unit': unit}

    return category_dict

def lookup_impact(category, id, category_dict):
    path = os.path.join(pod_lca.TEMP, 'TRACI_2.1_json_v1.0.0', 'lcia_categories')
    file = '{}.json'.format(category_dict[category]['id'])
    filepath = os.path.join(path, file)
    
    with open(filepath, 'r') as fp:
        traci = json.load(fp)
    # print(traci.keys())
    ifacts = traci['impactFactors']
    print(len(ifacts))

    i = 177
    for k in ifacts[i]:
        print(k)
        print(ifacts[i][k])
        print('')
        



if __name__ == '__main__':

    # TODO: How dies TRACI relate to Ecoinvent? Does it?

    for i in range(50): print('')

    category_dict = read_traci_categories()


    category = 'Global warming'
    # category = 'Smog formation'
    lookup_impact(category, id, category_dict)