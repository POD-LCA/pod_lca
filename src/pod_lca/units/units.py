__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from copy import deepcopy
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
    components : list of ~pod_lca.units.Unit
        List of components the unit is made up of. None if not a compound unit
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

        new_prefix = MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'multiply')
        prefix_name = "" if new_prefix is None else new_prefix.get_name()

        result = Unit.from_basics(
            name=prefix_name + self.get_name() + "-" + other.get_name(),
            standard_notation=self.get_standard_notation() + other.get_standard_notation(),
            qty_measured=self.get_qty_measured() + "-" + other.get_qty_measured()
        )
        result.numerator = self.numerator + other.numerator
        result.denominator = self.denominator + other.denominator
        result.prefix = new_prefix

        _, result = result.simplify()
        result.collapse_powers()

        return result

    def __rmul__(self, other):
        """Reflexive multiplication of units by metric prefixes."""
        if isinstance(other, MetricPrefix):
            if self.prefix:
                new_prefix = self.prefix * other
            else:
                new_prefix = other

            name = new_prefix.get_name() + self.get_name()
            standard_notation = new_prefix.get_symbol() + self.get_standard_notation()
            qty_measured = self.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.numerator = self.numerator[:]
            newUnit.denominator = self.denominator[:]
            newUnit.prefix = new_prefix

            return newUnit
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
        
        new_prefix = MetricPrefix.safe_combine_prefix(self.prefix, other.prefix, 'divide')
        prefix_name = "" if new_prefix is None else new_prefix.get_name()

        result = Unit.from_basics(
            name=prefix_name + self.get_name() + " per " + other.get_name(),
            standard_notation=self.get_standard_notation() + "/" + other.get_standard_notation(),
            qty_measured=self.get_qty_measured() + " per " + other.get_qty_measured()
        )

        result.numerator = self.numerator + other.denominator
        result.denominator = self.denominator + other.numerator
        result.prefix = new_prefix

        factor, result = result.simplify()
        result.collapse_powers()

        return result

    def __rtruediv__(self, other):
        """Reflexive division of units by unit value (1)."""
        if other == 1:
            if self.get_name().startswith("per "):
                name = self.get_name()[4:]
                standard_notation = self.get_standard_notation()[:-2]
                qty_measured = self.get_qty_measured()[4:]
            else:
                name = "per " + self.get_name()
                standard_notation = self.get_standard_notation() + "-1"
                qty_measured = "per " + self.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.prefix = MetricPrefix.safe_combine_prefix(1, other.prefix, 'divide')
            newUnit.denominator = self.numerator
            newUnit.numerator = self.denominator

            return newUnit
        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

    @classmethod
    def from_basics(cls, name, standard_notation, qty_measured, is_compound=False):
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

        if not is_compound:
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
        if (self.get_prefix() is None) and (len(self.numerator) == 1) and (len(self.get_components()) == 1):
            return False
        else:
            return True
        
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
            if not self.is_compound():
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

    def simplify(self):
        """Simplify a compound unit by cancelling common components in numerator and denominator.

        Returns
        -------
        :class:`float`
            Conversion factor resulting from the simplification.
        :class:`~pod_lca.units.Unit`
            Simplified unit.
        """
        if not self.is_compound():
            return 1.0, self

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
                    pass # TODO: extend with unit conversion

        total = len(self.numerator) + len(self.denominator)

        # Update metadata
        base_name = "-".join([u.name for u in self.numerator] +
                             [u.name for u in self.denominator])
        base_notation = "".join([u.standard_notation for u in self.numerator]) + \
                        "".join([f"/{u.standard_notation}" for u in self.denominator])
        base_qty_measured = "-".join([u.qty_measured for u in self.numerator] +
                                     [u.qty_measured for u in self.denominator])
        
        if self.prefix:
            self.name = self.prefix.get_name() + base_name
            self.standard_notation = self.prefix.get_symbol() + base_notation
        else:
            self.name = base_name
            self.standard_notation = base_notation
        self.qty_measured = base_qty_measured

        return factor, self

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

        # Update metadata
        total = len(self.numerator) + len(self.denominator)

        base_name = "-".join([u.name for u in self.numerator] +
                             [u.name for u in self.denominator])
        base_notation = "".join([u.standard_notation for u in self.numerator]) + \
                        "".join([f"/{u.standard_notation}" for u in self.denominator])
        base_qty_measured = "-".join([u.qty_measured for u in self.numerator] +
                                     [u.qty_measured for u in self.denominator])
        
        if self.prefix:
            self.name = self.prefix.get_name() + base_name
            self.standard_notation = self.prefix.get_symbol() + base_notation
        else:
            self.name = base_name
            self.standard_notation = base_notation
        self.qty_measured = base_qty_measured

        return self


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
                print(
                    f"Multiplication of {self.get_name()} and {other.get_name()} does not return a standard metric prefix."
                )

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
    def safe_combine_prefix(p1, p2, operator='multiply'):
        if p1 and p2:
            if operator == 'multiply':
                return p1 * p2
            elif operator == 'divide':
                return p1 / p2
        return p1 or p2

if __name__ == "__main__":
    pass

# TODO: check is_compound()
# TODO: check conversion
# TODO: unit test coverage for multiply and divide
# TODO: replace == with is, where applicable
