
from material.model.impacts import Impacts

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Master:
    """
    Master object from which product and process objects inherit.

    Attributes
    ----------
    id : int.
        An identification number.
    model : Model Obj.
        Model object to which this product/process belong.
    name : str
        Name of the product/process.
    life_cycle_stage : str
        Life cycle stage corresponding to the product/process.
    impacts : Impacts Obj.
        Impacts object corresponding to the product/process.
    database_item : str
        Flow name corresponding to the database entry which gives the unit impact of the product.
    qty : float
        Quantity of the product/process.
    unit : str
        Unit of measurement corresponding to the quantity of the product/process.
    
    """

    def __init__(self, id, name, model, stage):
        self.id = id
        self.model = model
        self.name = name
        self.life_cycle_stage = stage
        self.impacts = Impacts(self) if model is not None else None
        self.database_item = None
        self.qty = 0.0
        self.unit = None


    def __reduce__(self):
        
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage,), {"model": self.model, 
                                                                                     "impacts": self.impacts, 
                                                                                     "database_item": self.database_item, 
                                                                                     "qty": self.qty, "unit":self.unit})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def overide_id(self, new_id:int):
        """ Replace the product/process id by new number.
        
            Parameters
            ----------
            new_id : float
                New identification number.
        """

        self.id = new_id

    def update_life_cycle_stage(self, stage:str):
        """ Update the life cycle stage of the item.
            This will also move the corresponding Impacts object to the relvant dictionary in the Model object.
            
            Parameters
            ----------
            stage : str.
                Life cycle stage.
        """

        previous_stage = self.get_life_cycle_stage()
        self.set_life_cycle_stage(stage)
        
        impact_obj = self.get_impacts()
        parent_impacts_list = self.get_project().get_current_model().impacts[previous_stage]
        for impact in parent_impacts_list:
            if impact == impact_obj:
                parent_impacts_list.remove(impact_obj)
                break

        self.get_project().get_current_model().impacts[stage].append(impact_obj)

    def update_qty(self, qty:float):
        """ Update the qty of the item.
            This will also re-calculate the corresponding impact quantities.
            
            Parameters
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

    def set_impacts_qtys(self):
        """ Sets impacts quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

            Raises
            ------
            ImportError : Incompatible units of Master object and database entry.
        """

        if self.database_item:
            unit_impacts = self.get_project().database.get_impact_data(self.database_item)
            conversion_factor = self.get_calculator().conversion_factor(self.get_unit(), unit_impacts["Unit"])

            if conversion_factor is None:
                raise ImportError(f"{self.get_name()}-(of units {self.get_unit()}) and its LCA data ({self.database_item}) have incompatible units.")
            
            impacts = {key: unit_impacts[key] * conversion_factor * self.qty for key in unit_impacts[2:].index}

            self.impacts.updateImpactQty(impacts)

    def set_impact_database_entry(self, database_item:str):
        """ Sets the database (impacts) entry corresponding to the item.
            This method will also update the corresponding impact quanitities.
        
            Parameters
            ----------
            database_item : str.
                The name of the database item which gives the item impacts.
        """

        self.database_item = database_item
        self.set_impacts_qtys()

    def set_unit(self, unit):
        """ Set unit of measurement for the product/process.
        
            Parameters
            ----------
            unit : str
                Unit of measurement.
        """

        self.unit = unit

    def set_name(self, name):
        """ Set name of the product/process.
        
            Parameters
            ----------
            name : str
                Name of the product/process.
        """

        self.name = name

    def set_life_cycle_stage(self, stage):
        """ Set life cycle stage of the product/process.

            Notes
            -----
            This method will just change the life cycle stage, without any knock-on effects.
            To have the relevant knock on effects, use 'update_life_cycle_stage' method
        """

        self.life_cycle_stage = stage

    def get_name(self):
        """ Retrieve the name of the product/process.

            Returns
            -------
            str
                Name of the product/process.

        """

        return self.name

    def get_id(self):
        """ Retrieve the identification number of the product/process.

            Returns
            -------
            int
                Identification number of the product/process.

        """

        return self.id
    
    def get_qty(self):
        """ Retrieve the quantity of the product/process.

            Returns
            -------
            float
                Quantity of the product/process.

        """

        return self.qty
    
    def get_unit(self):
        """ Retrieve the unit of measurement of the product/process.

            Returns
            -------
            str
                Unit of measurement of the product/process.

        """

        return self.unit
    
    def get_impacts(self):
        """ Retrieve the impacts of the product/process.

            Returns
            -------
            Impacts Obj.
                Impacts of the product/process.

        """

        return self.impacts

    def get_life_cycle_stage(self):
        """ Retrieve the life cycle stage corresponding to the product/process.

            Returns
            -------
            str
                Corresponding life cycle stage.

        """

        return self.life_cycle_stage
    
    def get_model(self):
        """ Retrieve the model corresponding to the product/process.

            Returns
            -------
            Model Obj.
                Model corresponding to the product/process.

        """

        return self.model

    def get_project(self):
        """ Retrieve the corresponding project.

            Returns
            -------
            Project Obj.
                Corresponding project.

        """

        return self.get_model().get_project()  
    
    def get_database_row(self):
        """ Retrieve the impact database row corresponding to the product/process.

            Returns
            -------
            str
                Flow name corresponding to the database entry which gives the unit impact of the product.

        """

        return self.database_item

    def get_calculator(self):
        """ Retrieve the corresponding calculator.

            Returns
            -------
            Calculator Obj.
                Corresponding calculator.

        """

        return self.get_model().get_project().get_calculator()

if __name__ == '__main__':
    pass
