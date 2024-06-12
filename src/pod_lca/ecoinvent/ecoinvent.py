from __future__ import print_function

import os
import json
import pod_lca

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

def create_ecoinvent_maps(path):
    folders = ['processes',
               'flows',
               'flow_properties',
               'flow_properties',
               'lcia_categories',
               'lcia_methods']

    for folder in folders:
        path_ = os.path.join(path, folder)
        files = os.listdir(path_)
        map = {}
        for file in files:
            with open(os.path.join(path_, file), 'r') as fp:
                data = json.load(fp)
            name = data['name']
            map[name] = os.path.splitext(file)[0]

        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format(folder)), 'w') as f:
            json.dump(map, f)



# def read_ecoinvent_lcia(path):
#     path = os.path.join(path, 'lcia_methods')
#     # file = 'ed2353f9-9db5-32b0-b6a8-7bf29f6f46c8.json'
#     files = files = os.listdir(path)
#     file = files[2]
#     filepath = os.path.join(path, file)
#     with open(filepath, 'r') as fp:
#         lcia = json.load(fp)

#     # ics = lcia['impactCategories']
#     # for ic in ics:
#     #     print(ic['name'])
#     #     print(ic)
#     #     print('')

#     ics = lcia['impactCategories']
#     category_dict = {}
#     for ic in ics:
#         name = ic['name']
#         id = ic['@id']
#         unit = ic['refUnit']
#         category_dict[name] = {'id': id, 'unit': unit}

#     return category_dict

if __name__ == '__main__':

    # TODO: How does TRACI relate to Ecoinvent? Does it?

    for i in range(50): print('')

    # LCIA ---------------------------------------------------------------------

    # path = os.path.join(pod_lca.TEMP, 'ecoinvent_3_9_1_LCIA_Methods_openLCA_2 (1)')
    # category_dict = read_ecoinvent_lcia(path)
    # print(category_dict)


    # CREATE MAP ---------------------------------------------------------------

    # path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    # create_ecoinvent_maps(path)

    # OPEN JSON FILES FROM MAPS ------------------------------------------------

    map_name = 'processes'

    with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format(map_name)), 'r') as fp:
        map_ = json.load(fp)

    # key = list(map_.keys())[0]

    key = 'cement production, Portland | cement, Portland | EN15804, U'
    file = map_[key] + '.json'
    fp = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629', map_name, file)
    with open(fp, 'r') as fp:
        data = json.load(fp)

    # for k in data:
    #     print(k)
    #     # print(k, data[k])
    #     print('')

    # open one dict inside JSON file - - - - 

    key = 'exchanges'
    flows = {}
    for i in range(50, 2000):
        item = data[key][i]
        # for k in item:
        #     print(k)
        flow = item['flow']
        flow_id = flow['@id']
        flow_type = flow['flowType']
        if flow_type == 'ELEMENTARY_FLOW':
            break
    print(i)
    print(item['amount'])
    print(flow)
    for k in item:
        print(k)

    #     fp = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629', 'flows', '{}.json'.format(flow_id))
    #     with open(fp, 'r') as fp:
    #         ex = json.load(fp)
    #     for k in ex:
    #         print(k)


