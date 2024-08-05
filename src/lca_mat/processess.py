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
        self.mat_data = {}
        self.basis = {}

    # =================================
    # Setters / Getters
    # =================================

    def get_mat_data(self):
        """ Gets process matrix data.
            Matrix is kept as a dictionary of dictionaries, where the outer dictionary key is column number (process) 
            and the inner dictionary key is the row numbern (inventory item) and the value is the value (qty) on the 
            corresponding entry of the matrix.
        """
        return self.mat_data
    
    def get_basis(self):
        """ Gets basis (i.e., inventory vector) of the processes space.
        """
        return self.basis

    # =================================
    # Methods
    # =================================

    def add_process(self, exchanges):
        """ Adds a process to the Processes Matrix (P).
        
        Inputs:
        ------
            exchanges : dict.
                Dictionary of all exchanges.
        
        """
        mat_data = self.get_mat_data()
        col = len(mat_data)

        inventory = self.get_basis()
        new_process = {}
        for exchange in exchanges.keys():
            row = inventory[exchange]
            qty = exchanges[exchange].get_qty()
            new_process[row] = qty
        mat_data[col] = new_process

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

    def add_inventory_item(self, name, properties={}):
        """ Adds a new item to the inventory (q).
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        inventory = self.get_inventory()
        n = len(inventory)
        if not (name in inventory.keys()):
            new_inventory_item = InventoryItem(name, n)
            new_inventory_item.set_properties(properties)
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

    def set_properties(self, properties={}):
        
        pass
