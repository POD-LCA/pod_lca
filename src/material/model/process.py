from material.model.impacts import Impacts

class Process:

    def __init__(self, id, name, model, stage):
        self.id = id
        self.model = model
        self.name = name
        self.life_cycle_stage = stage
        self.year = 1900
        self.impacts = Impacts(self)
        self.database_item = None
        self.qty = 0.0
        self.unit = None

    def update_qty(self, qty):
        """ Update the qty of the process.
            This will also re-set the corresponding impact quantities.
            
        Parameters:
        ----------
        qty : float
            Production quantity.
        
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError
    
        self.qty = qty
        
        self.set_impacts_qtys()

    def update_life_cycle_stage(self, stage):
        """ Update the life cycle stage of the product.
            This will also move the corresponding impact object to the relvant dictionary in the model object.
            
        Parameters:
        ----------
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.
        """

        previous_stage = self.get_life_cycle_stage()
        self.life_cycle_stage = stage
        
        impact_obj = self.get_impacts()
        parent_impacts_list = self.get_project().get_model().impacts[previous_stage]
        for impact in parent_impacts_list:
            if impact == impact_obj:
                parent_impacts_list.remove(impact_obj)
                break

        self.get_project().get_model().impacts[stage].append(impact_obj)

    def set_impacts_qtys(self):
        """ Sets impacts quantities, based on database item asigned to the product and the product quantity.
            If no database entry is asigned, impacts are not updated.
            TODO: current method does not check compatibility of units. e.g. the database row could be for production of 1g whereas the product object is of units kg.
        """

        if self.database_item:
            unit_impacts = self.get_project().get_database().get_impact_data(self.database_item)
            if self.unit == unit_impacts["Units"]:
                pass
            
            self.impacts.updateImpactQty(GWP=unit_impacts["Global warming potential (kg CO2 eq)"] * self.qty,
                                         acid_pot=unit_impacts["Acidification potential (kg SO2 eq)"] * self.qty,
                                         eutro_pot=unit_impacts["Eutrophication potential (kg N eq)"] * self.qty,
                                         ozone_dep=unit_impacts["Ozone depletion potential (kg CFC-11 eq)"] * self.qty,
                                         smog=unit_impacts["Smog potential (kg O3 eq)"] * self.qty)


    def set_database_row(self, database_item):
        """ Sets the database (impacts) entry corresponding to the product.
            This method will also update the corresponding impact quanitities.
        
        Parameters:
        ----------
        database_item : str.
            The name of the database item which gives the product impacts.
        """

        self.database_item = database_item
        self.set_impacts_qtys()

    def set_unit(self, unit):

        self.unit = unit

    def get_impacts(self):

        return self.impacts

    def get_life_cycle_stage(self):

        return self.life_cycle_stage
    
    def get_model(self):

        return self.model

    def get_project(self):

        return self.get_model().get_project()  
    
    def get_database_row(self):

        return self.database_item

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
