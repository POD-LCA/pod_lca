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

    def add_process(self, unit_process_id, inventory_ids, exchange_qtys):
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
        for i in range(len(inventory_ids)):
            inventory_item = inventory.get_inventory_dict()[inventory_ids[i]]
            new_process[inventory_item.get_row_num()] = exchange_qtys[i]
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
        self.flow_ids = {}

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
    
    def get_flow_ids(self):

        return self.flow_ids
    
    def set_inventory_size(self, n):
        """ Sets the number of items in the inventory.
        """

        self.n = n

    # =================================
    # Methods
    # =================================

    def add_inventory_items(self, exchanges):

        inventory_ids, exchange_qtys = [], []
        for exchange in exchanges.keys():
            inventory_id = self.add_inventory_item(exchanges[exchange].get_flow_id(), exchanges[exchange].__dict__)
            exchange_qty = exchanges[exchange].get_qty()
            
            inventory_ids.extend([inventory_id])   
            exchange_qtys.extend([exchange_qty])

        return inventory_ids, exchange_qtys

    def add_inventory_item(self, flow_id, properties={}):
        """ Adds a new item to the inventory (q).
        
        Inputs:
        ------
        
        
        Returns:
        -------
        
        """
        
        inventory = self.get_inventory_dict()
        flow_ids = self.get_flow_ids()
        n = self.get_inventory_size()

        new = True
        if flow_id in flow_ids.keys():
            rows = flow_ids[flow_id]
            for row in rows:
                existing_product = inventory[row]
                unit_process = existing_product.get_unit_process_id()
                if properties['unit_process_id'] == unit_process:
                    new = False

        if new:
            row = n
            new_inventory_item = InventoryItem(flow_id, row)
            new_inventory_item.set_properties(properties)
            inventory[row] = new_inventory_item
            if flow_id in flow_ids.keys():
                flow_ids[flow_id].extend([row])
            else:
                flow_ids[flow_id] = [row]
            self.set_inventory_size(n+1)

        return row
        

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
        self.location = None

    def get_name(self):

        return self.name

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
    
    def get_unit_process_id(self):

        return self.unit_process_id
    
    def get_location(self):

        return self.location
    
    
    def set_properties(self, properties={}):
        """ Set propertise of the inventory item.
        """
        
        if 'name' in properties:
            self.name = properties['name']
        
        if 'unit' in properties:
            self.unit = properties['unit']

        if 'unit_process_id' in properties:
            self.unit_process_id = properties['unit_process_id']       

        if 'location' in properties:
            self.location = properties['location']      
