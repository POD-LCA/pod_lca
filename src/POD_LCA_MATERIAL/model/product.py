from POD_LCA_MATERIAL.model.impacts import Impacts

class Product:

    def __init__(self, id, name, project):
        self.id = id
        self.project = project
        self.name = name
        self.life_cycle_stage = None
        self.year = 1900
        self.impacts = Impacts(self)
        self.database_row = None
        self.qty = 0.0
        self.unit = None
        self.is_material = False
        self.is_energy = False

    def update_qty(self, qty):

        self.qty = qty

        unit_impacts = self.project.database.get_impact_data()
        self.impacts.updateImpactQty(unit_impacts * self.qty) 

    def get_impacts(self):

        return self.impacts 


class Fuel(Product):

    def __init__(self, id, name, project):
        super().__init__(id, name, project)
        self.is_material = True
        self.is_energy = True


        # TODO: Further thinking needed if this should be a seperated thing