from .processess import ProcessessMatrix

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

    # =================================
    # Methods
    # =================================

    def create_process_matrix(self):
        """ Creates the full process matrix.
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        P = ProcessessMatrix()
        inventory_vector = P.get_basis()
        database = self.get_database()
        unit_processes = database.get_unit_processess()
        for unit_process in unit_processes:
            exchanges = unit_process.get_exchanges()
            for exchange in exchanges:
                inventory_vector.add_inventory_item(exchange)
                ## this only give the exchange name... how to transfer the other details of the exchange
            P.add_process()


    def solve():
        """ Solves the LCI problem.
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        pass
    


