__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =================================
# LCI DATABASE CLASS
# =================================


class LCIDatabase:

    def __init__(self):

        self.name = None
        self.unit_processes = {}
        self.impacts = {}

    def get_unit_processess(self):
        """Returns a list of corresponding UnitProcess Objects."""
        pass

    def load_impacts(self):

        pass

    def get_impacts(self):

        if self.impacts:
            return self.impacts
        else:
            return self.load_impacts()


# =================================
# UNIT PROCESS CLASS
# =================================


class UnitProcess:

    def __init__(self, name):
        self.unit_process_id = None
        self.name = name
        self.exchanges = {}
        self.location = None
        self.qty = 0.0
        self.unit = None
        # TODO: Check other properties needed to be stored

    def __str__(self):
        # print("=====================")
        # print("Process name : ", self.get_name())
        # print("location : ", self.get_location())
        # print("qty : {:.2f}".format(self.qty), self.unit)
        # print("=====================")
        pass

    def get_name(self):

        return self.name

    def get_process_id(self):

        return self.unit_process_id

    def get_exchanges(self):

        return self.exchanges

    def get_location(self):

        return self.location

    def set_exchange(self, name, exchange):

        if not (exchange in self.get_exchanges.keys()):
            self.exchanges[name] = exchange
        else:
            raise NotImplementedError


# =================================
# EXCHANGE CLASS
# =================================


class Exchange:

    def __init__(self):
        self.name = None
        self.qty = 0.0
        self.unit = None
        self.flow_id = None
        self.is_elementary_flow = False
        self.is_product_flow = False
        self.is_waste_flow = False
        self.unit_process_id = None
        self.location = None

    def get_qty(self):

        return self.qty

    def get_flow_id(self):

        return self.flow_id

    # TODO: create getters and setters


# =================================
# IMPACT CLASS
# =================================


class Impact:

    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.unit = None
        self.qty = 0.0
        self.flow_impacts = {}

    def get_flows(self):

        return self.flow_impacts

    def get_name(self):

        return self.name

    def get_unit(self):

        return self.unit

    def get_qty(self):

        return self.qty

    def add_qty(self, qty):

        self.qty += qty
