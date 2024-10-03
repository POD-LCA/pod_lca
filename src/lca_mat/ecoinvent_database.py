from lca_mat.LCI_database import Exchange, LCIDatabase, UnitProcess, Impact

import json
import os
import time


class EcoinventDatabase(LCIDatabase):

    def __init__(self, process_file_path=None, impact_file_path=None):
        super().__init__()
        self.name = "Ecoinvent"
        self.process_file_path = process_file_path
        self.impact_file_path = impact_file_path

    # =================================
    # Setters / Getters
    # =================================

    def set_process_file_path(self, file_path):

        self.process_file_path = file_path

    def set_impact_file_path(self, file_path):

        self.impact_file_path = file_path

    def set_unit_processes(self, unit_processes):

        self.unit_processes = unit_processes
    
    # =================================
    # Printers
    # =================================

    def print_flow(self):

        pass

    def print_exchange(self):

        pass

    # =================================
    # Searchers
    # =================================

    def find_process_by_name(self, name):
        
        process_lst = []

        unit_processes = self.get_unit_processess()
        for unit_process in unit_processes.keys():
            if name in unit_processes[unit_process].get_name():
                process_lst.extend([unit_processes[unit_process]])
            
        return process_lst


    # =================================
    # Methods
    # =================================

    def get_unit_processess(self, process_id=None):
        """ Returns a list of corresponding UnitProcess Objects.
        """
        if self.unit_processes:
            if process_id is None:
                return self.unit_processes
            else:
                raise NotImplementedError
        else:
            if process_id is None:
                return self.load_unit_processess_all()
            else:
                return self.load_unit_processes_tree(process_id)


    def load_unit_processess_all(self):
        """ Returns a list of all UnitProcess Objects.
        """

        unit_processes = {}

        path = os.path.join(self.process_file_path, 'processes')
        files = os.listdir(path)
        for file in files:
            if file.endswith('json'):
                process_id = os.path.splitext(file)[0]    
                unit_process = EcoinventDatabase.get_unit_process(process_id, path)
                unit_processes[process_id] = unit_process
        
        self.unit_processes = unit_processes
                        
        return unit_processes
    
    def load_unit_processes_tree(self, root_id):
        """ Returns a list of all UnitProcess Objects, required for the production of a given product (process).
        """

        unit_processes = {}

        path = os.path.join(self.process_file_path, 'processes')
        id_list = [root_id]
        n = len(id_list)
        i = 0
        while i < n:
            process_id = id_list[i]
            unit_process = EcoinventDatabase.get_unit_process(process_id, path)
            dependent_processes = EcoinventDatabase.get_dependent_processes(unit_process)
            for dependent_process in dependent_processes:
                if not dependent_process in id_list:
                    id_list.extend([dependent_process])

            i += 1
            n = len(id_list)

            unit_processes[process_id] = unit_process
        
        self.unit_processes = unit_processes

        return unit_processes

    def load_impacts(self):

        folder = os.path.join(self.impact_file_path, 'lcia_categories')
        files = os.listdir(folder)
        for file in files:
            file_path = os.path.join(folder, file)
            if file.endswith('json'):
                with open(file_path, 'r', encoding='utf-8') as fp:
                    lcia = json.load(fp)

                id = os.path.splitext(file)[0]
                name = lcia["name"]   
                impact = Impact(name, id)
                impact.unit = lcia["refUnit"]
                for impact_factor in  lcia["impactFactors"]:
                    impact.flow_impacts[impact_factor["flow"]["@id"]] = impact_factor["value"]

                self.impacts[file] = impact

        return self.impacts

    @staticmethod
    def get_dependent_processes(unit_process):
        """ Returns a list of all first level process IDs (i.e., direct dependencies) required for the production 
            of a given product (process).
        """
        dependent_processes = []

        exchanges = unit_process.get_exchanges()
        for exchange in exchanges.keys():
            if exchanges[exchange].is_product_flow:
                dependent_processes.extend([exchanges[exchange].unit_process_id])

        return dependent_processes
    
    @staticmethod
    def get_unit_process(process_id, folder):
        """ Returns UnitProcess Object given the corresponding process ID.
        """
        
        file = os.path.join(folder, process_id + '.json')
        with open(file, 'r', encoding='utf-8') as fp:
            lcia = json.load(fp)
        if lcia["@type"] == "Process":
            #if lcia["processType"] == "UNIT_PROCESS": # TODO: Do these have to be unit processes? What is the distinction?
            name = lcia["name"]
            unit_process = UnitProcess(name)
            unit_process.unit_process_id = lcia["@id"] #+ '_' +  lcia["location"]["name"]
            unit_process.location = lcia["location"]["name"]
        
            exchange_data = lcia["exchanges"]
            for item in exchange_data: 
                exchange = Exchange()
                
                exchange.name = item["flow"]["name"]
                exchange.unit = item["flow"]["refUnit"]
                exchange.flow_id = item["flow"]["@id"]

                exchange.is_elementary_flow = True if item['flow']['flowType'] == 'ELEMENTARY_FLOW' else False
                exchange.is_waste_flow = True if item['flow']['flowType'] == 'WASTE_FLOW' else False
                exchange.is_product_flow = True if item['flow']['flowType'] == 'PRODUCT_FLOW' else False

                if item["isInput"]:
                    if exchange.is_product_flow:
                        unit_process_id = item["defaultProvider"]["@id"]
                        location = item["defaultProvider"]["location"] if isinstance(item["defaultProvider"]["location"], str) else item["defaultProvider"]["location"]["name"]
                    else:
                        unit_process_id = None
                        location = None
                    qty = -1 * item["amount"]
                else:
                    if exchange.is_product_flow:
                        unit_process_id = unit_process.unit_process_id
                        location = unit_process.location
                    else:
                        unit_process_id = None
                        location = None                        
                    qty = item["amount"]

                exchange.unit_process_id = unit_process_id
                exchange.qty = qty
                exchange.location = location
                exchange_key = item["internalId"]
                unit_process.exchanges[exchange_key] = exchange

            fp.close()
            return unit_process
    # TODO: Else condition
    
    # TODO: use getters and setters
    # TODO: docstrings


if __name__ == '__main__':

    from lca_mat import HOME

    database = EcoinventDatabase()
    database.set_process_file_path(HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629')
    database.set_impact_file_path(HOME + '\Archive\ecoinvent_3_9_1_LCIA_Methods_openLCA_2_(1)')

    start = time.time()
    database.get_unit_processess_all()
    # database.get_unit_processes_tree("a4c20f01-adb5-41ad-80af-fdc2b175585b")
    database.load_impacts()
