
from lca_modules.material.impacts import Impacts

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
    impact_database_entry : str
        Flow name corresponding to the database entry which gives the unit impact of the product.
    qty : float
        Quantity of the product/process.
    unit : str
        Unit of measurement corresponding to the quantity of the product/process.
    is_hotspot : bool
        True, if the object is a hotspot in the model.
    datasets : dict.
        Datasets corresponding to attributes: {attr (str): Dataset Obj}.
    distributions : dict.
        Distributions Datasets corresponding to attributes: {attr (str): Distribution Obj}.
    """

    def __init__(self, id, name, model, stage):
        self.id = id
        self.model = model
        self.name = name
        self.life_cycle_stage = stage
        self.impacts = Impacts(self) if model is not None else None
        self.impact_database_entry = None
        self.qty = 0.0
        self.unit = None
        self.is_hotspot = False
        self.datasets = {}
        self.distributions = {}

    def __reduce__(self):
        
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage,), {"model": self.model, 
                                                                                     "impacts": self.impacts, 
                                                                                     "database_item": self.impact_database_entry, 
                                                                                     "qty": self.qty, "unit":self.unit})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return f"Object(name={self.name}, LC stage={self.life_cycle_stage})"

    def set_id(self, new_id:int):
        """ Replace the product/process id by new number.
        
            Parameters
            ----------
            new_id : float
                New identification number.
        """

        self.id = new_id

    def set_name(self, name):
        """ Set name of the product/process.
        
            Parameters
            ----------
            name : str
                Name of the product/process.
        """

        self.name = name

    def set_life_cycle_stage(self, stage:str):
        """ Update the life cycle stage of the item.
            This will also move the corresponding Impacts object to the relvant dictionary in the Model object.
            
            Parameters
            ----------
            stage : str.
                Life cycle stage.
        """

        if self.get_life_cycle_stage() is not None:
            previous_stage = self.get_life_cycle_stage()
            self.life_cycle_stage = stage
            
            impact_obj = self.get_impacts()
            parent_impacts_list = self.get_project().get_current_model().impacts[previous_stage]
            for impact in parent_impacts_list:
                if impact == impact_obj:
                    parent_impacts_list.remove(impact_obj)
                    break

            self.get_project().get_current_model().impacts[stage].append(impact_obj)
        else:
            self.life_cycle_stage = stage

    def set_qty(self, qty:float):
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
                raise TypeError("Qunatity should be a number.")
    
        self.qty = qty
        
        self.update_impacts()

    def set_unit(self, unit):

        if self.get_unit() is not None:
            value_in = self.get_qty()
            unit_in = self.get_unit()

            conversion_factor = self.get_project().get_calculator().conversion_factor(unit_in, unit)

            if conversion_factor is not None:
                self.unit = unit
                self.update_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")
        else:
            self.unit = unit


    def update_impacts(self):
        """ Sets impacts quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

            Raises
            ------
            ImportError : Incompatible units of Master object and database entry.
        """

        if self.impact_database_entry:
            unit_impacts = self.get_project().database.get_impact_data(self.impact_database_entry)
            conversion_factor = self.get_calculator().conversion_factor(self.get_unit(), unit_impacts["Unit"])

            if conversion_factor is None:
                raise ImportError(f"{self.get_name()} (of units {self.get_unit()}) and the LCA data chosen ({self.impact_database_entry} of units {unit_impacts['Unit']}) are of incompatible units.")
            
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

        original_database_item = self.get_impact_database_entry()
        try:
            self.impact_database_entry = database_item
            self.update_impacts()
        except ImportError as e:
            self.impact_database_entry = original_database_item
            raise e

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
    
    def get_impact_database_entry(self):
        """ Retrieve the impact database row corresponding to the product/process.

            Returns
            -------
            str
                Flow name corresponding to the database entry which gives the unit impact of the product.

        """

        return self.impact_database_entry

    def get_calculator(self):
        """ Retrieve the corresponding calculator.

            Returns
            -------
            Calculator Obj.
                Corresponding calculator.

        """

        return self.get_model().get_project().get_calculator()

    def get_datasets(self):
        """ Get dataset objects of the Master Obj.

            Returns
            -------
            dict.
                Datasets corresponding to attributes: {attr (str): Dataset Obj}        
        """

        return self.datasets
        
    def get_distributions(self):
        """ Get distribution objects of the Master Obj.

            Returns
            -------
            dict.
                Distributions Datasets corresponding to attributes: {attr (str): Distribution Obj}.
        """

        return self.distributions

    
    def set_dataset(self, dataset, attr):
        """ Set a dataset object to the Master Obj.

            Parameters
            ----------
            dataset : Dataset Obj.
                Dataset object to be set
            attr : str.
                Attribute to which the dataset correspond.
        """

        if hasattr(self, attr):
            self.datasets[attr] = dataset
            dataset.set_parent(self)
            dataset.set_attr(attr)
        else:
            print(f"Object {type(self)} does not have an attribute {attr}")

    def set_distribution(self, distribution, attr):
        """ Set a set_distribution object to the Master Obj.

            Parameters
            ----------
            distribution : Distribution Obj.
                Distribution object to be set
            attr : str.
                Attribute to which the distribution correspond.
        """

        if hasattr(self, attr):
            self.distributions[attr] = distribution
            distribution.set_parent(self)
            distribution.set_attr_name(attr)
        else:
            print(f"Object {type(self)} does not have an attribute {attr}")

    @classmethod
    def copy(cls, obj):
        """ Make a copy of an object.

            Returns
            -------
            Master Obj.
                Copy of the object.
        """

        new_impact = obj.get_impacts().copy()

        new_obj = cls(None, None, None, None)
        new_obj.__dict__.update(obj.__dict__)

        new_impact.parent = new_obj
        new_obj.impacts = new_impact

        return new_obj

if __name__ == '__main__':
    pass
