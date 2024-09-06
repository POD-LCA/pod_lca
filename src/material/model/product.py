from material.model.impacts import Impacts

class Product:

    def __init__(self, id, name, model, stage):
        self.id = id
        self.model = model
        self.name = name
        self.life_cycle_stage = stage
        self.year = 1900
        self.impacts = Impacts(self)
        self.database_item = None
        self.qty = 0.0
        self.weight = 0.0
        self.density = 1.0 # the weight of 1 unit of prodcut
        self.transporter = None
        self.unit = None
        self.is_material = False
        self.is_energy = False
    
    def __reduce__(self):
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage), {"model": self.model, "year":self.year, "impacts": self.impacts,
                                                                                    "database_item": self.database_item, 
                                                                                    "qty": self.qty, "weight": self.weight, "transporter": self.transporter,
                                                                                    "density": self.density, "unit":self.unit, 
                                                                                    "is_material":self.is_material, "is_energy":self.is_energy})

    def __setstate__(self, state):
        self.__dict__.update(state)

    def update_qty(self, qty):
        """ Update the qty of the product.
            This will also re-set the corresponding impact quantities.
            
        Parameters:
        ----------
        qty : float
            Product quantity.
        
        """
        
        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError
            
        self.qty = qty
        self.weight = self.qty * self.density

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
        self.set_life_cycle_stage(stage)
        
        impact_obj = self.get_impacts()
        parent_impacts_list = self.get_project().get_model().impacts[previous_stage]
        for impact in parent_impacts_list:
            if impact == impact_obj:
                parent_impacts_list.remove(impact_obj)
                break

        self.get_project().get_model().impacts[stage].append(impact_obj)

    def set_life_cycle_stage(self, stage):
        """ Will just change the life cycle stage, without any knock-over effects.
        """

        self.life_cycle_stage = stage

    def set_impacts_qtys(self):
        """ Sets impacts quantities, based on database item asigned to the product and the product quantity.
            If no database entry is asigned, impacts are not updated.
            TODO: current method does not check compatibility of units. e.g. the database row could be for production of 1g whereas the product object is of units kg.
        """

        if self.database_item:
            unit_impacts = self.get_project().database.get_impact_data(self.database_item)
            conversion_factor = self.get_calculator().conversion_factor(self.get_unit(), unit_impacts["Units"])

            if conversion_factor is None:
                raise ImportError
            
            self.impacts.updateImpactQty(GWP=unit_impacts["Global warming potential (kg CO2 eq)"] *conversion_factor * self.qty,
                                         acid_pot=unit_impacts["Acidification potential (kg SO2 eq)"] *conversion_factor * self.qty,
                                         eutro_pot=unit_impacts["Eutrophication potential (kg N eq)"] *conversion_factor * self.qty,
                                         ozone_dep=unit_impacts["Ozone depletion potential (kg CFC-11 eq)"] *conversion_factor * self.qty,
                                         smog=unit_impacts["Smog potential (kg O3 eq)"] *conversion_factor * self.qty)

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

    def set_density(self, density):

        if isinstance(density, str):
            try:
                density = float(density)
            except:
                raise TypeError
    
        self.density = density
    
    def set_transporter(self, transporter):
        
        self.transporter = transporter

    def get_name(self):

        return self.name    
    
    def get_unit(self):

        return self.unit
    
    def get_qty(self):

        return self.qty

    def get_id(self):

        return self.id
    
    def get_weight(self):

        return self.weight

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
    
    def get_transporter(self):

        return self.transporter
    
    def get_calculator(self):

        return self.get_model().get_project().get_calculator()

class Fuel(Product):

    def __init__(self, id, name, project):
        super().__init__(id, name, project)
        self.is_material = True
        self.is_energy = True


        # TODO: Further thinking needed if this should be a seperated thing