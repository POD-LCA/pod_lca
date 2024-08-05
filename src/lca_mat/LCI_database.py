
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =================================
# LCI DATABASE CLASS
# =================================

class LCIDatabase():
    
    def __init__(self):

        self.name = None
        self.data = None

    def get_unit_processess():
        """  Returns a list of UnitProcess Objects.
        
        """

        # TODO: implement method
        pass

# =================================
# UNIT PROCESS CLASS
# =================================

class UnitProcess():

    def __init__(self):
        self.exchanges = {}
        # TODO: Check other properties needed to be stored

    def get_exchanges(self):

        return self.exchanges
    
    def set_exchange(self, name, exchange):

        if not (exchange in self.get_exchanges.keys()):
            self.exchanges[name] = exchange
        else:
            raise NotImplementedError

# =================================
# EXCHANGE CLASS
# =================================

class Exchange():

    def __init__(self):
        self.name = None
        self.qty = 0.0
        self.unit = None

    def get_qty(self):

        return self.qty
