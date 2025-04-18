from utilities.units.common_units import KILOGRAM

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class CarbonStorage:
    """
    Carbon storage record of a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this record belong.
    biogenic_carbon_qty : float
        Quantity of biogenic carbon
    biogenic_carbon_unit : Unit Obj.
        Units of biogenic carbon
    mineral_carbon_qty : float
        Quantity of mineral carbon
    mineral_carbon_unit : Unit Obj.
        Units of mineral carbon    

    """
    def __init__(self):
        self.parent = None
        self.biogenic_carbon_qty = 0.0
        self.biogenic_carbon_unit = KILOGRAM
        self.mineral_carbon_qty = 0.0
        self.mineral_carbon_unit = KILOGRAM

    def __str__(self):
        str = "="*75 + "\n" + f"Carbon Storage record of {self.get_parent().get_name()}\n" + "="*75 + "\n"
        str += f"biogenic carbon: {self.get_biogenic_carbon_qty()} {self.get_biogenic_carbon_unit().get_standard_notation()}\n"
        str += f"mineral carbon: {self.get_mineral_carbon_qty()} {self.get_mineral_carbon_unit().get_standard_notation()}"
        
        return str 
 
    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_parent(cls, parent):
        """ Create carbon storage record.
        
            Parameters
            ----------
            parent : Master Obj.
                The product or process object to which this record belong.

        """
        
        record = cls()

        record.set_parent(parent)

        return record

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent of the carbon storage record.

            Parameters
            ----------
            parent : Master Obj.
                The product or process object to which this record belong.        
        """
        self.parent = parent

        return parent

    def set_biogenic_carbon_qty(self, qty:float):
        """ Update the qty of the biogenic carbon.
            
            Parameters
            ----------
            qty : float
                Biogenic carbon quantity.
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Qunatity should be a number.")
    
        self.biogenic_carbon_qty = qty

        return self        

    def set_biogenic_carbon_unit(self, unit):
        """ Set unit of measurement for biogenic carbon.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_biogenic_carbon_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_biogenic_carbon_qty()
            unit_in = self.get_biogenic_carbon_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_biogenic_carbon_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self
    
    def set_mineral_carbon_qty(self, qty:float):
        """ Update the qty of the mineral carbon.
            
            Parameters
            ----------
            qty : float
                Mineral carbon quantity.
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Qunatity should be a number.")
    
        self.mineral_carbon_qty = qty

        return self  

    def set_mineral_carbon_unit(self, unit):
        """ Set unit of measurement for minearal carbon.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_mineral_carbon_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_mineral_carbon_qty()
            unit_in = self.get_mineral_carbon_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_mineral_carbon_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self, parent):
        """ Get the parent of the carbon storage record.

            Returns
            -------
            Master Obj.
                The product or process object to which this record belong.        
        """
        return self.parent

    def get_biogenic_carbon_qty(self):
        """ Get the qty of the biogenic carbon.
            
            Returns
            -------
            float
                Biogenic carbon quantity.
        """
        return self.biogenic_carbon_qty

    def get_biogenic_carbon_unit(self):
        """ Get unit of measurement for biogenic carbon.
        
            Returns
            -------
            Unit Obj.
                Unit of measurement.
        """
        return self.biogenic_carbon_unit

    def get_mineral_carbon_qty(self):
        """ Get the qty of the mineral carbon.
            
            Returns
            -------
            float
                Mineral carbon quantity.
        """
        return self.mineral_carbon_qty

    def get_mineral_carbon_unit(self):
        """ Get unit of measurement for mineral carbon.
        
            Returns
            -------
            Unit Obj.
                Unit of measurement.
        """
        return self.mineral_carbon_unit
    
class Emissions:
    """
    Emissions record of a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this record belong.
    CO2_qty : float
        Quantity of carbon dioxide emissions.
    CO2_unit : Unit Obj.
        Units of carbon dioxide emissions.
    N2O_qty : float
        Quantity of nitrous oxide emissions.
    N2O_unit : Unit Obj.
        Units of nitrous oxide emissions.
    CH4_qty : float
        Quantity of methane emissions.
    CH$_unit : Unit Obj.
        Units of methane emissions.    

    """
    def __init__(self):
        self.parent = None
        self.CO2_qty = 0.0
        self.CO2__unit = KILOGRAM
        self.N2O_qty = 0.0
        self.N2O_unit = KILOGRAM    
        self.CH4_qty = 0.0
        self.CH4_unit = KILOGRAM 

    def __str__(self):
        str = "="*75 + "\n" + f"Emissions record of {self.get_parent().get_name()}\n" + "="*75 + "\n"
        str += f"Carbon dioxide (CO2): {self.get_CO2_qty()} {self.get_CO2_unit().get_standard_notation()}\n"
        str += f"Nitrous oxide (N2O): {self.get_N2O_qty()} {self.get_N2O_unit().get_standard_notation()}\n"
        str += f"Methane (CH4): {self.get_CH4_qty()} {self.get_CH4_unit().get_standard_notation()}\n"
        
        return str 

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_parent(cls, parent):
        """ Create emissions record.
        
            Parameters
            ----------
            parent : Master Obj.
                The product or process object to which this record belong.

        """
        
        record = cls()

        record.set_parent(parent)

        return record
    
    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent of the carbon storage record.

            Parameters
            ----------
            parent : Master Obj.
                The product or process object to which this record belong.        
        """
        self.parent = parent

        return parent

    def set_CO2_qty(self, qty:float):
        """ Update the qty of carbon dioxide emissions.
            
            Parameters
            ----------
            qty : float
                Carbon dioxide emissions quantity.
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Qunatity should be a number.")
    
        self.CO2_qty = qty

        return self        

    def set_CO2_unit(self, unit):
        """ Set unit of measurement for carbon dioxide emissions.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_CO2_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_CO2_qty()
            unit_in = self.get_CO2_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_CO2_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self

    def set_N2O_qty(self, qty:float):
        """ Update the qty of nitrous oxide emissions.
            
            Parameters
            ----------
            qty : float
                Nitrous oxide emissions quantity.
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Qunatity should be a number.")
    
        self.N2O_qty = qty

        return self        

    def set_N2O_unit(self, unit):
        """ Set unit of measurement for nitrous oxide emissions.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_N2O_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_N2O_qty()
            unit_in = self.get_N2O_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_N2O_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self  

    def set_CH4_qty(self, qty:float):
        """ Update the qty of methane emissions.
            
            Parameters
            ----------
            qty : float
                Methane emissions quantity.
        """

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError("Qunatity should be a number.")
    
        self.CH4_qty = qty

        return self        

    def set_CH4_unit(self, unit):
        """ Set unit of measurement for methane emissions.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_CH4_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_CH4_qty()
            unit_in = self.get_CH4_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_CH4_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self  

    # ================================
    # Getters
    # ================================
    def get_parent(self, parent):
        """ Get the parent of the emissions record.

            Returns
            -------
            Master Obj.
                The product or process object to which this record belong.        
        """
        return self.parent

    def get_CO2_qty(self):
        """ Get the qty of the carbon dioxide emissions.
            
            Returns
            -------
            float
                Carbon dioxide emissions quantity.
        """
        return self.CO2_qty

    def get_CO2_unit(self):
        """ Get unit of measurement for carbon dioxide emissions.
        
            Returns
            -------
            Unit Obj.
                Unit of measurement.
        """
        return self.biogenic_carbon_unit

    def get_N2O_qty(self):
        """ Get the qty of the nitrous oxide emissions.
            
            Returns
            -------
            float
                Nitrous oxide emissions quantity.
        """
        return self.N2O_qty

    def get_N2O_unit(self):
        """ Get unit of measurement for nitrous oxide emissions.
        
            Returns
            -------
            Unit Obj.
                Unit of measurement.
        """
        return self.N2O_unit

    def get_CH4_qty(self):
        """ Get the qty of the methane emissions.
            
            Returns
            -------
            float
                Methane emissions quantity.
        """
        return self.CH4_qty

    def get_CH4_unit(self):
        """ Get unit of measurement for methane emissions.
        
            Returns
            -------
            Unit Obj.
                Unit of measurement.
        """
        return self.CH4_unit  

if __name__ == '__main__':
    pass
