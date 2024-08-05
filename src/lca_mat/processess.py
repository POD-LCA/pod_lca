__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =================================
# PROCESSESS MATRIX CLASS
# =================================

class ProcessessMatrix():

    def __init__(self):
        self.P = []
        self.basis = {}

    # =================================
    # Setters / Getters
    # =================================

    def get_basis(self):
        """ Gets basis (i.e., inventory vector) of the processes space.
        """
        return self.basis

    # =================================
    # Methods
    # =================================

    def add_process():
        """ Adds a process to the Processes Matrix (P).
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        # TODO: write implementation
        pass

# =================================
# INVENTORY VECCTOR CLASS
# =================================

class InventoryVector():

    def __init__(self):
        self.q = {}

    # =================================
    # Setters / Getters
    # =================================

    def get_inventory(self):
        """ Gets inventory dictionary.
        """
        return self.q

    # =================================
    # Methods
    # =================================

    def add_inventory_item(self, name, row, place=None, unit=None, qty=None):
        """ Adds a new item to the inventory (q).
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        inventory = self.get_inventory()
        if not (name in inventory.keys()):
            new_inventory_item = InventoryItem(name, row)
            # TODO: Set other properties of the inventory item
            inventory[name] = new_inventory_item

# =================================
# INVENTORY ITEM CLASS
# =================================

class InventoryItem():

    def __init__(self, name, row):
        self.name = name
        self.row = row
        self.place = None
        self.unit = None
        self.qty = 0.0
