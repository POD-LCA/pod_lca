from lca_mat.processess import ProcessessMatrix

from numpy import where, zeros

import os
import shutil
import time

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =================================
# PROBLEM CLASS
# =================================

class Problem(object):

    def __init__(self):
        self.database = None
        self.process_matrix = None
        self.demand = {}
        self.product_process_matrix = None
        self.process_exchange_matrix = None
        self.problem_settings = None

    # =================================
    # Setters / Getters
    # =================================

    def set_database(self, database):
        """ Sets database for the problem.
        
        Inputs:
        ------
            database    : LCIDatabase obj.
        
        """
        self.database = database
    
    def set_process_matrix(self, process_matrix):
        """ Sets process matrix for the problem.
        
        Inputs:
        ------
            process_matrix    : dict.
        
        """
        self.process_matrix = process_matrix

    def set_product_process_matrix(self, product_process_matrix):
        """ Sets selection matrix for the problem.
        
        Inputs:
        ------
            selection_matrix    : array.
        
        """
        self.product_process_matrix = product_process_matrix

    def set_process_exchange_matrix(self, proces_exchange_matrix):
        """ Sets selection matrix for the problem.
        
        Inputs:
        ------
            selection_matrix    : array.
        
        """
        self.process_exchange_matrix = proces_exchange_matrix

    def set_demand(self, row, val):

        if self.get_demand():
            self.demand[row] = val
        else:
            print("No inventory to set demand. Create process matrix before setting demand.")

    def get_database(self):
        """ Gets database for the problem.
        """
        return self.database
    
    def get_process_matrix(self):
        """ Gets process matrix for the problem.
        """
        return self.process_matrix

    def get_product_process_matrix(self):
        """ Gets selection matrix for the problem.
        """
        return self.product_process_matrix
    
    def get_product_exchange_matrix(self):

        return self.process_exchange_matrix
    
    def get_demand(self):

        return self.demand

    # =================================
    # Printer Methods
    # =================================

    def print_unit_processes(self, n=50):

        terminal_size = shutil.get_terminal_size()
        lines_per_page = terminal_size.lines - 2 
        os.system('cls' if os.name == 'nt' else 'clear')

        P = self.get_process_matrix()

        if P is not None:
            ids = P.get_process_ids()
            unitProcesss = self.get_database().get_unit_processess()
            print("col. no | process ID | process name")
            ctr = 0
            for id in ids.keys():
                print(str(ids[id]) + " | " +  id + " | " +  unitProcesss[id].get_name()[:n] + "...")

                if ctr > lines_per_page:
                    input("\nPress Enter to continue...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("col. no | process ID | process name")
                    ctr = 0
                else:
                    ctr += 1
        else:
            print("Create process matrix to load unit processess.")

    def print_inventory(self, n=100):

        terminal_size = shutil.get_terminal_size()
        lines_per_page = terminal_size.lines - 2 
        os.system('cls' if os.name == 'nt' else 'clear')

        P = self.get_process_matrix()
        if P is not None:
            inventory = P.get_basis().get_inventory_dict()
            print("row. no | exchange name | location | unit process id")
            ctr = 0
            for id in inventory.keys():
                prt_str = str(inventory[id].get_row_num()) + " | " +  inventory[id].get_name()[:n]
                if len(inventory[id].get_name()) > n:
                    prt_str += "..."
                prt_str += (" | " + inventory[id].get_location()) if inventory[id].get_location() is not None else " | --- "
                prt_str += (" | " + inventory[id].get_unit_process_id()) if inventory[id].get_unit_process_id() is not None else " | --- "
                print(prt_str)

                if ctr > lines_per_page:
                    input("\nPress Enter to continue...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("row. no | exchange name | location | unit process id")
                    ctr = 0
                else:
                    ctr += 1
        else:
            print("Create process matrix to load unit processess.")


    # =================================
    # User Methods
    # =================================

    def create_process_matrix(self, process_id=None):
        """ Creates the full process matrix.
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        P = ProcessessMatrix()
        inventory_vector = P.get_basis()
        database = self.get_database()
        unit_processes = database.get_unit_processess(process_id)
        for unit_process in unit_processes.keys():
            inventory_ids, exchange_qtys = inventory_vector.add_inventory_items(unit_processes[unit_process].get_exchanges())
            P.add_process(unit_processes[unit_process].get_process_id(), inventory_ids, exchange_qtys)

        self.set_process_matrix(P)

        # create demand matrix with all zeros
        rows = self.get_process_matrix().get_no_rows()
        self.demand = dict.fromkeys(range(rows), 0)

    def generate_product_process_matrix(self):
        
        rows = self.get_process_matrix().get_no_rows()
        cols = self.get_process_matrix().get_no_cols()

        product_process_matrix = zeros((rows, cols), dtype = 'bool')

        inventory_dict = self.get_process_matrix().get_basis().get_inventory_dict()
        process_ids = self.get_process_matrix().get_process_ids()

        for item in inventory_dict.keys():
            if inventory_dict[item].unit_process_id is not None:
                row = inventory_dict[item].get_row_num()
                col = process_ids[inventory_dict[item].unit_process_id]
                product_process_matrix[row][col] = True
        
        self.set_product_process_matrix(product_process_matrix)


    def generate_process_exchange_matrix(self):
        
        rows = self.get_process_matrix().get_no_rows()
        cols = self.get_process_matrix().get_no_cols()

        process_exchange_matrix = zeros((rows, cols), dtype = 'bool')

        process_mat_data = self.get_process_matrix().get_mat_data()

        for col in range(cols):
            for row in process_mat_data[col].keys():
                process_exchange_matrix[row][col] = True


        self.set_process_exchange_matrix(process_exchange_matrix)


    def solve():
        """ Solves the LCI problem.
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        pass
    
    # =================================
    # Private Methods
    # =================================

    def _partition_process_matrix(self, tol = 0.001):


        P = self.get_process_matrix()
        PP = self.get_product_process_matrix()
        PE = self.get_product_exchange_matrix()

        rows = set()
        cols = set()

        d = self.get_demand()
        for row in d.keys():
            if d[row] > tol:
                rows.add(row)

        no_rows, no_cols = len(rows), len(cols)
        update = True
        while update:
            cols.update(where(PP[list(rows),:])[1].tolist())
            rows.update(where(PE[:, list(cols)])[0].tolist())

            if (no_rows == len(rows)) and (no_cols == len(cols)):
                update = False
            else:
                no_rows, no_cols = len(rows), len(cols)

        # TODO: get the rows corresponding to processes

        return list(rows), list(cols)
        



if __name__ == '__main__':

    from lca_mat import HOME
    from lca_mat.ecoinvent_database import EcoinventDatabase

    from numpy import sum as npsum

    test_problem = Problem()

    database_path = HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629'
    database = EcoinventDatabase(database_path)

    test_problem.set_database(database)
    test_problem.create_process_matrix() # "a4c20f01-adb5-41ad-80af-fdc2b175585b"
    test_problem.generate_product_process_matrix()
    test_problem.generate_process_exchange_matrix()

    # processess
    # p1 = 'cement production, Portland | cement, Portland | EN15804, U - United States'
    # p2 = 'market for tap water | tap water | EN15804, U - Rest-of-World'
    # p3 = 'sand quarry operation, extraction from river bed | sand | EN15804, U - Rest-of-World'
    # p4 = 'gravel production, crushed | gravel, crushed | EN15804, U - Rest-of-World'

    # print("water")
    # process_lst = test_problem.get_database().find_process_by_name("market for tap water | tap water | EN15804, U")
    # for process in process_lst:
    #     print(process.get_process_id())
    #     print(process.location)

    # process ids
    # p1 = 'b6d92fa7-13c9-448b-9231-4736c9c4005a'
    # p2 = '3919839c-646f-422b-9cef-95879b14c52c'
    # p3 = 'efc81209-41ba-4abb-a293-a01f4489cf0a'
    # p4 = 'c8671c12-d160-44e7-9d93-e99d373cbd4a'

    # product ids
    # p1 = 'c5299a8e-d4b4-409c-9826-e8ae9e37c03d'
    # p2 = 'c5adb1fb-872e-4446-a3bb-c4b61aa4bd45'
    # p3 = 'f51d7ccf-0bee-430d-98a3-8334adbe39fc'
    # p4 = '37eceabd-b33f-4757-a4b9-5c51dee1710d'

    # col = test_problem.get_process_matrix().get_process_ids()['c8671c12-d160-44e7-9d93-e99d373cbd4a']
    # output_row = [key for key, value in test_problem.get_process_matrix().get_mat_data()[col].items() if value < 0]

    # product row
    # p1 = 250132
    # p2 = 104168
    # p3 = 211522
    # p4 = 243025

    test_problem.set_demand(250132, val=5)

    test_problem.print_unit_processes()
    # test_problem.print_inventory()

    rows, cols = test_problem._partition_process_matrix()
    # TODO: Compare tree method with matrix method (see they get the same number of process)

    # solve
        # determine the unit processe (cols) in the system
        # determine corresponding rows
        # partition and invert process matrix
        # update inventory

    # start = time.time()
    # end = time.time()
    # print(start - end)
