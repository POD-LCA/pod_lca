from POD_LCA_MATERIAL.model.impacts import Impacts

class Process:

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

    def update_qty(self, qty):

        self.qty = qty
        
        unit_impacts = self.project.database.get_impact_data()
        self.impacts.updateImpactQty(unit_impacts * self.qty)

    def get_impacts(self):

        return self.impacts   

class transportationProcess(Process):

    def __init__(self):
        super().__init__(self)
        self.transported_distance = 0.0
        self.transported_weight = 0.0

    def update_travel_distance(self, qty):

        self.transported_distance = qty

        self.update_qty(self.transported_distance * self.transported_weight)

    def update_travel_weight(self, qty):

        self.transported_weight = qty

        self.update_qty(self.transported_distance * self.transported_weight)
