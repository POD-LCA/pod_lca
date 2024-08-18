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
from pod_lca.lca.process import Process
from pod_lca.lca.process import Flow

class LCA(object):

    def __init__(self):
        self.graph                  = {}
        self.outputs                = {}
        self.processes              = {}
        self.process_map            = None
        self.lcia_map               = None
        self.ecoinvent_path         = None
        self.ecoinvent_lcia_path    = None
        self.ecoinvent_lcia         = {}
        self.environmental_impacts  = {}
        self.min_amount             = .001

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
        nt = Network('1000px', '1700px', notebook=True)
        nt.repulsion()

        G = self.network
        nt.from_nx(G)
        nt.show('nx.html')
        # nx.draw(G)
        # print(G.edges)

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

    def find_upstream_impacts_sequential(self, processes_, amounts, units):

        temp_processes = []
        for pname in processes_:
            uuid = self.process_map[pname]
            key = '{}_{}'.format(uuid, 0)
            p = Process()
            p.uuid = uuid
            p.name = pname
            p.amount = amounts[pname]
            p.scaling_factor = amounts[pname]
            p.unit = units[pname]
            p.level = 0
            p.key = key
            p.parent = 'source'
            self.processes[key] = p
            
            temp_processes.append(key)
            self.graph[key] = {}

        counter = 0
        while len(temp_processes) > 0:
            counter += 1
            # print('length', len(temp_processes))
            pro_key = temp_processes.pop(0)
            pro = self.processes[pro_key]
            pro_uuid   = pro.uuid
            pro_scaling_factor = pro.scaling_factor
            pro_level   = pro.level

            fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(pro_uuid))
            with open(fp, 'r') as fp:
                process = json.load(fp)

            in_pro  = [e for e in process['exchanges'] if e['isInput'] and e['flow']['flowType'] == 'PRODUCT_FLOW']
            in_elm  = [e for e in process['exchanges'] if e['isInput'] and e['flow']['flowType'] == 'ELEMENTARY_FLOW']
            in_was  = [e for e in process['exchanges'] if e['isInput'] and e['flow']['flowType'] == 'WASTE_FLOW']
            # out_pro  = [e for e in process['exchanges'] if not e['isInput'] and e['flow']['flowType'] == 'PRODUCT_FLOW']
            out_elm  = [e for e in process['exchanges'] if not e['isInput'] and e['flow']['flowType'] == 'ELEMENTARY_FLOW']
            out_was  = [e for e in process['exchanges'] if not e['isInput'] and e['flow']['flowType'] == 'WASTE_FLOW']
            input_exchanges  = [ e for e in process['exchanges'] if e['isInput'] and e['flow']['flowType'] != 'ELEMENTARY_FLOW']
            output_exchanges = [ e for e in process['exchanges'] if not e['isInput']]
            # waste_exchanges = [ e for e in process['exchanges'] if not e['isInput'] and e['flow']['flowType'] != 'WASTE_FLOW']

            print('length', len(processes)) 
            uuid0 = processes.pop(0)
            fp = os.path.join(self.ecoinvent_path, 'processes', '{}.json'.format(uuid0))
            with open(fp, 'r', encoding='utf-8') as fp:
                process0 = json.load(fp)
            input_exchanges0  = [ e for e in process0['exchanges'] if e['isInput'] and e['flow']['flowType'] != 'ELEMENTARY_FLOW']
            output_exchanges0 = [ e for e in process0['exchanges'] if not e['isInput']]

            for oex in output_exchanges:
                fname = oex['flow']['name']
                ftype = oex['flow']['flowType']
                fuuid = oex['flow']['@id']
                funit = oex['unit']['name']
                famnt = oex['amount']
                fkey = '{}_{}_{}'.format(fuuid, pro_level + 1, counter)

                f = Flow()
                f.name = fname
                f.flow_type = ftype
                f.uuid = fuuid
                f.amount = famnt 
                f.scaling_factor = famnt * pro_scaling_factor
                f.unit = funit
                pro.outputs.append(fkey)
                self.outputs[fkey] = f
            

            for inex in input_exchanges:
                ename = inex['flow']['name']
                eamnt = inex['amount']
                eunit = inex['unit']['name']
                e_scaling_factor = eamnt * pro_scaling_factor
                e_pro_uuid = inex['defaultProvider']['@id']
                e_pro_key = '{}_{}'.format(e_pro_uuid, pro_level + 1)

                if e_scaling_factor > self.min_amount:
                    temp_processes.append(e_pro_key)
                    epro = Process()
                    epro.uuid = e_pro_uuid
                    epro.name = ename
                    epro.amount = eamnt
                    epro.scaling_factor = pro_scaling_factor * eamnt
                    epro.unit = eunit
                    epro.level = pro_level + 1
                    epro.key = e_pro_key
                    epro.parent = pro_key

                    if e_pro_key in self.processes:
                        e_pro_key = '{}_{}'.format(e_pro_key, counter)

                    self.processes[e_pro_key] = epro

                    pro.inputs[e_pro_key] = epro

    def compute_environmental_impacts(self):
        self.environmental_impacts = {ick:0 for ick in self.ecoinvent_lcia}
        for fkey in self.outputs:
            flow = self.outputs[fkey]
            if flow.flow_type == 'ELEMENTARY_FLOW':
                for ick in self.ecoinvent_lcia:
                    if flow.uuid in self.ecoinvent_lcia[ick]:
                        impact = self.ecoinvent_lcia[ick][flow.uuid]['value'] * flow.scaling_factor
                        self.environmental_impacts[ick] += impact

    def run_units_test(self):
        units = set()
        for pk in self.processes:
            pro = self.processes[pk]
            punit = pro.unit
            units.add(punit)
        print(units)


if __name__ == '__main__': 

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

    p1 = 'cement production, Portland | cement, Portland | EN15804, U - United States'
    p2 = 'market for tap water | tap water | EN15804, U - Rest-of-World'
    p3 = 'sand quarry operation, extraction from river bed | sand | EN15804, U - Rest-of-World'
    p4 = 'gravel production, crushed | gravel, crushed | EN15804, U - Rest-of-World'
    # p5 = 'clinker production | clinker | EN15804, U - United States'
    # p5 = 'clinker production | clinker | EN15804, U'
    processes = [p1, p2, p3, p4]
    # processes = [p1]
    amounts = {p1:810, p2:2143, p3:1663, p4:40}  # this is in lbs
    # processes = [p1]
    amounts = {p1:810, p2:2143, p3:1663, p4:40}  # this is in lbs

    amounts = {k:lbs_to_kgs(amounts[k]) for k in amounts}  # tansform to kgs
    units = {k: 'kg' for k in amounts}

    # WHILE LOOP VERSION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    lca.min_amount = .001
    lca.min_amount = .1
    lca.find_upstream_impacts_sequential(processes, amounts, units)
    lca.compute_environmental_impacts()

    for ek in lca.environmental_impacts:
        print(ek)
        print('{:.2f}%'.format(100*(lca.environmental_impacts[ek] / exp_results[ek])))
        print(lca.environmental_impacts[ek],'    ', exp_results[ek])
        print('')

    lca.run_units_test()


