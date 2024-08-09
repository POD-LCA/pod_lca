from lca_mat.LCI_database import Exchange, LCIDatabase, UnitProcess

import json
import os
import time


class EcoinventDatabase(LCIDatabase):

    def __init__(self, file_path=None):

        self.name = "Ecoinvent"
        self.file_path = file_path
        self.unit_processes = {}

    # =================================
    # Setters / Getters
    # =================================

    def set_file_path(self, file_path):

        self.file_path = file_path

    def set_unit_processes(self, unit_processes):

        self.unit_processes = unit_processes
    
    # =================================
    # Printers
    # =================================

    def print_process(self):

        pass

    def print_flow(self):

        pass

    def print_exchange(self):

        pass
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

        path = os.path.join(self.file_path, 'processes')
        files = os.listdir(path)
        for file in files:
            if file.endswith('json'):
                process_id = os.path.splitext(file)[0]    
                unit_process = EcoinventDatabase.get_unit_process(process_id, path)
                unit_processes[process_id] = unit_process
                        
        return unit_processes
    
    def load_unit_processes_tree(self, root_id):
        """ Returns a list of all UnitProcess Objects, required for the production of a given product (process).
        """

        unit_processes = {}

        path = os.path.join(self.file_path, 'processes')
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
        return unit_processes

    @staticmethod
    def get_dependent_processes(unit_process):
        """ Returns a list of all first level process IDs (i.e., direct dependencies) required for the production 
            of a given product (process).
        """
        dependent_processes = []

        exchanges = unit_process.get_exchanges()
        for exchange in exchanges.keys():
            if not exchanges[exchange].is_elementary_flow:
                if exchanges[exchange].unit_process_id is not None:
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
        
            exchange_data = lcia["exchanges"]
            for item in exchange_data: 
                exchange = Exchange()
                exchange.name = item["flow"]["name"]
                exchange.qty = item["amount"]
                exchange.unit = item["flow"]["refUnit"]
                exchange.flow_id = item["flow"]["@id"]
                if item["flow"]["flowType"] == "PRODUCT_FLOW":
                    exchange.is_elementary_flow = False
                    if item["isInput"]:
                        exchange.unit_process_id = item["defaultProvider"]["@id"]
                        location = item["defaultProvider"]["location"] if isinstance(item["defaultProvider"]["location"], str) else item["defaultProvider"]["location"]["name"]
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
    database.set_file_path(HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629')

    start = time.time()
    # database.get_unit_processess_all()
    database.get_unit_processes_tree("a4c20f01-adb5-41ad-80af-fdc2b175585b")
    end = time.time()
    elapsed = start - end
    print(elapsed)
