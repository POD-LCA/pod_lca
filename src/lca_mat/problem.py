from lca_mat.processess import ProcessessMatrix

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
            database    : LCIDatabase obj.
        
        """
        self.process_matrix = process_matrix

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

    test_problem = Problem()

    database_path = HOME + '\Archive\ecoinvent_391_en15804gd_upr_n2_20230629'
    database = EcoinventDatabase(database_path)

    test_problem.set_database(database)
    start = time.time()
    test_problem.create_process_matrix("a4c20f01-adb5-41ad-80af-fdc2b175585b")
    end = time.time()
    print(start - end)
