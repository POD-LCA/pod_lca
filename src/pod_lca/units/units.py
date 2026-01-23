__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from collections import Counter
from math import log10

from ..units import UNIT_CONVERSIONS, ALL_PREFIXES, POWER_RULES
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
        self.numerator = []
        self.denominator = []


    def __str__(self):
        return f"Unit {self.get_name()} ({self.get_standard_notation()}) measuring {self.get_qty_measured()}."
    
    def __eq__(self, other):
        if isinstance(other, Unit):
            return (
                self.get_name() == other.get_name() and
                self.get_standard_notation() == other.get_standard_notation() and
                self.get_qty_measured() == other.get_qty_measured()
            )
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
        result.numerator = self.numerator + other.numerator
        result.denominator = self.denominator + other.denominator
        result.prefix = MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'multiply')

        result = result.simplify()
        result.collapse_powers()
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
            result.numerator = self.numerator[:]
            result.denominator = self.denominator[:]
            result.prefix = new_prefix
    
            result = result.simplify()
            result.collapse_powers()
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
        result.numerator = self.numerator + other.denominator
        result.denominator = self.denominator + other.numerator
        result.prefix =  MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'divide')

        result = result.simplify()
        result.collapse_powers()
        result._rebuild_strings()

        return result

    def __rtruediv__(self, other):
        """Reflexive division of units by unit value (1)."""
        if other == 1:
            result = Unit.from_basics("","","")
            result.prefix = MetricPrefix.safe_combine_prefix(None, self.prefix, 'divide')
            result.denominator = self.numerator
            result.numerator = self.denominator

            result = result.simplify()
            result.collapse_powers()
            result._rebuild_strings()

            return result
        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

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

        unit.numerator = [unit]

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

    def get_components(self):
        """Retrieve components of the unit of measurement, if a compound unit.

        Returns
        -------
        list of ~pod_lca.units.Unit
            List of component units, or None if not a compound unit.
        """
        return self.numerator + self.denominator

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
        if self.get_qty_measured() == to_unit.get_qty_measured():
            if (not self.is_compound()) and (not to_unit.is_compound()):
                if self == to_unit:
                    return 1.0
                return Unit.compute_conversion_factor(self, to_unit)

            factor = 1.0

            # Numerator conversions
            self_num = self.numerator
            to_num = to_unit.numerator 
            for u_in, u_out in zip(self_num, to_num):
                factor *= u_in.convert_to(u_out)

            # Denominator conversions (inverse)
            self_den = self.denominator
            to_den = to_unit.denominator
            for u_in, u_out in zip(self_den, to_den):
                factor /= u_in.convert_to(u_out)

            # prefix
            if self.prefix:
                factor *= 10 ** self.prefix.get_power()

            if to_unit.prefix:
                factor /= 10 ** to_unit.prefix.get_power()

            return factor

        simplification_factor, simplified = self.simplify()

        if simplified.get_qty_measured() == to_unit.get_qty_measured():
            return simplification_factor * simplified.convert_to(to_unit)

        raise TypeError("Incompatible units for conversion.")

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

    def simplify(self, return_factor=False):
        """Simplify a compound unit by cancelling common components in numerator and denominator.

        Parameters
        ----------
        return_factor: bool
            If false, no unit conversion operations carried out.

        Returns
        -------
        :class:`float`
            Conversion factor resulting from the simplification.
        :class:`~pod_lca.units.Unit`
            Simplified unit.
        """
        if not self.is_compound():
            if return_factor:
                return 1.0, self
            else:
                return self

        factor = 1.0
        numerator = self.numerator
        denominator = self.denominator
        for n in numerator[:]:
            for d in denominator[:]:
                if n.qty_measured != d.qty_measured:
                    continue
                
                if n == d:
                    self.numerator.remove(n)
                    self.denominator.remove(d)
                else:
                    if return_factor:
                        factor *= n.convert_to(d)
                        self.numerator.remove(n)
                        self.denominator.remove(d)

        if return_factor:
            if self.prefix:
                factor *= 10 ** self.prefix.power
                self.prefix = None
                self._rebuild_strings()
                
            return factor, self
        else: 
            self._rebuild_strings()
            if factor == 1.0:
                return self
            else:
                raise ValueError

    def collapse_powers(self, power_rules=POWER_RULES):
        """Collapse repeated units into squared/cubed forms based on a rules dict.
        """
        if not self.is_compound():
            return self
        
        # expand power rules
        reverse_power_rules = {v: k for k, v in POWER_RULES.items()}
        def expand_units(units):
            """Expand collapsed units into base units for counting."""
            expanded = []
            for u in units:
                if u in reverse_power_rules:
                    base, exp = reverse_power_rules[u]
                    expanded.extend([base] * exp)
                else:
                    expanded.append(u)
            return expanded

        # Expand numerator and denominator
        numerator_expanded = expand_units(self.numerator)
        denominator_expanded = expand_units(self.denominator or [])

        # Numerator
        num_counts = Counter(numerator_expanded)
        new_numerator = []
        for unit, count in num_counts.items():
            key = (unit, count)
            if key in power_rules:
                new_numerator.append(power_rules[key])
            else:
                new_numerator.extend([unit] * count)
        self.numerator = new_numerator

        # Denominator
        if self.denominator:
            denom_counts = Counter(denominator_expanded)
            new_denominator = []
            for unit, count in denom_counts.items():
                key = (unit, count)
                if key in power_rules:
                    new_denominator.append(power_rules[key])
                else:
                    new_denominator.extend([unit] * count)
            self.denominator = new_denominator

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
    
if __name__ == "__main__":
    pass
