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
    base_unit : ~pod_lca.units.Unit
        Base unit of the Obj. None if itself a base unit.
    prefix : ~pod_lca.units.MetricPrefix
        Metric prefix. None if a base unit or non-metric.
    convert_compound : bool
        If True, unit conversion assuming the unit to be a compound unit.
    components : list of ~pod_lca.units.Unit
        List of components the unit is made up of. None if not a compound unit
    """

    def __init__(self):
        self.name = None
        self.standard_notation = None
        self.qty_measured = None
        self.base_unit = None
        self.prefix = None
        self.convert_compound = False # TODO: try and omit and stick to numerator and denominator
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

        result = Unit.from_basics(
            name=self.get_name() + "-" + other.get_name(),
            standard_notation=self.get_standard_notation() + other.get_standard_notation(),
            qty_measured=self.get_qty_measured() + "-" + other.get_qty_measured()
        )
        result.convert_compound = True

        result.numerator = self.numerator + other.numerator
        if self.denominator or other.denominator:
            result.denominator = self.denominator + other.denominator

        _, result = result.simplify()
        result.collapse_powers()

        return result

    def __rmul__(self, other):
        """Reflexive multiplication of units by metric prefixes."""
        if isinstance(other, MetricPrefix):
            if self.get_base() is None:
                name = other.get_name() + self.get_name()
                standard_notation = other.get_symbol() + self.get_standard_notation()
                qty_measured = self.get_qty_measured()

                newUnit = Unit.from_basics(name, standard_notation, qty_measured)
                newUnit.base_unit = self
                newUnit.prefix = other

                return newUnit
            else:
                new_prefix = self.get_prefix() * other

                name = new_prefix.get_name() + self.get_base().get_name()
                standard_notation = new_prefix.get_symbol() + self.get_base().get_standard_notation()
                qty_measured = self.get_qty_measured()

                newUnit = Unit.from_basics(name, standard_notation, qty_measured)
                newUnit.base_unit = self.get_base()
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

        # Create new compound unit container
        result = Unit.from_basics(
            name=self.get_name() + " per " + other.get_name(),
            standard_notation=self.get_standard_notation() + "/" + other.get_standard_notation(),
            qty_measured=self.get_qty_measured() + " per " + other.get_qty_measured()
        )
        result.convert_compound = True

        # Reuse numerator / denominator components
        result.numerator = list(self.numerator) if self.convert_compound else [self]
        if other.convert_compound:
            # append other's numerator to denominator
            result.denominator = list(other.numerator)
            # also add other's denominator to numerator (division by fraction)
            if other.denominator:
                result.numerator += list(other.denominator)
        else:
            # simple unit: goes to denominator
            result.denominator = [other]

        # Simplify and collapse powers in-place
        factor, result = result.simplify()
        result.collapse_powers()

        # Normalize empty denominator → None
        if result.denominator == []:
            result.denominator = None

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
            newUnit.base_unit = self.get_base()
            newUnit.prefix = self.get_prefix()
            newUnit.convert_compound = self.convert_compound
            newUnit.components = [self] if self.get_components() is None else self.get_components()
            newUnit.denominator = [self]

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

    def get_base(self):
        """Retrieve the base unit of the unit of measurement, if exist.

        Returns
        -------
        ~pod_lca.units.Unit
            Base unit of measurement, or None if itself a base unit of measurement.
        """
        return self.base_unit

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
            if not self.convert_compound:
                if self == to_unit:
                    return 1.0
                elif self.get_base() is None or to_unit.get_base() is None:
                    return Unit.compute_conversion_factor(self, to_unit, self.get_qty_measured())
                elif self.get_base() == to_unit.get_base():
                    return self.prefix.convert_to(to_unit.get_prefix())
                else:  # both units are prefixed
                    return Unit.compute_conversion_factor(self, to_unit, self.get_qty_measured())
            else:
                components_in = self.get_components()
                components_out = to_unit.get_components()

                conversion_factor = 1.0
                for component_in, component_out in zip(
                    components_in, components_out
                ):  # it is assumed components of in and out are in same order
                    conversion_factor *= component_in.convert_to(component_out)
                return conversion_factor

        else:
            simplification_factor, self = self.simplify()
            if (
                self.get_qty_measured() == to_unit.get_qty_measured()
            ):  # TODO: test this branch... potential issues with quantity measured after simplification
                conversion_factor = self.convert_to(to_unit)
                return simplification_factor * conversion_factor

    @staticmethod
    def compute_conversion_factor(unit_in, unit_out, qty_measured):
        """Computes conversion factor from unit_in to unit_out, given (a) They both measure same quantities, and
            (b) they are not compound units.

        Parameters
        ----------
        unit_in : ~pod_lca.units.Unit
            Unit of measurement from which the value will be converted.
        unit_out : ~pod_lca.units.Unit
            Unit of measurement to which the value will be converted.
        qty_measured : str
            Quantity measured by the units of measruements considered.

        Returns
        -------
        float
            Conversion factor to be applied on the value.
        """
        qty = unit_in.get_qty_measured()

        name_in = unit_in.get_base().get_name() if unit_in.get_base() else unit_in.get_name()
        name_out = unit_out.get_base().get_name() if unit_out.get_base() else unit_out.get_name()

        factor_in = UNIT_CONVERSIONS[qty][name_in]
        factor_out = UNIT_CONVERSIONS[qty][name_out]

        if unit_in.get_prefix():
            factor_in /= 10 ** unit_in.get_prefix().get_power()
        if unit_out.get_prefix():
            factor_out /= 10 ** unit_out.get_prefix().get_power()

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
        if not self.convert_compound:
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
        self.convert_compound = total > 1

        # Update metadata
        self.name = "-".join([u.name for u in self.numerator] +
                             [u.name for u in self.denominator])
        self.standard_notation = "".join([u.standard_notation for u in self.numerator]) + \
                                 "".join([f"/{u.standard_notation}" for u in self.denominator])
        self.qty_measured = "-".join([u.qty_measured for u in self.numerator] +
                                     [u.qty_measured for u in self.denominator])
        return factor, self

    def collapse_powers(self, power_rules=POWER_RULES):
        """Collapse repeated units into squared/cubed forms based on a rules dict.
        """
        if not self.convert_compound:
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
        self.convert_compound = total > 1

        self.name = "-".join([u.name for u in self.numerator] +
                             [u.name for u in self.denominator])
        self.standard_notation = "".join([u.standard_notation for u in self.numerator]) + \
                                 "".join([f"/{u.standard_notation}" for u in self.denominator])
        self.qty_measured = "-".join([u.qty_measured for u in self.numerator] +
                                     [u.qty_measured for u in self.denominator])
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


if __name__ == "__main__":
    pass

# TODO: replace == with is, where applicable