from utilities.units import UNIT_CONVERSIONS, ALL_PREFIXES
from utilities.objects.array_methods import get_attribute_as_list

from math import log10

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Unit:
    """
    Unit object from which units are created.

    Attributes
    ----------
    name : str.
        Common name of the unit.
    standard_notation : str.
        Standard notation of the unit.
    qty_measured : str.
        The quantity measured by the unit---e.g., 'length', 'mass', 'time'.
    base_unit : Unit Obj
        Base unit of the Obj. None if itself a base unit.
    prefix : MetricPrefix Obj.
        Metric prefix. None if a base unit or non-metric.
    convert_compound : bool
        If True, unit conversion assuming the unit to be a compound unit.
    components : List of Unit Obj.
        List of components the unit is made up of. None if not a compound unit
    """
    def __init__(self):
        self.name = None
        self.standard_notation = None
        self.qty_measured = None
        self.base_unit = None
        self.prefix = None
        self.convert_compound = False
        self.components = None

    def __str__(self):
        return f"Unit {self.get_name()} ({self.get_standard_notation()}) measuring {self.get_qty_measured()}."

    def __mul__(self, other):
        """ Multiplication of units by other units."""

        if isinstance(other, Unit):
            name = self.get_name() + '-' + other.get_name()
            standard_notation = self.get_standard_notation() + other.get_standard_notation()
            qty_measured = self.get_qty_measured() + '-' + other.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.convert_compound = True
            newUnit.components = [self, other]

            return newUnit

        elif isinstance(other, MetricPrefix):
            raise TypeError(f"Metric prefixes not defined for post multiplication.")

    def __rmul__(self, other):
        """ Reflexive multiplication of units by metric prefixes."""

        if isinstance(other, MetricPrefix):
            if self.get_base() is None:
                name = other.get_name()  + self.get_name()
                standard_notation = other.get_symbol() + self.get_standard_notation()
                qty_measured = self.get_qty_measured()

                newUnit = Unit.from_basics(name, standard_notation, qty_measured)
                newUnit.base_unit = self
                newUnit.prefix = other

                return newUnit
            else:
                new_prefix = self.get_prefix() * other

                name = new_prefix.get_name()  + self.get_base().get_name()
                standard_notation = new_prefix.get_symbol() + self.get_base().get_standard_notation()
                qty_measured = self.get_qty_measured()

                newUnit = Unit.from_basics(name, standard_notation, qty_measured)
                newUnit.base_unit = self.get_base()
                newUnit.prefix = new_prefix

                return newUnit
        else:
            raise TypeError(f"unsupported operand type(s) for *: {self.__class__.__name__} and {other.__class__.__name__}")

    def __truediv__(self, other):
        """ Devision of units by other units."""

        if isinstance(other, Unit):
            name = self.get_name() + ' per ' + other.get_name()
            standard_notation = self.get_standard_notation() + '/' + other.get_standard_notation()
            qty_measured = self.get_qty_measured() + ' per ' + other.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.convert_compound = True
            newUnit.components = [self, 1/ other]

            return newUnit

        else:
            raise TypeError(f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}")
        
    def __rtruediv__(self, other):
        """ Reflexive division of units by unit value (1)."""

        if other == 1:
            name = 'per ' + self.get_name()
            standard_notation = self.get_standard_notation() + '-1'
            qty_measured =  'per ' + self.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.base_unit = self.get_base()
            newUnit.prefix = self.get_prefix()
            newUnit.convert_compound = self.convert_compound
            newUnit.components = self.get_components()

            return newUnit
        else:
            raise TypeError(f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}")


    @classmethod
    def from_basics(cls, name, standard_notation, qty_measured):
        """ Create a unit from basic data.

            Attributes
            ----------
            name : str.
                Common name of the unit.
            standard_notation : str.
                Standard notation of the unit.
            qty_measured : str.
                The quantity measured by the unit---e.g., 'length', 'mass', 'time'.
        
        """

        unit = cls()
        unit.set_name(name)
        unit.set_standard_notation(standard_notation)
        unit.set_qty_measured(qty_measured)

        return unit
    
    def set_name(self, name):
        """ Set the name of the unit of measurement.
        
            Parameters
            ----------
            name : str
                Name of the unit of measurement.
        
        """

        self.name = name

    def set_standard_notation(self, standard_notatoion):
        """ Set the standard notation of the unit of measurement.
        
            Parameters
            ----------
            standard_notatoion : str
                Standard notation of the unit of measurement.
        
        """

        self.standard_notation = standard_notatoion

    def set_qty_measured(self, qty_measured):
        """ Set the quantity measured by the unit of measurement.
        
            Parameters
            ----------
            qty_measured : str
                Quantity measured by the unit of measurement.
        
        """

        self.qty_measured = qty_measured


    def get_name(self):
        """ Get the name of the unit of measurement.

            Returns
            -------
            str
                Name of the unit of measurement.

        """

        return self.name
    
    def get_standard_notation(self):
        """ Retrieve the standard notation of the unit of measurement.

            Returns
            -------
            str
                Standard notation of the unit of measurement.

        """

        return self.standard_notation
    
    def get_qty_measured(self):
        """ Get the quantity measured by the unit of measurement.

            Returns
            -------
            str.
                Quantity measured by the unit of measurement.

        """

        return self.qty_measured
    
    def get_base(self):
        """ Retrieve the base unit of the unit of measurement, if exist.

            Returns
            -------
            Unit Obj.
                Base unit of measurement, or None if itself a base unit of measurement.

        """

        return self.base_unit

    def get_prefix(self):
        """ Retrieve the metric prefix of the unit of measurement, if exist.

            Returns
            -------
            MetricPrefix Obj.
                Metric prefix of the unit of measurement, or None if no prefix.

        """

        return self.prefix

    def get_components(self):
        """ Retrieve components of the unit of measurement, if a compound unit.

            Returns
            -------
            List of Unit Obj.
                List of component units, or None if not a compound unit.

        """

        return self.components

    def get_conversion_factor(self, to_unit):
        """ Returns conversion factor.

            Parameters
            ----------
            to_unit : Unit Obj.
                Unit of measurement to which the value will be converted to (from the current unit of measuremnt).

            Returns
            -------
            float
                Conversion factor to be applied on the value.
        
        """

        if self.get_qty_measured() == to_unit.get_qty_measured():
            if not self.convert_compound:
                if self == to_unit:
                    return 1.0
                elif self.get_base() is None or to_unit.get_base() is None:
                    return Unit.compute_conversion_factor(self, to_unit, self.get_qty_measured())
                elif self.get_base() == to_unit.get_base():
                    return self.prefix.get_conversion_factor(to_unit.get_prefix())
                else: # both units are prefixed
                    return Unit.compute_conversion_factor(self, to_unit, self.get_qty_measured())
            else:
                components_in = self.get_components()
                components_out = to_unit.get_components()

                conversion_factor = 1.0
                for component_in, component_out in zip(components_in, components_out): # it is assumed components of in and out are in same order
                    conversion_factor *= component_in.get_conversion_factor(component_out)
                return conversion_factor
            
        else:
            raise TypeError(f"{self.get_name()} of dimensions {self.get_qty_measured()} and {to_unit.get_name()} of dimensions {to_unit.get_qty_measured()} are incompatible.")
        
    @staticmethod
    def compute_conversion_factor(unit_in, unit_out, qty_measured):
        """ Computes conversion factor from unit_in to unit_out, given (a) They both measure same quantities, and 
            (b) they are not compound units.

            Parameters
            ----------
            unit_in : Unit Obj.
                Unit of measurement from which the value will be converted.
            unit_out : Unit Obj.
                Unit of measurement to which the value will be converted.
            qty_measured : str
                Quantity measured by the units of measruements considered.
                
            Returns
            -------
            float
                Conversion factor to be applied on the value.        

        """
        inverse_flag = False
        unit_in_name = unit_in.get_name() if unit_in.get_base() is None else unit_in.get_base().get_name()
        unit_out_name = unit_out.get_name() if unit_out.get_base() is None else unit_out.get_base().get_name()
        
        if qty_measured.startswith('per '):
            inverse_flag = True
            qty_measured = qty_measured.replace('per ', "")
            unit_in_name = unit_in_name.replace('per ', "")
            unit_out_name = unit_out_name.replace('per ', "")

        if unit_in.get_base() is None:
            factor_in = UNIT_CONVERSIONS[qty_measured][unit_in_name]
        else:
            factor_in = UNIT_CONVERSIONS[qty_measured][unit_in_name] / 10**(unit_in.get_prefix().get_power())

        if unit_out.get_base() is None:
            factor_out = UNIT_CONVERSIONS[qty_measured][unit_out_name]  
        else:
            factor_out = UNIT_CONVERSIONS[qty_measured][unit_out_name] / 10**(unit_out.get_prefix().get_power())

        conversion_factor = factor_out / factor_in
        if inverse_flag:
            conversion_factor = 1 / conversion_factor

        return conversion_factor
    

class MetricPrefix:
    """
    Unit object from which units are created.

    Attributes
    ----------
    name : str.
        Standard name of the prefix.
    symbol : str.
        Standard symbol of the unit.
    power : int.
        Power to the ten corresponding to the prefix.
    """
    def __init__(self, name, symbol, power):
        # No create_from class method is implemented as users are not expected to create new prefixes.
        # The definitive list of prefixes are initiated and ready for use from metric_prefixes.py.
        self.name = name
        self.symbol = symbol
        self.power = power

    def __str__(self):
        return f"Metric prefix {self.get_name()} ({self.get_symbol()}) representing a value of e{self.get_power()}."

    def __mul__(self, other):
        """ Multiplication of metric prefixes with other metric prefixes or units."""

        if isinstance(other, MetricPrefix):

            new_power = self.get_power() + other.get_power()
            all_powers = get_attribute_as_list(ALL_PREFIXES, 'power')

            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                print(f"Multiplication of {self.get_name()} and {other.get_name()} does not return a standard metric prefix.")

        elif isinstance(other, Unit):

            return other.__rmul__(self)
        
        else:

            raise TypeError(f"unsupported operand type(s) for *: {self.__class__.__name__} and {other.__class__.__name__}")
        
    def __truediv__(self, other):
        """ Division of metric prefixes with other metric prefixes or units."""

        if isinstance(other, MetricPrefix):

            new_power = self.get_power() - other.get_power()
            all_powers = get_attribute_as_list(ALL_PREFIXES, 'power')

            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                print(f"Division of {self.get_name()} and {other.get_name()} does not return a standard metric prefix.")

        elif isinstance(other, Unit):

            return other.__rmul__(self)
        
        else:

            raise TypeError(f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}")
        
    def __rtruediv__(self, other):
        """ Reflective division of metric prefixes with numbers."""

        if isinstance(other, int) or isinstance(other, float):
            if other <= 0 or not log10(other).is_integer():
                raise TypeError(f"Reflexive division of prefixes constrained to values that are integer powers of 10.")
            
            new_power = log10(other) - self.get_power()
            all_powers = get_attribute_as_list(ALL_PREFIXES, 'power')

            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                print(f"Division of {self.get_name()} and {other.get_name()} does not return a standard metric prefix.") 

        else:
            raise TypeError(f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}")           

    def get_name(self):
        """ Retrieve the name of the prefix.

            Returns
            -------
            str
                Standard name of the prefix.

        """

        return self.name
    
    def get_symbol(self):
        """ Retrieve the symbol of the prefix.

            Returns
            -------
            str
                Symbol of the prefix.

        """

        return self.symbol

    def get_power(self):
        """ Retrieve the power to the ten corresponding to the prefix.

            Returns
            -------
            int
                Power to the ten corresponding to the prefix.

        """

        return self.power
        
    def get_conversion_factor(self, to_prefix):
        """ Compute conversion factor for converting preixes.
        
            Parameters
            ----------
            to_prefix : MetricPrefix Obj.
                Metric prefix to which the value will be converted to (from the current metric prefix).

            Returns
            -------
            float
                Conversion factor to be applied on the value.

        """

        return 10**(to_prefix.get_power() - self.get_power())


if __name__ == '__main__':
    pass
