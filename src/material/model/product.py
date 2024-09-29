
from material.model.master import Master

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Product(Master):
    """
    Product object, inheriting from the Master object, represent a product.

    Attributes
    ----------
    weight : float
        Mass of the product.
    weight_unit : str
        Unit of measurement of mass. Default is set as 'kg'.
    density : float
        The mass of product in weight units per unit of product's unit of measurement.
    trnasporter : TransportationProcess Obj.
        Transportation process, if the product is being transported, else None.
    is_material : bool
        True, if the product is a material.
    is_fuel : bool
        True, of the product is an energy source.

    """

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.weight = 0.0
        self.weight_unit = 'kg'
        self.density = 1.0 # the weight of 1 unit of prodcut
        self.transporter = None
        self.is_material = False
        self.is_energy = False

    def __reduce__(self):
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage), {"model": self.model, "year":self.year, "impacts": self.impacts,
                                                                                    "database_item": self.database_item, 
                                                                                    "qty": self.qty, "weight": self.weight, "transporter": self.transporter,
                                                                                    "density": self.density, "unit":self.unit, 
                                                                                    "is_material":self.is_material, "is_energy":self.is_energy})

    def update_qty(self, qty):
        """ Update the qty of the product.
            This will also re-calculate the corresponding impact quantities.
            
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

    def set_density(self, density):
        """ Set density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)
        
            Parameters
            ----------
            float
                Denisty of product (mass per unit mesurement of product).

            Raises
            ------
            TypeError : Density must be a numerical value.

        """

        if isinstance(density, str):
            try:
                density = float(density)
            except:
                raise TypeError(f"Density of {self.get_name()} should be a numerical value.")
    
        self.density = density
    
    def set_unit(self, unit):
        """ Set unit of measurement for the product.
            If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.
        
            Parameters
            ----------
            unit : str
                Unit of measurement.
        
        """

        self.unit = unit
        if self.get_calculator().is_mass_unit(unit):
            self.set_weight_unit(unit)
            self.density = 1.0

    def set_weight_unit(self, unit):
        """ Set unit of measurement for the mass of the product.

            Parameters
            ----------
            str
                Unit of measurement of mass.
        
        """

        self.weight_unit = unit
    
    def set_transporter(self, transporter):
        """ Set transport processes the product is subject to.
            If not already added, will add the product to the transportation process as a transported product.
            
            Note
            ----
            This method is equivalent to calling 'set_transported_product' from the TransportationProcess Obj.

            Parameters
            ----------
            TransportationProcess Obj.
                Transportation process the product is subject to.

        """

        self.transporter = transporter
        if self not in transporter.get_transported_products():
            transporter.set_transported_products(self)  
           
    def get_weight(self):
        """ Retrieve the mass of the product.
        
            Returns
            -------
            str
                Mass of the product.
        """

        return self.weight
    
    def get_transporter(self):
        """ Retrieve transport processes the product is subject to, if any.

            Returns
            -------
            TransportationProcess Obj.
                Transportation process the product is subject to, if any.
                None, otherwise.
        """

        return self.transporter
    
    def get_weight_unit(self):
        """ Retrieve the unit of measurement of mass of the product.
            This is used for the definition of density of the product.

            Returns
            -------
            str
                Unit of measurement of mass of the product.
        """

        return self.weight_unit
    
    def get_density(self):
        """ Retrieve density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)
        
            Returns
            -------
            float
                Denisty of product (mass per unit mesurement of product).

        """

        return self.density


class Fuel(Product):
    """
    Fuel product object, inheriting from the product object.

    Attributes
    ----------
    is_material : bool
        True
    is_energy : bool
        True

    """

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_material = True
        self.is_energy = True


class Emission(Product):
    """
    Emission product object, inheriting from the product object.

    Attributes
    ----------
    is_emission : bool
        True
        
    """

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_emssion = True


class Waste(Product):
    """
    Waste product object, inheriting from the product object.

    Attributes
    ----------
    is_waste : bool
        True
        
    """

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_waste = True

if __name__ == '__main__':
    pass
