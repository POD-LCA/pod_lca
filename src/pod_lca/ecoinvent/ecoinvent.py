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
    # folders = ['processes',
    #            'flows',
    #            'flow_properties',
    #            'flow_properties',]

    folders = ['processes']

    for folder in folders:
        path_ = os.path.join(path, folder)
        files = os.listdir(path_)
        # print(len(files))
        map = {}
        for file in files:
            with open(os.path.join(path_, file), 'r') as fp:
                data = json.load(fp)
            # print(data.keys())
            name = data['name']
            location = data['location']['name']
            # print(location)
            if name in map:
                map[name]['uuids'].append(os.path.splitext(file)[0])
                map[name]['locations'].append(location)
            else:
                map[name] = {}
                map[name]['uuids'] = [os.path.splitext(file)[0]]
                map[name]['locations'] = [location]
        
        #TODO: This way of picking the best process based on location is not great!!!!
        for key in map:
            if len(map[key]['uuids']) > 1:
                locations = map[key]['locations']
                if 'United States' in locations:
                    i = locations.index('United States')
                elif 'Global' in locations:
                    i = locations.index('Global')
                elif 'Rest-of-World' in locations:
                    i = locations.index('Rest-of-World')
                else:
                    i = 0
                map[key] = map[key]['uuids'][i]
            else:
                map[key] = map[key]['uuids'][0]

        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format(folder)), 'w') as f:
            json.dump(map, f)

def create_ecoinvent_maps_lcia_maps(path):
    path = os.path.join(path, 'lcia_categories')
    files = os.listdir(path)
    cmap = {}
    for file in files:
        filepath = os.path.join(path, file)
        if file.endswith('json'):
            with open(filepath, 'r') as fp:
                lcia = json.load(fp)
            category = lcia['name']
            id_ = lcia['@id']
            cmap[category] = id_

    with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_lcia_categories_map.json'), 'w') as f:
        json.dump(cmap, f)
    return cmap

if __name__ == '__main__':

    # TODO: How does TRACI relate to Ecoinvent? Does it?

    for i in range(50): print('')

    # LCIA ---------------------------------------------------------------------

    # path = os.path.join(pod_lca.TEMP, 'ecoinvent_3_9_1_LCIA_Methods_openLCA_2_(1)')
    # category_dict = create_ecoinvent_maps_lcia_maps(path)
    # for k in category_dict:
    #     print(k)
    #     print(category_dict[k])
    #     print('')



    # # CREATE MAP ---------------------------------------------------------------

    path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    create_ecoinvent_maps(path)

    # # OPEN JSON FILES FROM MAPS ------------------------------------------------

    # map_name = 'processes'

    # with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format(map_name)), 'r') as fp:
    #     map_ = json.load(fp)

    # # key = list(map_.keys())[0]

    # key = 'cement production, Portland | cement, Portland | EN15804, U'
    # file = map_[key] + '.json'
    # fp = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629', map_name, file)
    # with open(fp, 'r') as fp:
    #     data = json.load(fp)

    # # for k in data:
    # #     print(k)
    # #     # print(k, data[k])
    # #     print('')

    # # open one dict inside JSON file - - - - 

    # key = 'exchanges'
    # flows = {}
    # for i in range(50, 2000):
    #     item = data[key][i]
    #     # for k in item:
    #     #     print(k)
    #     flow = item['flow']
    #     flow_id = flow['@id']
    #     flow_type = flow['flowType']
    #     if flow_type == 'ELEMENTARY_FLOW':
    #         break
    # print(i)
    # print(item['amount'])
    # print(flow)
    # for k in item:
    #     print(k)

    # #     fp = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629', 'flows', '{}.json'.format(flow_id))
    # #     with open(fp, 'r') as fp:
    # #         ex = json.load(fp)
    # #     for k in ex:
    # #         print(k)


