
from lca_modules.impacts.impacts import Impacts

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
    unit : Unit Obj
        Unit of measurement corresponding to the quantity of the product/process.
    is_hotspot : bool
        True, if the object is a hotspot in the model.
    datasets : dict.
        Datasets corresponding to attributes: {attr (str): Dataset Obj}.
    distributions : dict.
        Distributions Datasets corresponding to attributes: {attr (str): Distribution Obj}.
    """

    def __init__(self):
        self.id = None
        self.model = None
        self.name = None
        self.life_cycle_stage = None
        self.impacts = Impacts.from_parent(self)
        self.database_item = None
        self.qty = 0.0
        self.unit = None
        self.is_hotspot = False
        self.datasets = {}
        self.distributions = {}

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, id, name, model, stage, qty, unit, impacts_from):
        """ Create a new item in a model.
        
        Parameters
        ----------
        id : int.
            An identification number.
        name : str
            Name of the item.
        model : Model Obj.
            Model in which the item is created.
        stage : str
            LCA stage.
        qty : float
            Quantity of the item
        unit : Unit Obj
            Unit corresponding to the quantity.
        impacts_from : str
            Name of the impact database entry from which to use impacts.
        """

        item = cls()

        item.set_id(id)
        item.set_name(name)
        item.set_model(model)
        item.set_life_cycle_stage(stage)
        item.set_qty(qty)
        item.set_unit(unit)
        item.set_impact_database_entry(impacts_from)

        return item

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

    # ================================
    # Setters
    # ================================
    def set_id(self, id:int):
        """ Set the product/process id.
        
            Parameters
            ----------
            id : float
                Item identification number.
        """

        self.id = id

        return self

    def set_model(self, model):
        """ Set the model corresponding to the product/process.

            Parameters
            ----------
            model : Model Obj.
                Model corresponding to the product/process.

        """

        self.model = model

        return self

    def set_life_cycle_stage(self, stage):
        """ Set life cycle stage of the product/process.

            Notes
            -----
            This method will just change the life cycle stage, without any knock-on effects.
            To have the relevant knock on effects, use 'update_life_cycle_stage' method
        """

        if self.get_life_cycle_stage() is None:
            self.life_cycle_stage = stage
        else:
            previous_stage = self.get_life_cycle_stage()
            self.set_life_cycle_stage(stage)
            
            impact_obj = self.get_impacts()
            parent_impacts_list = self.get_project().get_current_model().impacts[previous_stage]
            for impact in parent_impacts_list:
                if impact == impact_obj:
                    parent_impacts_list.remove(impact_obj)
                    break

            self.get_project().get_current_model().impacts[stage].append(impact_obj)

        return self

    def set_name(self, name):
        """ Set name of the product/process.
        
            Parameters
            ----------
            name : str
                Name of the product/process.
        """

        self.name = name

        return self

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
            self.database_item = database_item
            self.update_impacts()
        except ImportError as e:
            self.database_item = original_database_item
            raise e
        
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

        return self

    def set_unit(self, unit):
        """ Set unit of measurement for the product/process.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_qty()
            unit_in = self.get_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self

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

    # ================================
    # Getters
    # ================================
    def get_id(self):
        """ Retrieve the identification number of the product/process.

            Returns
            -------
            int
                Identification number of the product/process.

        """

        return self.id

    def get_model(self):
        """ Retrieve the model corresponding to the product/process.

            Returns
            -------
            Model Obj.
                Model corresponding to the product/process.

        """

        return self.model
        
    def get_name(self):
        """ Retrieve the name of the product/process.

            Returns
            -------
            str
                Name of the product/process.

        """

        return self.name

    def get_life_cycle_stage(self):
        """ Retrieve the life cycle stage corresponding to the product/process.

            Returns
            -------
            str
                Corresponding life cycle stage.

        """

        return self.life_cycle_stage

    def get_impact_database_entry(self):
        """ Retrieve the impact database row corresponding to the product/process.

            Returns
            -------
            str
                Flow name corresponding to the database entry which gives the unit impact of the product.

        """

        return self.database_item

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

    def get_project(self):
        """ Retrieve the corresponding project.

            Returns
            -------
            Project Obj.
                Corresponding project.

        """

        return self.get_model().get_project() 
    
    # ================================
    # Methods
    # ================================
    def update_impacts(self):
        """ Sets impacts quantities, based on database item asigned to the product/process 
            and the product/process quantity.
            If no database entry is asigned, impacts are not updated.

            Raises
            ------
            ImportError : Incompatible units of Master object and database entry.
        """

        if self.database_item:
            unit_impacts = self.get_project().get_database().get_data_entry(self.database_item)
            conversion_factor = self.get_unit().get_conversion_factor(unit_impacts["Unit"])

            if conversion_factor is None:
                raise ImportError(f"{self.get_name()} (of units {self.get_unit()}) and the LCA data chosen ({self.database_item} of units {unit_impacts['Unit']}) are of incompatible units.")
            
            impacts = {key: unit_impacts[key] * conversion_factor * self.qty for key in unit_impacts[2:].index}

            self.impacts.update_impact_qty(impacts) 


if __name__ == '__main__':
    pass
