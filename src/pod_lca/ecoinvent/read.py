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
    pro_path = os.path.join(path, 'processes')
    files = os.listdir(pro_path)
    pro_map = {}
    for file in files:
        with open(os.path.join(pro_path, file), 'r') as fp:
            data = json.load(fp)
        name = data['name']
        pro_map[name] = os.path.splitext(file)[0]

    with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_processes_map.json'), 'w') as f:
        json.dump(pro_map, f)

    return pro_map

if __name__ == '__main__':

    # TODO: How dies TRACI relate to Ecoinvent? Does it?

    for i in range(50): print('')

    # path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    # pro_map = create_ecoinvent_maps(path)

    with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_processes_map.json'), 'r') as fp:
        pro_map = json.load(fp)

    pro1 = 'cement production, Portland | cement, Portland | EN15804, U'
    pro2 = 'gravel production, crushed | gravel, crushed | EN15804, U'

    file = pro_map[pro1] + '.json'
    fp = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629', 'processes', file)
    with open(fp, 'r') as fp:
        data = json.load(fp)

    for k in data:
        print(k)
        print('')

    print(data['processDocumentation'])

    # for i in range(10):
    #     for k in data['exchanges'][i]:
    #         print(k, data['exchanges'][i][k])
    #         print('')
    #     print('')
    #     print('')
    #     print('')
    