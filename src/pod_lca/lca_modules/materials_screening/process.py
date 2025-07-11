
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Master
from ..impacts import CarbonStorage
from ..impacts import Emissions
from ..impacts import Impacts
from ...units import KILOGRAM


class Process(Master):
    """ Process object, inheriting from the Master object, represent a process.

    Attributes
    ----------
    inputs : list of Master Obj.
        Input products and processes.
    """

    def __init__(self):
        super().__init__()
        self.inputs = []

    def __str__(self):
        return f"Process(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"
    

class TransportationProcess(Process):
    """ Transportation Process object, inheriting from the Process object, represent a transportation process.

    Attributes
    ----------
    transported_distance : float
        Distance traveled in the transportation process.
    transported_weight : float
        Mass transported in the transportation process.
    transported_distance_unit : Unit Obj.
        Unit of measurement of the distance travelled.
    transported_weight_unit : Unit Obj.
        Unit of measurement of the transported mass.
    transported_products : list of Product Obj.
        Products transported in the transportation process.
    """

    def __init__(self):
        super().__init__()
        self.transported_distance = 0.0
        self.transported_weight = 0.0
        self.transported_distance_unit = None
        self.transported_weight_unit = KILOGRAM  # default unit
        self.transported_products = []
        
    def __str__(self):
            return f"Transpportation Process(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, id, name, model, stage, transported_distance, unit, impacts_from):
        """ Create process in a model.
        
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
        item.set_transported_distance(transported_distance)
        item.set_transported_distance_unit(unit)
        item.impacts = Impacts.from_parent(item)
        item.emissions = Emissions.from_parent(item)
        item.carbon_storage = CarbonStorage.from_parent(item)
        item.unit_impacts = Impacts.from_parent(item)
        item.unit_emissions = Emissions.from_parent(item)
        item.unit_carbon_storage = CarbonStorage.from_parent(item)
        item.set_impact_database_entry(impacts_from)
        item.add_inventory_records_to_model()

        return item
    
    # ================================
    # Setters
    # ================================
    def set_unit(self):
        """ Set unit of measurement for the transportation process.
            The unit of measurement has dimensions of mass x distance.
        """
        if self.get_transported_distance_unit() is not None:
            self.unit = self.get_transported_weight_unit() * self.get_transported_distance_unit()

    def set_transported_distance(self, qty):
        """ Update the distance travelled in the transportation process.
            This will update the process quantity of transportation (in mass x distance).

        Parameters
        ----------
        qty : float
            Distance traveled in the transportation process.
        """
        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError

        self.transported_distance = qty

        self.set_qty(self.transported_distance * self.get_transported_weight())

    def set_transported_weight(self):
        """ Update the mass transported in the transportation process.
            This wil obtain the mass from corresponding products transported.
            The units of mass need not be consistent as the method converts units.
            This will also update the process quantity of transportation (in mass x distance).
        """
        weight = 0.0
        products = self.get_transported_products()
        for product in products:
            weight_added = product.get_weight()
            weight_conversion_factor = product.get_weight_unit().get_conversion_factor(self.get_transported_weight_unit())
            weight += (weight_added * weight_conversion_factor)
        
        self.transported_weight = weight

        self.set_qty(self.transported_distance * self.transported_weight)

    def set_transported_distance_unit(self, unit):
        """ Set unit of measurement for travel distance of the transportation process.
            This will also update the process quantity of transportation (in mass x distance).
        
        Parameters
        ----------
        unit : str
            Unit of measurement.
        """
        self.transported_distance_unit = unit
        self.set_unit()
    
    def set_transported_weight_unit(self, unit):
        """ Set unit of measurement for mass transported.
            This will also update the process quantity of transportation (in mass x distance).
        
        Parameters
        ----------
        unit : str
            Unit of measurement.
        """
        self.transported_weight_unit = unit
        self.set_unit()

    def set_transported_products(self, products):
        """ Set prodcuts transported in the transportation process.
            Will add each product in turn calling 'set_transported_product'.
        
        Parameters
        ----------
        products : list of Product Obj.
            Products transported in the transportation process.
        """
        for product in products:
            self.set_transported_product(product)
        
    def set_transported_product(self, product):
        """ Set prodcuts transported in the transportation process.
            If there are no products currently tranported in this process, the unit of measurement of mass
            of the transportation process will be set to that of the product added.
            If not already added, will set the transportation process to the product as its transporter.

        Note
        -----
        This method is equivalent to calling 'set_transporter' from the Product Object.
    
        Parameters
        ----------
        product : Product Obj.
            Product transported in the transportation process.
        """
        if len(self.get_transported_products()) == 0:
            weight_unit = product.get_weight_unit()
            self.set_transported_weight_unit(weight_unit)
    
        if product not in self.get_transported_products():
            self.get_transported_products().append(product)
            if not self == product.get_transporter():
                product.set_transporter(self)

        self.set_transported_weight()

    # ================================
    # Getters
    # ================================       
    def get_transported_distance(self):
        """ Retrieve the distance travelled in the transportation process.

        Returns
        -------
        float
            Distance traveled in the transportation process.
        """
        return self.transported_distance
    
    def get_transported_weight(self):
        """ Retrieve the mass transported in the transportation process.

            Returns
            -------
            float
                Weight transported in the transportation process.
        """
        return self.transported_weight
    
    def get_transported_distance_unit(self):
        """ Retrieve the unit of measurement of the travel distance of the transportation process.

            Returns
            -------
            str
                Unit of measurement of the distance travelled.
        """
        return self.transported_distance_unit
    
    def get_transported_weight_unit(self):
        """ Retrieve the unit of measurement of the transported mass of the transportation process.

            Returns
            -------
            str
                Unit of measurement of the transported mass.
        """
        return self.transported_weight_unit
    
    def get_transported_products(self):
        """ Retrieve all products transported in the transportation process.

            Returns
            -------
            list of Product Obj.
                All transported products.
        """
        return self.transported_products

    # ================================
    # Methods
    # ================================
    def remove_transported_product(self, item):
        """ Remove a product from the transportation process.
            This will remove the transporter from the product as well.
            Transported mass of the transportation process is also updated.

        Parameters
        ----------
        item : Product Obj.
            Product to be removed from the transportation process.

        Raises
        ------
        Key Error : Product is not part of the transportation process.
        """
        products = self.get_transported_products()
        try:
            products.remove(item)
            item.transporter = None
        except:
            raise KeyError(f"'{item.get_name()}' is not part of the transporation process ({self.get_name()}).")

        self.set_transported_weight()


if __name__ == '__main__':
    pass
