from lca_mat.processess import ProcessessMatrix

from numpy import zeros

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
        self.demand = {}
        self.process_matrix = None
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

    def get_database(self):
        """ Gets database for the problem.
        """
        return self.database
    
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

    def get_process_matrix(self):
        """ Gets process matrix for the problem.
        """
        return self.process_matrix

    # =================================
    # Methods
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
        for unit_process in unit_processes:
            exchanges = unit_process.get_exchanges()
            for exchange_id in exchanges.keys():
                inventory_vector.add_inventory_item(exchange_id, exchanges[exchange_id].__dict__)
            P.add_process(exchanges, unit_process.get_process_id())

        self.set_process_matrix(P)

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
    

if __name__ == '__main__':

    from lca_mat import HOME
    from lca_mat.ecoinvent_database import EcoinventDatabase

    from numpy import sum as npsum

    test_problem = Problem()

    database_path = HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629'
    database = EcoinventDatabase(database_path)

    test_problem.set_database(database)
    test_problem.create_process_matrix("a4c20f01-adb5-41ad-80af-fdc2b175585b")
    test_problem.generate_selection_matrix()
    
    # why there more processes than inventory items??
    npsum(test_problem.selection_matrix, axis=0)
    npsum(test_problem.selection_matrix, axis=1)

    # set demand
    # solve
        # determine the unit processe (cols) in the system
        # determine corresponding rows
        # partition and invert process matrix
        # update inventory

    # start = time.time()
    # end = time.time()
    # print(start - end)
