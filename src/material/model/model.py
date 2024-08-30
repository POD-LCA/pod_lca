from material.model.process import Process, transportationProcess
from material.model.product import Product

class Model:

    def __init__(self, project):
        self.project = project
        self.processes = [] # maybe dicts
        self.products = []
        self.impacts = {'A1':[], 'A2':[], 'A3':[]}
        
    def __reduce__(self):
        
        return (self.__class__, (None), {"project": self.project, "processes":self.processes, 
                                         "products": self.products, "impacts": self.impacts})
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def create_process(self, name, stage):
        """ Create process object.
            Then, append the process object and the corresponding impact objects to its properties.
            Impact objects are kept in a dictionary based on the life cycle stage.

        Parameters:
        ----------
        name : str.
            Name of the process.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.

        Returns:
        -------
        Process Obj.
            Process object created.
        """

        n = len(self.processes)
        process = Process(n, name, self, stage)

        self.processes.append(process)
        self.impacts[stage].append(process.get_impacts())

        return process
    
    def create_transportation_process(self, name:str, stage:str):
        """ Create process object.
            Then, append the process object and the corresponding impact objects to its properties.
            Impact objects are kept in a dictionary based on the life cycle stage.

        Parameters:
        ----------
        name : str.
            Name of the process.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.

        Returns:
        -------
        Process Obj.
            Process object created.
        """

        n = len(self.processes)
        process = transportationProcess(n, name, self, stage)

        self.processes.append(process)
        self.impacts[stage].append(process.get_impacts())

        return process
    
    def create_product(self, name, stage):
        """ Create product object.
            Then, append the product object and the corresponding impact objects to its properties.
            Impact objects are kept in a dictionary based on the life cycle stage.

        Parameters:
        ----------
        name : str.
            Name of the product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.

        Returns:
        -------
        Product Obj.
            Product object created.
        """

        n = len(self.products)
        product = Product(n, name, self, stage)

        self.products.append(product)
        self.impacts[stage].append(product.get_impacts())

        return product
    
    def get_processes(self):

        return self.processes
    
    def get_products(self):

        return self.products
    
    def get_impacts(self):
        
        return self.impacts
    
    def get_project(self):

        return self.project
