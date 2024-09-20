from material.model.process import Process, transportationProcess
from material.model.product import Product, Emission, Fuel, Waste

class Model:

    def __init__(self, project, name='default'):
        self.project = project
        self.name = name
        self.processes = [] # maybe dicts
        self.products = []
        self.impacts = {'A1':[], 'A2':[], 'A3':[]}
        
    def __reduce__(self):
        
        return (self.__class__, (None,), {"project": self.project, "processes":self.processes, 
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
    
    def create_energy(self, name, stage):
        """ Create Energy object.
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
            Energy product object created.
        """

        n = len(self.products)
        energy = Fuel(n, name, self, stage)

        self.products.append(energy)
        self.impacts[stage].append(energy.get_impacts())

        return energy
    
    def create_emission(self, name, stage):
        """ Create Emission object.
            Then, append the product object and the corresponding impact objects to its properties.
            Impact objects are kept in a dictionary based on the life cycle stage.

        Parameters:
        ----------
        name : str.
            Name of the emission product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.

        Returns:
        -------
        Product Obj.
            Emission object created.
        """

        n = len(self.products)
        emission = Emission(n, name, self, stage)

        self.products.append(emission)
        self.impacts[stage].append(emission.get_impacts())

        return emission

    def create_waste(self, name, stage):
        """ Create Waste object.
            Then, append the product object and the corresponding impact objects to its properties.
            Impact objects are kept in a dictionary based on the life cycle stage.

        Parameters:
        ----------
        name : str.
            Name of the waste product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.

        Returns:
        -------
        Product Obj.
            Waste object created.
        """

        n = len(self.products)
        waste = Waste(n, name, self, stage)

        self.products.append(waste)
        self.impacts[stage].append(waste.get_impacts())

        return waste
    
    def get_processes(self):

        return self.processes
    
    def get_products(self):

        return self.products
    
    def get_impacts(self):
        
        return self.impacts
    
    def get_project(self):

        return self.project
    
    def delete_obj(self, obj):
        """ Removes products or processes, along with the impact objects.
        """

        impact = obj.get_impacts()

        if type(obj) == Product:
            self.get_products().remove(obj)
            for process in self.get_processes():
                if type(process) is transportationProcess:
                    if obj in process.get_transported_products():
                        process.get_transported_products().remove(obj)
                        process.set_travel_weight()
        elif type(obj) == Process:
            self.get_processes().remove(obj)

        impacts = self.get_impacts()
        for stage in impacts:
            if impact in impacts[stage]:
                self.get_impacts()[stage].remove(impact)
                break
