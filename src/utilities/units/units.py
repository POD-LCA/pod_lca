from utilities.units import UNIT_CONVERSIONS

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
    base_unit : Unit Obj
        Base unit of the Obj. None if itself a base unit.
    prefix : MetricPrefix Obj.
        Metric prefix. None if a base unit or non-metric.
    type : str.
        The quantity measure by the unit---e.g., 'length', 'mass', 'time'.
    is_compound_unit : bool
        True, if a compound unit made of other units.
    is_metric : bool
        True, if a metric unit. This will let it have metric prefixes.
    components : List of Unit Obj.
        List of components the unit is made up of. None if not a compound unit
    """
    def __init__(self, name, standard_notation, type, is_metric):
        self.name = name
        self.standard_notation = standard_notation
        self.base_unit = None
        self.prefix = None
        self.type = type
        self.is_compound_unit = False
        self.is_metric = is_metric
        self.components = None

    def get_name(self):

        return self.name
    
    def get_standard_notation(self):

        return self.standard_notation

    def get_base(self):

        return self.base_unit

    def get_prefix(self):

        return self.prefix
    
    def get_type(self):

        return self.type

    def get_components(self):

        return self.components

    def get_convertion_factor(self, to_unit):
        """ Returns conversion factor."""

        if self.get_type() == to_unit.get_type():
            if self.is_compound_unit:
                pass
                # TODO: for each component do conversion, and combine back
            else:
                if self.get_base() == to_unit.get_base():

                    return self.prefix.convert(to_unit.get_prefix())
                
                elif self.get_base() is None or to_unit.get_base() is None:
                    if self.get_base() is None:
                        factor_in = UNIT_CONVERSIONS[self.get_type()][self.get_name()]
                    else:
                        factor_in = UNIT_CONVERSIONS[self.get_type()][self.get_base().get_name()] / 10**(self.get_prefix().get_power())


                    if to_unit.get_base() is None:
                        factor_out = UNIT_CONVERSIONS[self.get_type()][to_unit.get_name()]  
                    else:
                        factor_out = UNIT_CONVERSIONS[self.get_type()][to_unit.get_base().get_name()] / 10**(to_unit.get_prefix().get_power())

                    return factor_out / factor_in

                else:
                    pass
                    # TODO: example for this
                    # TODO: implement
                    #   convert prefixes
                    #   convert base units        
        else:
            raise TypeError(f"{self.get_name()} of dimensions {self.get_type()} and {to_unit.get_name()} of dimensions {to_unit.get_type()} are incompatible.")
        
        
    # TODO: Method to create units from base units
    # TODO: update docstrings

class MetricPrefix:

    def __init__(self, name, symbol, power):
        self.name = name
        self.symbol = symbol
        self.power = power

    def get_name(self):

        return self.name
    
    def get_symbol(self):

        return self.symbol

    def get_power(self):

        return self.power
        
    def convert(self, to_prefix):

        return 10**(to_prefix.get_power() / self.get_power())


if __name__ == '__main__':
    from utilities.units.standard_units import METER, MILE, KILOMETER, GRAM, KILOGRAM, SQUARE_FEET

    conversion_factor = METER.get_convertion_factor(to_unit=KILOMETER)
    print(conversion_factor)
