from __future__ import print_function

import os
import json
import networkx as nx
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import pod_lca
from pod_lca.utilities import lbs_to_kgs




class LCA(object):
    def __init__(self):
        self.graph                  = {}
        self.outputs                = {}
        self.network                = nx.Graph()
        self.process_map            = None
        self.lcia_map               = None
        self.ecoinvent_path         = None
        self.ecoinvent_lcia_path    = None
        self.ecoinvent_lcia         = {}
        self.environmental_impacts  = {}

    def read_ecoinvent_maps(self):
        with open(os.path.join(pod_lca.DATA, 'maps', 'ecoinvent_{}_map.json'.format('processes')), 'r') as fp:
            self.process_map = json.load(fp)

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

    def plot_graph(self):

        from pyvis.network import Network
        nt = Network('1000px', '1700px', notebook=False)

        G = self.network
        nt.from_nx(G)
        nt.show('nx.html')
        # nx.draw(G)
        # print(G.edges)

    def run_ecoinvent_recursive(self, uuid, seen):
        fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid))
        with open(fp, 'r') as fp:
            process = json.load(fp)
        self.network.add_node(uuid)
        seen.append(uuid)
        exchanges = process['exchanges']
        for exchange in exchanges:
            is_input = exchange['isInput']
            is_not_elementary = exchange['flow']['flowType'] != 'ELEMENTARY_FLOW'
            if is_input: 
                if is_not_elementary:
                    uuid2 = exchange['defaultProvider']['@id']
                    if uuid2 not in seen:
                        self.network.add_node(uuid2)
                        self.network.add_edge(uuid, uuid2)
                        return self.run_ecoinvent_recursive(uuid2, seen)
                    else:
                        self.network.add_node(uuid2)
                        self.network.add_edge(uuid, uuid2)
                else:
                    uuid2 = exchange['flow']['@id']
                    self.network.add_node(uuid2, color='red')
                    self.network.add_edge(uuid, uuid2)
            else:
                continue

    def run_ecoinvent_while(self, uuid):
        fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid))
        with open(fp, 'r') as fp:
            process = json.load(fp)

        ex_map = {ex['flow']['@id']: ex for ex in process['exchanges']}
        q = [ex['flow']['@id'] for ex in process['exchanges']]
        seen = []

        while q:
            exid = q.pop(0)
            if exit not in seen:
                exchange = ex_map[exid]
                is_input = exchange['isInput']
                is_not_elementary = exchange['flow']['flowType'] != 'ELEMENTARY_FLOW'
                if is_input and is_not_elementary:
                    pid = exchange['defaultProvider']['@id']
                    fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(pid))
                    with open(fp, 'r') as fp:
                        process = json.load(fp)
                    if 'exchanges' in process:
                        uuids = [ex['flow']['@id'] for ex in process['exchanges']]
                        for uuid in uuids:
                            if uuid not in seen:
                                self.network.add_edge(exid, uuid)
                                q.append(uuid)
                                seen.append(uuid)
                        ex_map_temp = {ex['flow']['@id']: ex for ex in process['exchanges']}
                        ex_map.update(ex_map_temp)
            print(len(q))

    def run_ecoinvent_processes_loops(self, processes):
        for process_name in processes:
            self.graph[process_name] = {}
            self.network.add_node(process_name, color='black', size=20)
            uuid = self.process_map[process_name]
            fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid))
            with open(fp, 'r') as fp:
                process = json.load(fp)
            exchanges = process['exchanges']
            for exchange in exchanges:
                is_input = exchange['isInput']
                is_not_elementary = exchange['flow']['flowType'] != 'ELEMENTARY_FLOW'

                flow_id = exchange['flow']['@id']
                self.graph[process_name][flow_id] = {'flow_name':exchange['flow']['name'],
                                                     'flow_type':exchange['flow']['flowType'],
                                                     'flow_id':exchange['flow']['@id'],
                                                     'amount': exchange['amount'],
                                                     }
                if is_input and is_not_elementary:
                    uuid2 = exchange['defaultProvider']['@id']
                    fp2 = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid2))
                    with open(fp2, 'r') as fp2:
                        process2 = json.load(fp2)
                    process_name2 = process2['name']
                    self.network.add_node(process_name2, color=2)
                    self.network.add_edge(process_name, process_name2, color='light grey')
                    exchanges2 = process2['exchanges']
                    for exchange2 in exchanges2:
                        is_input = exchange2['isInput']
                        is_not_elementary = exchange2['flow']['flowType'] != 'ELEMENTARY_FLOW'
                       
                        flow_id = exchange2['flow']['@id']
                        self.graph[process_name][flow_id] = {'flow_name':exchange2['flow']['name'],
                                                             'flow_type':exchange2['flow']['flowType'],
                                                             'flow_id':exchange2['flow']['@id'],
                                                             'amount': exchange2['amount'],
                                                             }
                        if is_input and is_not_elementary:
                            uuid3 = exchange2['defaultProvider']['@id']
                            fp3 = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid3))
                            with open(fp3, 'r') as fp3:
                                process3 = json.load(fp3)
                            process_name3 = process3['name']
                            self.network.add_node(process_name3, color=3)
                            self.network.add_edge(process_name2, process_name3, color='light grey')
                            exchanges3 = process3['exchanges']
                            for exchange3 in exchanges3:
                                is_input = exchange3['isInput']
                                is_not_elementary = exchange3['flow']['flowType'] != 'ELEMENTARY_FLOW'
                                
                                flow_id = exchange3['flow']['@id']
                                self.graph[process_name][flow_id] = {'flow_name':exchange3['flow']['name'],
                                                             'flow_type':exchange3['flow']['flowType'],
                                                             'flow_id':exchange3['flow']['@id'],
                                                             'amount': exchange3['amount'],
                                                             }
                                
                                if is_input and is_not_elementary:
                                    uuid4 = exchange3['defaultProvider']['@id']
                                    fp4 = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid4))
                                    with open(fp4, 'r') as fp4:
                                        process4 = json.load(fp4)
                                    process_name4 = process4['name']

                                    self.network.add_node(process_name4, color=4)
                                    self.network.add_edge(process_name3, process_name4, color='light grey')
                                if not is_not_elementary:
                                    self.network.add_node(exchange3['flow']['name'], color='red')
                                    self.network.add_edge(process_name3, exchange3['flow']['name'], color='light grey')

    def compute_impact_from_single_process(self, process_name, impact_category):
        uuid = self.process_map[process_name]
        fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid))
        with open(fp, 'r') as fp:
            process = json.load(fp)
        output_exchanges = [ e for e in process['exchanges'] if not e['isInput']]
        total_impact = 0
        for exchange in output_exchanges:
            fn = exchange['flow']['name']
            ft = exchange['flow']['flowType']
            fid = exchange['flow']['@id']
            fam = exchange['amount']
            # print(fn, ft)
            if ft == 'ELEMENTARY_FLOW':
                if fid in self.ecoinvent_lcia[impact_category]:
                    char = self.ecoinvent_lcia[impact_category][fid]['value']
                    impact = char * fam
                else:
                    impact = 0
                # print(impact, fn)
                total_impact += impact
        return total_impact

    def find_upstream_impacts_loops(self, processes, amounts):

        self.outputs = {pk:{} for pk in processes}

        # loop 0 -------------------------------------------------------------------------------------------------------
        for process_name in processes:
            amount0 = amounts[process_name]
            uuid0 = self.process_map[process_name]
            fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid0))
            with open(fp, 'r') as fp:
                process0 = json.load(fp)
            input_exchanges0  = [ e for e in process0['exchanges'] if e['isInput'] and e['flow']['flowType'] != 'ELEMENTARY_FLOW']
            output_exchanges0 = [ e for e in process0['exchanges'] if not e['isInput']]
            for oex0 in output_exchanges0:
                fn0 = oex0['flow']['name']
                ft0 = oex0['flow']['flowType']
                fid0 = oex0['flow']['@id']
                fam0 = oex0['amount'] * amount0
                unit0 = oex0['unit']['name']
                key0 = fid0
                if ft0 == 'ELEMENTARY_FLOW':
                    if key0 in self.outputs[process_name]:
                        self.outputs[process_name][key0]['amount'] += fam0
                    else:
                        self.outputs[process_name][key0] = {'name': fn0, 'flow_type': ft0, 'amount': fam0, 'id':fid0, 'unit': unit0}
            
            # loop 1 ---------------------------------------------------------------------------------------------------
            for iex1 in input_exchanges0:
                amount1 = iex1['amount']
                uuid1 = iex1['defaultProvider']['@id']
                fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid1))
                with open(fp, 'r') as fp:
                    process1 = json.load(fp)
                input_exchanges1  = [ e for e in process1['exchanges'] if e['isInput']]
                output_exchanges1 = [ e for e in process1['exchanges'] if not e['isInput']]
                for oex1 in output_exchanges1:
                    fn1 = oex1['flow']['name']
                    ft1 = oex1['flow']['flowType']
                    fid1 = oex1['flow']['@id']
                    fam1 = oex1['amount'] * amount0 * amount1
                    unit1 = oex1['unit']['name']
                    key1 = fid1
                    if ft1 == 'ELEMENTARY_FLOW':
                        if key1 in self.outputs[process_name]:
                            self.outputs[process_name][key1]['amount'] += fam1
                        else:
                            self.outputs[process_name][key1] = {'name': fn1, 'flow_type': ft1, 'amount': fam1, 'id':fid1, 'unit': unit1}
                # loop 2 ---------------------------------------------------------------------------------------------
                for iex2 in input_exchanges1:
                    amount2 = iex2['amount']
                    if iex2['flow']['flowType'] != 'ELEMENTARY_FLOW':
                        uuid2 = iex2['defaultProvider']['@id']
                        fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid2))
                        with open(fp, 'r') as fp:
                            process2 = json.load(fp)
                        input_exchanges2  = [ e for e in process2['exchanges'] if e['isInput']]
                        output_exchanges2 = [ e for e in process2['exchanges'] if not e['isInput']]
                        for oex2 in output_exchanges2:
                            fn2 = oex2['flow']['name']
                            ft2 = oex2['flow']['flowType']
                            fid2 = oex2['flow']['@id']
                            fam2 = oex2['amount'] * amount0 * amount1 * amount2
                            unit2 = oex2['unit']['name']
                            key2 = fid2
                            if ft2 == 'ELEMENTARY_FLOW':
                                if key2 in self.outputs[process_name]:
                                    self.outputs[process_name][key2]['amount'] += fam2
                                else:
                                    self.outputs[process_name][key2] = {'name': fn2, 'flow_type': ft2, 'amount': fam2, 'id':fid2, 'unit': unit2}

    def compute_elementary_flow_impacts(self, processes, amounts):
        #TODO: This will have to be redone after the final graph structure is set. 

        self.total = {k: 0 for k in self.ecoinvent_lcia}
        for process_name in processes:
            for ok in self.outputs[process_name]:
                fn  = self.outputs[process_name][ok]['name']
                fid = self.outputs[process_name][ok]['id']
                ft  = self.outputs[process_name][ok]['flow_type']
                fam = self.outputs[process_name][ok]['amount']
                for impact_cat_k in self.ecoinvent_lcia:
                    if ft == 'ELEMENTARY_FLOW':
                        if fid in self.ecoinvent_lcia[impact_cat_k]:
                            impact = self.ecoinvent_lcia[impact_cat_k][fid]['value'] * fam   #* amounts[process_name]
                            self.total[impact_cat_k] += impact


        # self.environmental_impacts = {k: {} for k in processes}
        # for process_name in processes:
        #     for impact_cat_k in self.ecoinvent_lcia:
        #         self.environmental_impacts[process_name][impact_cat_k] = 0
        #         for ok in self.outputs[process_name]:
        #             fn  = self.outputs[process_name][ok]['name']
        #             fid = self.outputs[process_name][ok]['id']
        #             ft  = self.outputs[process_name][ok]['flow_type']
        #             fam = self.outputs[process_name][ok]['amount']
        #             if fid in self.ecoinvent_lcia[impact_cat_k]:
        #                 impact = self.ecoinvent_lcia[impact_cat_k][fid]['value'] * fam 
        #                 self.environmental_impacts[process_name][impact_cat_k] += impact
        #                 if impact_cat_k == 'climate change - global warming potential (GWP100)':
        #                     print(process_name)
        #                     print(impact)
        #                     print('')

        # self.total = {k:0 for k in self.ecoinvent_lcia}
        # for pk in self.environmental_impacts:
        #     for ick in self.environmental_impacts[pk]:
        #         self.total[ick] += self.environmental_impacts[pk][ick]

        # # for ic in self.total:
        # #     self.total[ic] *= amounts[process_name]

if __name__ == '__main__': 

    # TODO: FIX THE PROCESS MAP TO HAVE ALL VERSIONS OF EACH PROCESS!!!

    for i in range(50): print('')

    lca = LCA()
    lca.ecoinvent_path = os.path.join(pod_lca.TEMP, 'ecoinvent_391_en15804gd_upr_n2_20230629')
    lca.ecoinvent_lcia_path = os.path.join(pod_lca.TEMP, 'ecoinvent_3_9_1_LCIA_Methods_openLCA_2_(1)')
    lca.read_ecoinvent_maps()
    lca.read_ecoinvent_lcia()

    #ETHAN TEST #######################################################################

    # pname = 'clinker production | clinker | EN15804, U'
    # icname = 'climate change - global warming potential (GWP100)'
    # print(lca.compute_impact_from_single_process(pname, icname))

    ############################################################################

    exp_results = {'acidification - acidification potential (AP)':0.661877466,
                   'climate change - global warming potential (GWP100)':334.5031055,
                   'ecotoxicity: freshwater - ecotoxicity: freshwater':1356.898015,
                   'eutrophication - eutrophication potential':0.308631429,
                   'human toxicity: carcinogenic - human toxicity: carcinogenic':9.16E-06,
                   'human toxicity: non-carcinogenic - human toxicity: non-carcinogenic':4.12E-05,
                   'ozone depletion - ozone depletion potential (ODP)':1.06E-06,
                   'particulate matter formation - particulate matter formation potential (PMFP)':0.097404705,
                   'photochemical oxidant formation - maximum incremental reactivity (MIR)':14.20324672,}



    p1 = 'cement production, Portland | cement, Portland | EN15804, U'
    p2 = 'market for tap water | tap water | EN15804, U'
    p3 = 'sand quarry operation, extraction from river bed | sand | EN15804, U'
    p4 = 'gravel production, crushed | gravel, crushed | EN15804, U'
    p5 = 'clinker production | clinker | EN15804, U'
    processes = [p1, p2, p3, p4]
    amounts = {p1:810, p2:2143, p3:1663, p4:40}  # this is in lbs

    amounts = {k:lbs_to_kgs(amounts[k]) for k in amounts}  # tansform to kgs
    lca.find_upstream_impacts_loops(processes, amounts)
    lca.compute_elementary_flow_impacts(processes, amounts)


    # ic = 'climate change - global warming potential (GWP100)'
    # print(lca.total[ic])
    # print('{:.2f}%'.format(100*(lca.total[ic] / exp_results[ic])))

    for ek in lca.total:
        print(ek)
        print('{:.2f}%'.format(100*(lca.total[ek] / exp_results[ek])))
        print(lca.total[ek])
        print('')

