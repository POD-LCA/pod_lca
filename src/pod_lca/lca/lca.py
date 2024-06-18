from __future__ import print_function

import os
import json

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import pod_lca

from pod_lca.traci import read_traci_categories
from pod_lca.traci import read_traci_impacts



class LCA(object):
    def __init__(self):
        self.graph              = {}
        self.promap             = None
        self.ecoinvent_path     = None
        self.traci_path         = None
        self.traci              = None

    def read_ecoinvent_maps(self):
        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format('processes')), 'r') as fp:
            self.promap = json.load(fp)

    def run_ecoinvent_process(self, process_name):
        file = self.promap[process_name] + '.json'
        fp = os.path.join(self.ecoinvent_path, 'processes', file)
        with open(fp, 'r') as fp:
            process = json.load(fp)
        exchanges = process['exchanges']
        
        graph = {}
        for exchange in exchanges:
            amount = exchange['amount']
            eid = exchange['internalId']
            flow = exchange['flow']
            flow_id = flow['@id']
            flow_name = flow['name']
            flow_type = flow['flowType']
            graph[eid] = {'flow_type':flow_type,
                          'flow_id': flow_id,
                          'flow_type': flow_type,
                          'flow_name': flow_name,
                          'amount': amount,
            }
        # print(exchange.keys())
        self.graph[process_name] = graph

    def read_traci_impacts(self):
        mpath = os.path.join(self.traci_path, 'lcia_methods')
        cpath = os.path.join(self.traci_path, 'lcia_categories')
        filename = os.listdir(mpath)[0]
        impact_categories = read_traci_categories(os.path.join(mpath, filename))
        self.traci = read_traci_impacts(cpath, impact_categories)

    def compute_elementary_flow_impacts(self, process_name):
        for k in lca.graph[process_name]:
            fn = lca.graph[process_name][k]['flow_name']
            ft  = lca.graph[process_name][k]['flow_type']
            fid = lca.graph[process_name][k]['flow_id']
            # print(ft)
            for impact_cat_k in lca.traci:
                if ft == 'ELEMENTARY_FLOW':
                    # print(fn)
                    if fid in lca.traci[impact_cat_k]:
                        impact = lca.traci[impact_cat_k][fid]
                    else:
                        impact = 0
                    print(impact_cat_k)
                    print(fn, impact)
                    print('')

if __name__ == '__main__':
    
    for i in range(50): print('')

    lca = LCA()
    lca.ecoinvent_path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    # lca.traci_path = os.path.join(pod_lca.TEMP, 'TRACI_2.1_json_v1.0.0')
    lca.read_ecoinvent_maps()
    # lca.read_ecoinvent_lcia()

    process_name = 'cement production, Portland | cement, Portland | EN15804, U'
    lca.run_ecoinvent_process(process_name)
    



    # lca.read_traci_impacts()  #TODO: THIS NEEDS TO BE REPLACED WITH A ECOINVENT METHODS, METHOD
    # lca.compute_elementary_flow_impacts(process_name)
    # print(type(lca.traci['Global warming']))

