from material.model.impacts import Impacts
from material.model.product import Product

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

    def __reduce__(self):
        
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage,), {"model": self.model, "year":self.year, 
                                                                                     "impacts": self.impacts, 
                                                                                     "database_item": self.database_item, 
                                                                                     "qty": self.qty, "unit":self.unit})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def overide_id(self, new_id):

        self.id = new_id

    def update_qty(self, qty:float):
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

    def update_life_cycle_stage(self, stage:str):
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
            unit_impacts = self.get_project().get_database().get_impact_data(self.database_item)
            conversion_factor = self.get_calculator().conversion_factor(self.get_unit(), unit_impacts["Units"])

            if conversion_factor is None:
                if not((type(self) is transportationProcess) and (len(self.get_transported_products()) == 0)):
                    raise ImportError
            else:
                self.impacts.updateImpactQty(GWP=unit_impacts["Global warming potential (kg CO2 eq)"] * self.qty,
                                            acid_pot=unit_impacts["Acidification potential (kg SO2 eq)"] * self.qty,
                                            eutro_pot=unit_impacts["Eutrophication potential (kg N eq)"] * self.qty,
                                            ozone_dep=unit_impacts["Ozone depletion potential (kg CFC-11 eq)"] * self.qty,
                                            smog=unit_impacts["Smog potential (kg O3 eq)"] * self.qty)

    def set_database_row(self, database_item:str):
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

    def get_name(self):

        return self.name

    def get_id(self):

        return self.id
    
    def get_qty(self):

        return self.qty
    
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

    def get_unit(self):

        return self.unit
    
    def get_calculator(self):

        return self.get_model().get_project().get_calculator()
    
class transportationProcess(Process):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.transported_distance = 0.0
        self.transported_weight = 0.0
        self.transported_distance_unit = None
        self.transported_weight_unit = None
        self.transported_products = []

    def __reduce__(self):
        
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage,), {"model": self.model, "year":self.year, 
                                                                                     "impacts": self.impacts, 
                                                                                     "database_item": self.database_item, 
                                                                                     "qty": self.qty, "unit":self.unit,
                                                                                     "transported_distance": self.transported_distance,
                                                                                     "transported_weight": self.transported_weight,
                                                                                     "transported_products": self.transported_products,
                                                                                     "transported_distance_unit": self.transported_distance_unit,
                                                                                     "transported_weight_unit": self.transported_weight_unit})
    
    def get_transported_distance(self):

        return self.transported_distance
    
    def get_transported_weight(self):

        return self.transported_weight
    
    def get_transported_distance_unit(self):
        
        return self.transported_distance_unit
    
    def get_transported_weight_unit(self):

        return self.transported_weight_unit
    
    def get_transported_products(self):

        return self.transported_products

    def set_transported_distance(self, qty):

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError

        self.transported_distance = qty

        self.update_qty(self.transported_distance * self.get_transported_weight())

    def set_travel_weight(self):

        weight = 0.0
        products = self.get_transported_products()
        for product in products:
            weight_added = product.get_weight()
            weight_conversion = self.get_calculator().conversion_factor(product.get_unit(), self.get_transported_weight_unit())
            weight += (weight_added * weight_conversion)
        
        self.transported_weight = weight

        self.update_qty(self.transported_distance * self.transported_weight)

    def set_transported_distance_unit(self, unit):
        
        self.transported_distance_unit = unit
    
    def set_transported_weight_unit(self, unit):

        self.transported_weight_unit = unit

    def set_unit(self):

        self.unit = self.get_transported_weight_unit() + self.get_transported_distance_unit()
    
    def set_transported_products(self, products):

        if len(self.get_transported_products()) == 0:
            weight_unit = products[0].get_unit() if isinstance(products, list) else products.get_unit()
            self.set_transported_weight_unit(weight_unit)
            self.set_unit()
    
        if isinstance(products, list):
            self.get_transported_products().extend(products)
        else:
            self.get_transported_products().append(products)
        
        self.set_travel_weight()

    def remove_transported_product(self, item):

        products = self.get_transported_products()
        try:
            products.remove(item)
        except:
            pass # item not in list

        self.set_travel_weight()

    


