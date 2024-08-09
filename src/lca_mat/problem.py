from lca_mat.processess import ProcessessMatrix

from numpy import where, zeros

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
        self.selection_matrix = None
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

    def set_selection_matrix(self, selection_matrix):
        """ Sets selection matrix for the problem.
        
        Inputs:
        ------
            selection_matrix    : array.
        
        """
        self.selection_matrix = selection_matrix

    def set_demand(self, row, val):

        if not self.get_demand():
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

    def get_selection_matrix(self):
        """ Gets selection matrix for the problem.
        """
        return self.selection_matrix
    
    def get_demand(self):

        return self.demand

    # =================================
    # Printer Methods
    # =================================

    def print_unit_processes(self, n=50):

        P = self.get_process_matrix()

        if P is not None:
            ids = P.get_process_ids()
            unitProcesss = self.get_database().get_unit_processess()
            print("col. no | process ID | process name")
            for id in ids.keys():
                print(str(ids[id]) + " | " +  id + " | " +  unitProcesss[id].get_name()[:n] + "...")
        else:
            print("Create process matrix to load unit processess.")

    def print_inventory(self, n=100):

        P = self.get_process_matrix()
        if P is not None:
            inventory = P.get_basis().get_inventory_dict()
            print("row. no | exchange name | location | unit process id")
            for id in inventory.keys():
                prt_str = str(inventory[id].get_row_num()) + " | " +  inventory[id].get_name()[:n]
                if len(inventory[id].get_name()) > n:
                    prt_str += "..."
                prt_str += (" | " + inventory[id].get_location()) if inventory[id].get_location() is not None else " | --- "
                prt_str += (" | " + inventory[id].get_unit_process_id()) if inventory[id].get_unit_process_id() is not None else " | --- "
                print(prt_str)
        else:
            print("Create process matrix to load unit processess.")

        # TODO: print if it is an product flow



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
            inventory_ids = inventory_vector.add_inventory_items(unit_processes[unit_process].get_exchanges())
            P.add_process(inventory_ids, unit_processes[unit_process].get_process_id())

        self.set_process_matrix(P)

        # create demand matrix with all zeros
        rows = self.get_process_matrix().get_no_rows()
        self.demand = dict.fromkeys(range(rows), 0)

    def generate_selection_matrix(self):
        
        rows = self.get_process_matrix().get_no_rows()
        cols = self.get_process_matrix().get_no_cols()

        selecion_matrix = zeros((rows, cols), dtype = 'bool')

        inventory_dict = self.get_process_matrix().get_basis().get_inventory_dict()
        process_ids = self.get_process_matrix().get_process_ids()

        for item in inventory_dict.keys():
            if inventory_dict[item].unit_process_id is not None:
                row = inventory_dict[item].get_row_num()
                col = process_ids[inventory_dict[item].unit_process_id]
                selecion_matrix[row][col] = True
        
        self.set_selection_matrix(selecion_matrix)


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
        S = self.get_selection_matrix()

        rows = set()
        cols = set()

        d = self.get_demand()
        for row in d.keys():
            if d[row] > tol:
                rows.add(row)

        lst = where(S[rows])

        inventory = P.basis.q[0].get_unit_process_id()
        # in selection matrix, get columns where those rows are non zeros
            # add those to cols
        








if __name__ == '__main__':

    from lca_mat import HOME
    from lca_mat.ecoinvent_database import EcoinventDatabase

    from numpy import sum as npsum

    test_problem = Problem()

    database_path = HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629'
    database = EcoinventDatabase(database_path)

    test_problem.set_database(database)
    test_problem.create_process_matrix("a4c20f01-adb5-41ad-80af-fdc2b175585b") # "f35f761d-9551-4191-9d70-c111ab212bab"
    test_problem.generate_selection_matrix()

    test_problem.set_demand(row=10, val=5)

    # test_problem.print_unit_processes()
    # test_problem.print_inventory()

    test_problem._partition_process_matrix()
    

    # solve
        # determine the unit processe (cols) in the system
        # determine corresponding rows
        # partition and invert process matrix
        # update inventory

    # start = time.time()
    # end = time.time()
    # print(start - end)
