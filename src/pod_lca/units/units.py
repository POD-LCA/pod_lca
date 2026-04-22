__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from collections import Counter
from math import log10
from copy import deepcopy

from ..units import ALL_PREFIXES
from ..units import STANDARD_COMPOUNDS
from ..units import UNIT_CONVERSIONS
from ..units import UNIT_NAME_OVERRIDES
from ..units import UNIT_NOTATION_OVERRIDES
from ..utilities import ArrayMethods


class Unit:
    """Unit object from which units are created.

    Attributes
    ----------
    name : str
        Common name of the unit.
    standard_notation : str
        Standard notation of the unit.
    qty_measured : {'time', 'mass', 'length', 'area', 'volume', 'power', 'energy', 'count', 'carbon storage'}
        The quantity measured by the unit.
    prefix : ~pod_lca.units.MetricPrefix
        Metric prefix. None if a base unit or non-metric.
    numerator : list of ~pod_lca.units.Unit
        List of components in the numerator of the unit.
    denominator : list of ~pod_lca.units.Unit
        List of components in the denominator of the unit.
    """

    def __init__(self):
        self.name = None
        self.standard_notation = None
        self.qty_measured = None
        self.prefix = None
        self.units = BaseUnits()

    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj
        for k, v in self.__dict__.items():
            setattr(new_obj, k, deepcopy(v, memo))
        return new_obj


    def __str__(self):
        return f"Unit {self.get_name()} ({self.get_standard_notation()}) measuring {self.get_qty_measured()}."
    
    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.units == other.units
        return NotImplemented

    def __hash__(self):
        return hash((
            self.get_name(),
            self.get_standard_notation(),
            self.get_qty_measured()
        ))

    def __mul__(self, other):
        """Multiplication of units by other units."""
        if not isinstance(other, Unit):
            raise TypeError(f"unsupported operand type(s) for *: {type(self)} and {type(other)}")

        result = Unit.from_basics("", "", "")
        result.units = self.units + other.units
        result.prefix = MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'multiply')

        for key in list(result.units.keys()):
            if result.units[key] == 0:
                del result.units[key]

        result.expand_standard_compounds()
        result.collapse_standard_compounds()
        result._rebuild_strings()

        return result

    def __rmul__(self, other):
        """Reflexive multiplication of units by metric prefixes."""
        if isinstance(other, MetricPrefix):
            if self.prefix:
                new_prefix = self.prefix * other
            else:
                new_prefix = other

            result = Unit.from_basics("", "", "")
            result.units = self.units
            result.prefix = new_prefix
    
            result.expand_standard_compounds()
            result.collapse_standard_compounds()
            result._rebuild_strings()

            return result
        else:
            raise TypeError(
                f"unsupported operand type(s) for *: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    def __truediv__(self, other):
        """Division of units by other units."""
        if not isinstance(other, Unit):
            raise TypeError(
                f"unsupported operand type(s) for /: {type(self).__name__} and {type(other).__name__}"
            )

        result = Unit.from_basics("","","")
        result.units = self.units - other.units
        result.prefix =  MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'divide')

        for key in list(result.units.keys()):
            if result.units[key] == 0:
                del result.units[key]
                
        result.expand_standard_compounds()
        result.collapse_standard_compounds()
        result._rebuild_strings()

        return result

    def __rtruediv__(self, other):
        """Reflexive division of units by unit value (1)."""
        if other == 1:
            result = Unit.from_basics("","","")
            result.prefix = MetricPrefix.safe_combine_prefix(None, self.prefix, 'divide')
            result.units = -self.units

            result.expand_standard_compounds()
            result.collapse_standard_compounds()
            result._rebuild_strings()

            return result
        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    @property
    def numerator(self):
        result = []
        for u, p in self.units.items():
            if p > 0:
                result.extend([u] * p)
        return result

    @property
    def denominator(self):
        result = []
        for u, p in self.units.items():
            if p < 0:
                result.extend([u] * (-p))
        return result

    @classmethod
    def from_basics(cls, name, standard_notation, qty_measured):
        """Create a unit from basic data.

        Parameters
        ----------
        name : str
            Common name of the unit.
        standard_notation : str
            Standard notation of the unit.
        qty_measured : {'time', 'mass', 'length', 'area', 'volume', 'power', 'energy', 'count', 'carbon storage'}
            The quantity measured by the unit.
        """
        unit = cls()
        unit.set_name(name)
        unit.set_standard_notation(standard_notation)
        unit.set_qty_measured(qty_measured)

        unit.units = BaseUnits({unit:1})

        return unit

    def set_name(self, name):
        """Set the name of the unit of measurement.

        Parameters
        ----------
        name : str
            Name of the unit of measurement.
        """
        self.name = name

        return self

    def set_standard_notation(self, standard_notatoion):
        """Set the standard notation of the unit of measurement.

        Parameters
        ----------
        standard_notatoion : str
            Standard notation of the unit of measurement.
        """
        self.standard_notation = standard_notatoion

        return self

    def set_qty_measured(self, qty_measured):
        """Set the quantity measured by the unit of measurement.

        Parameters
        ----------
        qty_measured : str
            Quantity measured by the unit of measurement.
        """
        self.qty_measured = qty_measured

        return self

    def get_name(self):
        """Get the name of the unit of measurement.

        Returns
        -------
        str
            Name of the unit of measurement.
        """
        return self.name

    def get_standard_notation(self):
        """Retrieve the standard notation of the unit of measurement.

        Returns
        -------
        str
            Standard notation of the unit of measurement.
        """
        return self.standard_notation

    def get_qty_measured(self):
        """Get the quantity measured by the unit of measurement.

        Returns
        -------
        str
            Quantity measured by the unit of measurement.
        """
        return self.qty_measured

    def get_prefix(self):
        """Retrieve the metric prefix of the unit of measurement, if exist.

        Returns
        -------
        ~pod_lca.units.MetricPrefix
            Metric prefix of the unit of measurement, or None if no prefix.
        """
        return self.prefix

    def get_components(self, unique=False):
        """Retrieve components of the unit of measurement, if a compound unit.

        Returns
        -------
        list of ~pod_lca.units.Unit
            List of component units, or None if not a compound unit.
        """
        components = []
        for u, p in self.units.items():
            if unique:
                components.extend([u])
            else:
                components.extend([u] * abs(p))
        return components

    def is_compound(self):
        if (self.get_prefix() is None) and (len(self.numerator) <= 1) and (len(self.get_components()) <= 1):
            return False
        else:
            return True

    def is_dimensionless(self):
        """Check if the unit is dimensionless (no numerator or denominator, no name)."""
        return (
            not self.numerator and
            not self.denominator and
            not self.name and
            not self.standard_notation and
            not self.qty_measured
        )
    
    def convert_to(self, to_unit):
        """Returns conversion factor.

        Notes
        -----
        - Assumes multiple units are not used to measure the same thing (e.g., unit_in has both meters and feet. This is invalid).

        Parameters
        ----------
        to_unit : ~pod_lca.units.Unit
            Unit of measurement to which the value will be converted to (from the current unit of measuremnt).

        Returns
        -------
        float
            Conversion factor to be applied on the value.

        Raises
        ------
        TypeError
            Incompatible units for conversion.
        """
        # incompatible units
        if self.get_qty_measured() != to_unit.get_qty_measured():
            raise TypeError("Incompatible units for conversion.")
    
        # simple unit conversion
        if (not self.is_compound()) and (not to_unit.is_compound()):
            if self == to_unit:
                return 1.0
            return Unit.compute_conversion_factor(self, to_unit)

        # compound unit conversion
        factor = 1.0
        for component_in, power_in in self.units.items():
            for component_out, power_out in to_unit.units.items():
                if power_in != power_out:
                    continue

                try:
                    factor *= (component_in.convert_to(component_out)) ** power_in
                    break
                except TypeError:
                    pass

            else:
                raise TypeError("Incompatible units for conversion.")

        # prefix
        if self.prefix:
            factor *= 10 ** self.prefix.get_power()

        if to_unit.prefix:
            factor /= 10 ** to_unit.prefix.get_power()

        return factor


    @staticmethod
    def compute_conversion_factor(unit_in, unit_out):
        """Computes conversion factor from unit_in to unit_out, given (a) They both measure same quantities, and
            (b) they are not compound units.

        Parameters
        ----------
        unit_in : ~pod_lca.units.Unit
            Unit of measurement from which the value will be converted.
        unit_out : ~pod_lca.units.Unit
            Unit of measurement to which the value will be converted.

        Returns
        -------
        float
            Conversion factor to be applied on the value.
        """
        qty = unit_in.get_qty_measured()

        name_in = unit_in.get_name()
        name_out = unit_out.get_name()

        factor_in = UNIT_CONVERSIONS[qty][name_in]
        factor_out = UNIT_CONVERSIONS[qty][name_out]

        if unit_in.prefix:
            factor_in /= 10 ** unit_in.prefix.get_power()

        if unit_out.prefix:
            factor_out /= 10 ** unit_out.prefix.get_power()

        return factor_out / factor_in
            
    def expand_standard_compounds(self,):
        changed = True
        while changed:
            changed = False

            for u, power in list(self.units.items()):
                if u in STANDARD_COMPOUNDS and power != 0:
                    self.units[u] -= power
                    if self.units[u] == 0:
                        del self.units[u]

                    for base_u, base_p in STANDARD_COMPOUNDS[u].items():
                        self.units[base_u] += base_p * power

                    changed = True
                    break  # restart scan

        return self

    def collapse_standard_compounds(self):
        """Collapse repeated units into squared/cubed forms based on a rules dict.
        """
        compounds_sorted = sorted(
            STANDARD_COMPOUNDS.keys(),
            key=lambda u: sum(STANDARD_COMPOUNDS[u].values()),
            reverse=True
        ) # sorted largest to smallest based on power

        changed = True
        while changed:
            changed = False

            for compound in compounds_sorted:
                def_counter = Counter(STANDARD_COMPOUNDS[compound])
                num_check = all(self.units.get(u, 0) >= p for u, p in def_counter.items())
                denom_check = all(self.units.get(u, 0) <= -p for u, p in def_counter.items())
                if num_check or denom_check:
                    for u, p in def_counter.items():
                        if num_check:
                            self.units[u] -= p
                        else:
                            self.units[u] += p
                        if self.units[u] == 0:
                            del self.units[u]
                    if num_check:
                        self.units[compound] += 1
                    else:
                        self.units[compound] -= 1
                    changed = True
                    break  # restart scan

        return self

    def _rebuild_strings(self):
        """ Rebuild name, standard notation, and quantity.

        Notes
        -----
        The following rules apply:
        - Numerator units joined by '-'
        - Denominator units joined by '-'
        - 'per' (name) or '/' (notation) between numerator and denominator only if denominator exists
        - Parentheses if more than one unit in numerator or denominator
        - Prefix applied at the front if present. If no numerator, prefix indicated in the denominator
        """
        num_units = [u for u in self.numerator if not u.is_dimensionless()]
        denom_units = [u for u in (self.denominator or []) if not u.is_dimensionless()]

        # Helper
        def join_group(units):
            if not units:
                return ""
            if len(units) == 1:
                return units[0].name
            return "(" + "-".join(u.name for u in units) + ")"

        def join_group_notation(units):
            if not units:
                return ""
            if len(units) == 1:
                return units[0].standard_notation
            return "(" + "-".join(u.standard_notation for u in units) + ")"

        def join_group_qty(units):
            if not units:
                return ""
            if len(units) == 1:
                return units[0].qty_measured
            return "(" + "-".join(u.qty_measured for u in units) + ")"

        # Build numerator/denominator strings
        num_name = join_group(num_units)
        denom_name = join_group(denom_units)

        num_notation = join_group_notation(num_units)
        denom_notation = join_group_notation(denom_units)

        num_qty = join_group_qty(num_units)
        denom_qty = join_group_qty(denom_units)

        # Combine numerator and denominator
        if denom_name:
            self.name = f"{num_name} per {denom_name}" if num_name else f"per {denom_name}"
            self.standard_notation = f"{num_notation}/{denom_notation}" if num_notation else f"1/{denom_notation}"
            self.qty_measured = f"{num_qty} per {denom_qty}" if num_qty else f"per {denom_qty}"
        else:
            self.name = num_name
            self.standard_notation = num_notation
            self.qty_measured = num_qty

        # Apply prefix at the front
        if self.prefix:
            if not self.numerator:
                denom_prefix = self.prefix.inverse()
                self.name = f"per {denom_prefix.get_name()}{denom_name}" if self.denominator else self.prefix.get_name()
                self.standard_notation = f"1/{denom_prefix.get_symbol()}{denom_notation}"
            else:
                self.name = f"{self.prefix.get_name()}{self.name}" if self.name else self.prefix.get_name()
                self.standard_notation = f"{self.prefix.get_symbol()}{self.standard_notation}" if self.standard_notation else self.prefix.get_symbol()

        if self.name in UNIT_NAME_OVERRIDES:
            self.name = UNIT_NAME_OVERRIDES[self.name]
        if self.standard_notation in UNIT_NOTATION_OVERRIDES:
            self.standard_notation = UNIT_NOTATION_OVERRIDES[self.standard_notation]


class MetricPrefix:
    """Unit object from which units are created.

    Attributes
    ----------
    name : str
        Standard name of the prefix.
    symbol : str
        Standard symbol of the unit.
    power : int
        Power to the ten corresponding to the prefix.
    """

    def __init__(self, name, symbol, power):
        # No create_from class method is implemented as users are not expected to create new prefixes.
        # The definitive list of prefixes are initiated and ready for use from metric_prefixes.py.
        self.name = name
        self.symbol = symbol
        self.power = power

    def __eq__(self, other):
        if isinstance(other, MetricPrefix):
            return (
                self.get_name() == other.get_name() and
                self.get_symbol() == other.get_symbol() and
                self.get_power() == other.get_power()
            )
        return NotImplemented
    
    def __str__(self):
        return f"Metric prefix {self.get_name()} ({self.get_symbol()}) representing a value of e{self.get_power()}."

    def __mul__(self, other):
        """Multiplication of metric prefixes with other metric prefixes or units."""
        if isinstance(other, MetricPrefix):

            new_power = self.get_power() + other.get_power()
            all_powers = ArrayMethods.get_attribute_as_list(ALL_PREFIXES, "power")

            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                superscript = str(new_power).translate(str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))
                return MetricPrefix("", f"10{superscript}", new_power)

        elif isinstance(other, Unit):

            return other.__rmul__(self)

        else:

            raise TypeError(
                f"unsupported operand type(s) for *: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    def __truediv__(self, other):
        """Division of metric prefixes with other metric prefixes or units."""
        if isinstance(other, MetricPrefix):

            new_power = self.get_power() - other.get_power()
            if new_power == 0:
                return None

            all_powers = ArrayMethods.get_attribute_as_list(ALL_PREFIXES, "power")
            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                print(f"Division of {self.get_name()} and {other.get_name()} does not return a standard metric prefix.")

        elif isinstance(other, Unit):

            return other.__rmul__(self)

        else:

            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    def __rtruediv__(self, other):
        """Reflective division of metric prefixes with numbers."""
        if isinstance(other, int) or isinstance(other, float):
            if other <= 0 or not log10(other).is_integer():
                raise TypeError("Reflexive division of prefixes constrained to values that are integer powers of 10.")

            new_power = log10(other) - self.get_power()
            if new_power == 0:
                return None
            
            all_powers = ArrayMethods.get_attribute_as_list(ALL_PREFIXES, "power")
            try:
                index = all_powers.index(new_power)
                newPrefix = ALL_PREFIXES[index]
                return newPrefix
            except ValueError:
                print(f"Division of {self.get_name()} and {other.get_name()} does not return a standard metric prefix.")

        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    def get_name(self):
        """Retrieve the name of the prefix.

        Returns
        -------
        str
            Standard name of the prefix.
        """
        return self.name

    def get_symbol(self):
        """Retrieve the symbol of the prefix.

        Returns
        -------
        str
            Symbol of the prefix.
        """
        return self.symbol

    def get_power(self):
        """Retrieve the power to the ten corresponding to the prefix.

        Returns
        -------
        int
            Power to the ten corresponding to the prefix.
        """
        return self.power

    def convert_to(self, to_prefix):
        """Compute conversion factor for converting preixes.

        Parameters
        ----------
        to_prefix : ~pod_lca.units.MetricPrefix
            Metric prefix to which the value will be converted to (from the current metric prefix).

        Returns
        -------
        float
            Conversion factor to be applied on the value.
        """
        return 10 ** (self.get_power() - to_prefix.get_power())

    @staticmethod
    def safe_combine_prefix(p1, p2, operator="multiply"):
        if operator == "multiply":
            if p1 and p2:
                return p1 * p2
            return p1 or p2

        if operator == "divide":
            if p1 and p2:
                return p1 / p2
            if p1 and not p2:
                return p1 
            if not p1 and p2:
                return p2.inverse()
            return None

        raise ValueError(f"Unknown operator: {operator}")

    def inverse(self):
        new_power = -self.power

        all_powers = ArrayMethods.get_attribute_as_list(ALL_PREFIXES, "power")
        try:
            index = all_powers.index(new_power)
            newPrefix = ALL_PREFIXES[index]
            return newPrefix
        except ValueError:
            superscript = str(new_power).translate(str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))
            return MetricPrefix("", f"10{superscript}", new_power)
    

class BaseUnits(dict):
    """Object to keep track of base unit counts.
    """
    def __init__(self, data=None):
        super().__init__()
        if data:
            for k, v in data.items():
                self[k] = v

    def __eq__(self, other):
        if self is other:
            return True
        
        if not isinstance(other, dict):
            return False

        def get_primitive_map(d):
            return {
                (getattr(k, 'name', k)): v 
                for k, v in dict.items(d) 
                if v != 0
            }

        return get_primitive_map(self) == get_primitive_map(other)

    def __getitem__(self, key):
        return super().get(key, 0)
    
    def __neg__(self):
        result = BaseUnits(self)
        for k, v in self.items():
                    result[k] = -v
        return result
    
    def __add__(self, other):
        result = BaseUnits(self)
        for k, v in other.items():
            result[k] = result.get(k, 0) + v
        return result

    def __sub__(self, other):
        result = BaseUnits(self)
        for k, v in other.items():
            result[k] = result.get(k, 0) - v
        return result

    def __iadd__(self, other):
        for k, v in other.items():
            self[k] = self.get(k, 0) + v
        return self

    def __isub__(self, other):
        for k, v in other.items():
            self[k] = self.get(k, 0) - v
        return self

    def copy(self):
        return BaseUnits(self)
    

if __name__ == "__main__":
    pass
