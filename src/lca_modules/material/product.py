
from lca_modules.material.master import Master

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

    def __init__(self):
        super().__init__()
        self.weight = 0.0
        self.weight_unit = None
        self.density = 1.0 # the weight of 1 unit of prodcut
        self.transporter = None
        self.is_material = True

    def __str__(self):
        return f"Product(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

    # ================================
    # Setters
    # ================================
    def set_qty(self, qty):
        """ Update the qty of the product.
            This will also re-calculate the corresponding impact quantities.
            
            Parameters
            ----------
            qty : float
                Product quantity.
        
        """
        
        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Quantity should be a numeric entry.")
            
        self.qty = qty
        self.weight = self.qty * self.density

        self.update_impacts()

        return self

    def set_unit(self, unit):
        """ Set unit of measurement for the product.
            If the unit of measurement is of mass dimensions, same unit is set as weight unit of the product.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        
        """

        self.unit = unit
        if unit.get_qty_measured() == 'mass':
            self.set_weight_unit(unit)
            self.density = 1.0

        return self

    def set_weight_unit(self, unit):
        """ Set unit of measurement for the mass of the product.

            Parameters
            ----------
            str
                Unit of measurement of mass.
        
        """

        self.weight_unit = unit

        return self

    def set_density(self, density):
        """ Set density of the product.
            Density is defined here as mass per unit measurement of product (not necessarily volume)
        
            Parameters
            ----------
            density : float
                Denisty of product (mass per unit mesurement of product).

            Raises
            ------
            TypeError
                Density must be a numerical value.

        """

        if isinstance(density, str):
            try:
                density = float(density)
            except:
                raise TypeError(f"Density of {self.get_name()} should be a numerical value.")
    
        self.density = density

        return self

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
            transporter.set_transported_product(self)

        return self

    # ================================
    # Getters
    # ================================      
    def get_weight(self):
        """ Retrieve the mass of the product.
        
            Returns
            -------
            str
                Mass of the product.
        """

        return self.weight

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
       
    def get_transporter(self):
        """ Retrieve transport processes the product is subject to, if any.

            Returns
            -------
            TransportationProcess Obj.
                Transportation process the product is subject to, if any.
                None, otherwise.
        """

        return self.transporter


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

    def __init__(self):
        super().__init__()
        self.is_material = True
        self.is_energy = True

    def __str__(self):
        return f"Fuel(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

class Emission(Product):
    """
    Emission product object, inheriting from the product object.

    Attributes
    ----------
    is_emission : bool
        True
        
    """

    def __init__(self):
        super().__init__()
        self.is_emssion = True

    def __str__(self):
        return f"Emission(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

class Waste(Product):
    """
    Waste product object, inheriting from the product object.

    Attributes
    ----------
    is_waste : bool
        True
        
    """

    def __init__(self):
        super().__init__()
        self.is_waste = True

    def __str__(self):
        return f"Waste(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"


if __name__ == '__main__':
    pass
