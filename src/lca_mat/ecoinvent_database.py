from .LCI_database import LCIDatabase

class EcoinventDatabase(LCIDatabase):

    def __init__(self):

        self.name = "Ecoinvent"
        self.data = None
        