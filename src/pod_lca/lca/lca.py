from __future__ import print_function

import os
import json

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import pod_lca



class LCA(object):
    def __init__(self):
        self.graph                  = {}
        self.process_map            = None
        self.lcia_map               = None
        self.ecoinvent_path         = None
        self.ecoinvent_lcia_path    = None
        self.ecoinvent_lcia         = {}

    def read_ecoinvent_maps(self):
        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format('processes')), 'r') as fp:
            self.process_map = json.load(fp)

    def recursion(self, process_name):
        uuids = self.process_map[process_name]
        print(uuids)
        for uuid in uuids:
            fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid))
            with open(fp, 'r') as fp:
                process = json.load(fp)
            if process['location']['name'] == 'United States':
                break
        print('')
        exchanges = process['exchanges']
        print(len(exchanges))
        # for exchange in exchanges[:1]:
        #     print(exchange.keys())
        #     print(exchange['flow']['name'], exchange['flow']['@id'])

        #     print(exchange.keys())
        #     print('')
        #     flow = exchange['flow']
        #     print(flow)
        #     print('')
        #     file = flow['@id'] + '.json'
        #     fp = os.path.join(self.ecoinvent_path, 'flows', file)
        #     with open(fp, 'r') as fp:
        #         flow2 = json.load(fp)
        #     print(flow2)
        #     break
        #     # exchanges2 = process['exchanges']
        #     # print(len(exchanges2))

    def run_ecoinvent_process(self, process_name):
        #TODO: This function should run the entire network.
        #TODO: Try recursion or memoization
        
        
        file = self.process_map[process_name] + '.json'
        fp = os.path.join(self.ecoinvent_path, 'processes', file)
        with open(fp, 'r') as fp:
            process = json.load(fp)
        exchanges = process['exchanges']
        graph = {}
        for i, exchange in enumerate(exchanges):
            amount = exchange['amount']
            # eid = exchange['internalId']
            flow = exchange['flow']
            flow_id = flow['@id']
            flow_name = flow['name']
            flow_type = flow['flowType']
            ekey = '{}-{}'.format(i, flow_name)
            graph[ekey] = {'flow_type':flow_type,
                           'flow_id': flow_id,
                           'flow_type': flow_type,
                           'flow_name': flow_name,
                           'amount': amount}
        self.graph[process_name] = graph

    def read_ecoinvent_lcia(self):
        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_lcia_categories_map.json'), 'r') as fp:
            self.lcia_map = json.load(fp)
        
        for key in self.lcia_map:
            filepath = os.path.join(self.ecoinvent_lcia_path,'lcia_categories', '{}.json'.format(self.lcia_map[key]))
            with open(filepath, 'r') as fp:
                ic = json.load(fp)
            self.ecoinvent_lcia[key] = {}
            for i in range(len(ic['impactFactors'])):
                id_ = ic['impactFactors'][i]['flow']['@id']
                self.ecoinvent_lcia[key][id_] = ic['impactFactors'][i]

    def compute_elementary_flow_impacts(self, process_name):
        #TODO: This will have to be redone after the final graph structure is set. 
        for k in lca.graph[process_name]:
            fn = lca.graph[process_name][k]['flow_name']
            ft  = lca.graph[process_name][k]['flow_type']
            fid = lca.graph[process_name][k]['flow_id']
            # print(ft)
            for impact_cat_k in lca.ecoinvent_lcia:
                if ft == 'ELEMENTARY_FLOW':
                    if fid in lca.ecoinvent_lcia[impact_cat_k]:
                        impact = lca.ecoinvent_lcia[impact_cat_k][fid]['value']
                    else:
                        impact = 0

                    # if impact != 0 and impact_cat_k == 'climate change - global warming potential (GWP100)':
                    #     print(fid)
                    #     print(impact_cat_k)
                    #     print(fn, impact)
                    #     print('')

    def plot_graph(self):
        import networkx as nx
        from pyvis.network import Network
        nt = Network('1000px', '1700px')

        G = nx.from_dict_of_dicts(self.graph)
        nt.from_nx(G)
        nt.show('nx.html')
        nx.draw(G)
        # print(G.edges)

if __name__ == '__main__':

    # TODO: FIX THE PROCESS MAP TO HAVE ALL VERSIONS OF EACH PROCESS!!!

    for i in range(50): print('')

    lca = LCA()
    lca.ecoinvent_path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    lca.ecoinvent_lcia_path = os.path.join(pod_lca.TEMP, 'ecoinvent_3_9_1_LCIA_Methods_openLCA_2_(1)')
    lca.read_ecoinvent_maps()
    lca.read_ecoinvent_lcia()

    # ok = '0795345f-c7ae-410c-ad25-1845784c75f5'

    # ic = 'climate change - global warming potential (GWP100)'
    # # print(lca.ecoinvent_lcia[ic]['impactFactors'][0])
    # # print(len(lca.ecoinvent_lcia[ic]['impactFactors']))
    # ic_map = {}
    # for i in range(len(lca.ecoinvent_lcia[ic]['impactFactors'])):
    #     id_ = lca.ecoinvent_lcia[ic]['impactFactors'][i]['flow']['@id']
    #     ic_map[id_] = i

    # print(ic_map[ok])



    process_name = 'cement production, Portland | cement, Portland | EN15804, U'
    # process_name = 'clinker production | clinker | EN15804, U'
    # process_name = 'market for tap water | tap water | EN15804, U'
    # process_name = 'sand quarry operation, extraction from river bed | sand | EN15804, U'
    # process_name = 'gravel production, crushed | gravel, crushed | EN15804, U'
    # lca.run_ecoinvent_process(process_name)
    lca.recursion(process_name)
    # lca.compute_elementary_flow_impacts(process_name)

    # lca.plot_graph()