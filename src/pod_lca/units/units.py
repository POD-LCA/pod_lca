__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from copy import deepcopy
from itertools import combinations
from math import log10

from ..units import UNIT_CONVERSIONS, ALL_PREFIXES
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
        self.convert_compound = False
        self.components = None
        self.denominator = None

    def __str__(self):
        return f"Unit {self.get_name()} ({self.get_standard_notation()}) measuring {self.get_qty_measured()}."

    def __eq__(self, other):
        if isinstance(other, Unit):
            test_1 = other.get_name() == self.get_name()
            test_2 = self.get_standard_notation() == other.get_standard_notation()
            test_3 = self.get_qty_measured() == other.get_qty_measured()
            return bool(test_1 * test_2 * test_3)
        return NotImplemented

    def __mul__(self, other):
        """Multiplication of units by other units."""
        if isinstance(other, Unit):
            # check for cancelling units
            other_copy = deepcopy(other)
            self_copy = deepcopy(self)
            parts_self = self.get_components() if self_copy.convert_compound else [self_copy]
            parts_other = other_copy.get_components() if other_copy.convert_compound else [other_copy]
            for component_self in parts_self:
                for component_other in parts_other:
                    if component_self == component_other:
                        return_self = False
                        return_other = False
                        # update other
                        if other_copy == component_other:
                            return_self = True
                        else:
                            if other_copy.denominator is not None:
                                if component_other in other_copy.denominator:
                                    other_copy.name = other_copy.get_name().replace(
                                        " per " + component_other.get_name(), ""
                                    )
                                    other_copy.standard_notation = other_copy.get_standard_notation().replace(
                                        "/" + component_other.get_standard_notation(), ""
                                    )
                                    other_copy.qty_measured = other_copy.get_qty_measured().replace(
                                        " per " + component_other.get_qty_measured(), ""
                                    )
                                    other_copy.components.remove(component_other)
                                    other_copy.convert_compound = False if len(other_copy.components) > 0 else True
                                    other_copy.denominator = None
                                else:
                                    other_copy.name = other_copy.get_name().replace(
                                        "-" + component_other.get_name(), ""
                                    )
                                    other_copy.standard_notation = other_copy.get_standard_notation().replace(
                                        component_other.get_standard_notation(), ""
                                    )
                                    other_copy.qty_measured = other_copy.get_qty_measured().replace(
                                        "-" + component_other.get_qty_measured(), ""
                                    )
                                    other_copy.components.remove(component_other)
                                    other_copy.convert_compound = False if len(other_copy.components) > 0 else True
                        # update self
                        if self_copy == component_self:
                            return_other = True
                        else:
                            if self_copy.denominator is not None:
                                if component_self in self_copy.denominator:
                                    self_copy.name = self_copy.get_name().replace(
                                        " per " + component_self.get_name(), ""
                                    )
                                    self_copy.standard_notation = self_copy.get_standard_notation().replace(
                                        "/" + component_self.get_standard_notation(), ""
                                    )
                                    self_copy.qty_measured = self_copy.get_qty_measured().replace(
                                        " per " + component_self.get_qty_measured(), ""
                                    )
                                    self_copy.components.remove(component_self)
                                    self_copy.convert_compound = False if len(self_copy.components) > 0 else True
                                    self_copy.denominator = None
                                else:
                                    self_copy.name = self_copy.get_name().replace("-" + component_self.get_name(), "")
                                    self_copy.standard_notation = self_copy.get_standard_notation().replace(
                                        component_self.get_standard_notation(), ""
                                    )
                                    self_copy.qty_measured = self_copy.get_qty_measured().replace(
                                        "-" + component_self.get_qty_measured(), ""
                                    )
                                    self_copy.components.remove(component_self)
                                    self_copy.convert_compound = False if len(self_copy.components) > 0 else True

                        if return_self:
                            if not self_copy.convert_compound:
                                return self_copy.components[0]
                            return self_copy
                        elif return_other:
                            if not other_copy.convert_compound:
                                return other_copy.components[0]
                            return other_copy

            # parts post cancellation being added
            name = self_copy.get_name() + "-" + other_copy.get_name()
            standard_notation = self_copy.get_standard_notation() + other_copy.get_standard_notation()
            qty_measured = self_copy.get_qty_measured() + "-" + other_copy.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.convert_compound = True
            if self_copy.convert_compound and other_copy.convert_compound:
                newUnit.components = self_copy.components + other_copy.components
                if self_copy.denominator is not None and other_copy.denominator is not None:
                    newUnit.denominator = self_copy.denominator + other_copy.denominator
                elif self_copy.denominator is not None and other_copy.denominator is None:
                    newUnit.denominator = self_copy.denominator
                elif self_copy.denominator is None and other_copy.denominator is not None:
                    newUnit.denominator = other_copy.denominator
                else:
                    newUnit.denominator = None
            elif self_copy.convert_compound and not other_copy.convert_compound:
                newUnit.components = self_copy.components + [other_copy]
                if self_copy.denominator is not None:
                    newUnit.denominator = self_copy.denominator
            elif not self_copy.convert_compound and other_copy.convert_compound:
                newUnit.components = [self_copy] + other_copy.components
                if other_copy.denominator is not None:
                    newUnit.denominator = other_copy.denominator
            else:
                newUnit.components = [self_copy, other_copy]

            return newUnit

        elif isinstance(other, MetricPrefix):
            raise TypeError("Metric prefixes not defined for post multiplication.")

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
        """Devision of units by other units."""
        if isinstance(other, Unit):
            name = self.get_name() + " per " + other.get_name()
            standard_notation = self.get_standard_notation() + "/" + other.get_standard_notation()
            qty_measured = self.get_qty_measured() + " per " + other.get_qty_measured()

            newUnit = Unit.from_basics(name, standard_notation, qty_measured)
            newUnit.convert_compound = True
            newUnit.components = [self, other]
            newUnit.denominator = [other]

            return newUnit

        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {self.__class__.__name__} and {other.__class__.__name__}"
            )

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
        return self.components

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
            else:
                raise TypeError(
                    f"{self.get_name()} of dimensions {self.get_qty_measured()} and {to_unit.get_name()} of dimensions {to_unit.get_qty_measured()} are incompatible."
                )

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
        inverse_flag = False
        unit_in_name = unit_in.get_name() if unit_in.get_base() is None else unit_in.get_base().get_name()
        unit_out_name = unit_out.get_name() if unit_out.get_base() is None else unit_out.get_base().get_name()

        if qty_measured.startswith("per "):
            inverse_flag = True
            qty_measured = qty_measured.replace("per ", "")
            unit_in_name = unit_in_name.replace("per ", "")
            unit_out_name = unit_out_name.replace("per ", "")

        if unit_in.get_base() is None:
            factor_in = UNIT_CONVERSIONS[qty_measured][unit_in_name]
        else:
            factor_in = UNIT_CONVERSIONS[qty_measured][unit_in_name] / 10 ** (unit_in.get_prefix().get_power())

        if unit_out.get_base() is None:
            factor_out = UNIT_CONVERSIONS[qty_measured][unit_out_name]
        else:
            factor_out = UNIT_CONVERSIONS[qty_measured][unit_out_name] / 10 ** (unit_out.get_prefix().get_power())

        conversion_factor = factor_out / factor_in
        if inverse_flag:
            conversion_factor = 1 / conversion_factor

        return conversion_factor

    def simplify(self):
        """Simplify a compound unit by cancelling common components in numerator and denominator.

        Returns
        -------
        :class:`float`
            Conversion factor resulting from the simplification.
        :class:`~pod_lca.units.Unit`
            Simplified unit.
        """
        if self.convert_compound:
            parts = self.get_components()
            for component in combinations(parts, 2):
                if component[0] in self.denominator and component[1] in self.denominator:
                    continue
                elif component[0] not in self.denominator and component[1] not in self.denominator:
                    continue
                else:
                    if component[0].qty_measured != component[1].qty_measured:
                        continue
                    denominator = component[0] if component[0] in self.denominator else component[1]
                    numerator = component[1] if denominator == component[0] else component[0]

                    factor = numerator.convert_to(denominator)

                    self.name = self.name.replace(numerator.get_name(), "").replace(
                        " per " + denominator.get_name(), ""
                    )
                    self.standard_notation = self.standard_notation.replace(
                        numerator.get_standard_notation(), ""
                    ).replace("/" + denominator.get_standard_notation(), "")
                    self.qty_measured = self.qty_measured.replace(numerator.get_qty_measured(), "").replace(" per ", "")

                    if "-" in self.name:
                        self.name = self.name.replace("-", "")
                        self.qty_measured = self.qty_measured.replace("-", "")

                    self.components.remove(numerator)
                    self.components.remove(denominator)
                    self.denominator.remove(denominator)

                    self.convert_compound = False if len(self.components) < 2 else True
                    if len(self.components) == 1:
                        self = self.components[0]

                    if self.convert_compound:
                        factor, self = self.simplify()

                    return factor, self

            return 1.0, self
        else:
            return 1.0, self


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
