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
        self.basis = InventoryVector()
        self.process_ids = {}
        self.no_rows = 0
        self.no_cols = 0

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
    
    def get_no_rows(self):
        """ Gets number of rows in the Process matrix.
        """
        return self.no_rows
    
    def get_no_cols(self):
        """ Gets number of cols in the Process matrix.
        """
        return self.no_cols
    
    def get_process_ids(self):
        """ Gets a dictionary of process ids corresponding to columns of the Process matrix.
        """
        return self.process_ids


    # =================================
    # Methods
    # =================================

    def add_process(self, exchanges, unit_process_id):
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
            inventory_item = inventory.get_inventory_dict()[exchange]
            new_process[inventory_item.get_row_num()] = inventory_item.get_qty()
        mat_data[col] = new_process
        self.process_ids[unit_process_id] = col

        self.no_rows = inventory.get_inventory_size()
        self.no_cols = col + 1

# =================================
# INVENTORY VECCTOR CLASS
# =================================

class InventoryVector():

    def __init__(self):
        self.q = {}
        self.n = 0

    # =================================
    # Setters / Getters
    # =================================

    def get_inventory_dict(self):
        """ Gets inventory dictionary.
        """
        return self.q
    
    def get_inventory_size(self):
        """ Gets the number of items in the inventory.
        """

        return self.n
    
    def set_inventory_size(self, n):
        """ Sets the number of items in the inventory.
        """

        self.n = n

    # =================================
    # Methods
    # =================================

    def add_inventory_item(self, id, properties={}):
        """ Adds a new item to the inventory (q).
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        inventory = self.get_inventory_dict()
        n = self.get_inventory_size()
        if not (id in inventory.keys()):
            new_inventory_item = InventoryItem(id, n)
            new_inventory_item.set_properties(properties)
            inventory[id] = new_inventory_item
            self.set_inventory_size(n+1)

# =================================
# INVENTORY ITEM CLASS
# =================================

class InventoryItem():

    def __init__(self, flow_id, row):
        self.name = None
        self.flow_id = flow_id
        self.row = row
        self.qty = 0.0
        self.unit = None
        self.unit_process_id = None

    def get_row_num(self):
        """ Get row number of the inventory item in the process matrix basis.
        """

        return self.row
    
    def get_qty(self):
        """ Get amount of the inventory item.
        """

        return self.qty

    def get_unit(self):
        """ Get unit corresponding to the amount of the inventory item.
        """

        return self.unit
    
    
    def set_properties(self, properties={}):
        """ Set propertise of the inventory item.
        """
        
        if 'name' in properties:
            self.name = properties['name']
        
        if 'qty' in properties:
            self.qty = properties['qty']
        
        if 'unit' in properties:
            self.unit = properties['unit']

        if 'unit_process_id' in properties:
            self.unit_process_id = properties['unit_process_id']           
