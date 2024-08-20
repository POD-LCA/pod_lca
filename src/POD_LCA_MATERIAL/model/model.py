from POD_LCA_MATERIAL.model.process import Process
from POD_LCA_MATERIAL.model.product import Product

class Model:

    def __init__(self):
        self.processes = []
        self.products = []
        self.impacts = []

    def create_process(self, name, project):

        n = len(self.processes)
        process = Process(n, name, project)

        self.processes.append(process)
        self.impacts.append(process.get_impacts())

        return process
    
    def create_product(self, name, project):

        n = len(self.flows)
        product = Product(n, name, project)

        self.products.append(product)
        self.impacts.append(product.get_impacts())

        return product
