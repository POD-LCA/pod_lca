__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from enum import Enum, auto

from ..units import UNIT_CONVERSIONS
from ..units import UNIT_REGISTRY


class UnitConversionException:
    def applies(self, unit_in, unit_out):
        raise NotImplementedError

    def apply(self, unit_in, unit_out):
        """
        Returns:
            factor: float
            ops: list[UnitOp]
        """
        raise NotImplementedError


class UnitOp:
    def __init__(self, side, remove=None, add=None):
        self.side = side
        self.remove = remove or {}
        self.add = add or {}


class UnitSide(Enum):
    IN = auto()
    OUT = auto()


class ImperialEnergyException(UnitConversionException):

    IMPERIAL_ENERGY_UNITS = {"British Thermal Unit", "therm"}

    def _find_energy_unit(self, unit):
        for component in unit.units:
            if component.qty_measured == "energy":
                return component
        return None

    def applies(self, unit_in, unit_out):
        in_energy = self._find_energy_unit(unit_in)
        out_energy = self._find_energy_unit(unit_out)

        if not in_energy or not out_energy:
            return False

        return (
            (in_energy.get_name() in self.IMPERIAL_ENERGY_UNITS)
            !=
            (out_energy.get_name() in self.IMPERIAL_ENERGY_UNITS)
        )

    def apply(self, unit_in, unit_out):
        factor = 1
        ops = []

        for unit_list, side in zip([unit_in.units, unit_out.units], [UnitSide.IN, UnitSide.OUT]):
            for component, power in unit_list.items():
                component_name = component.get_name()
                if component_name in type(self).IMPERIAL_ENERGY_UNITS:
                    if side == UnitSide.IN:
                        factor /= (UNIT_CONVERSIONS["energy"][component_name]) ** power
                    else:
                        factor *= (UNIT_CONVERSIONS["energy"][component_name]) ** power

                    ops.append(
                        UnitOp(
                            side=side,
                            remove={component: power},
                            add={UNIT_REGISTRY["watt-hour"]: power}
                        )
                    )

        return factor, ops
