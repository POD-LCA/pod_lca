
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
    
    def get_type(self):

        return self.type

    def convert(self, to_unit):

        if Unit.is_type(to_unit, self.type):
            if self.is_compound_unit:
                pass
                # for each component do conversion, and combine back
            else:
                if self.base_unit == self.base_unit:
                    pass
                    # do prefix convert
                else:
                    pass
                    # get conversion factor to convert
                
        else:
            raise TypeError
        

class MetricPrefix:

    def __init__(self, name, symbol, power):
            self.name = name
            self.symbol = symbol
            self.power = power    
        
    def prefix_convert(self, to_prefix):

        pass



