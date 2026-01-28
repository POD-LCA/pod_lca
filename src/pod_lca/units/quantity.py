__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.units import Unit


class Quantity(object):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return '{} ({})'.format(self.value, self.unit.name)

    def __add__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                val = val.unit.convert_to(self.unit) * val.value
                return Quantity(self.value + val, self.unit)
            else:
                raise TypeError(f"unsupported operand type(s) for + {self.unit.name} and {val.unit.name}")
        else:
            self.value += val
            return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                val = val.unit.convert_to(self.unit) * val.value
                return Quantity(self.value - val, self.unit)
            else:
                raise TypeError(f"unsupported operand type(s) for - {self.unit.name} and {val.unit.name}")
        else:
            self.value -= val
            return self

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = self.value * (val.value * val.unit.convert_to(self.unit))
                unit = self.unit * self.unit
            else:
                value = self.value * val.value
                unit = self.unit * val.unit
            return Quantity(value, unit)
        else:
            return Quantity(self.value * val, self.unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = self.value * (val.value * val.unit.convert_to(self.unit))
                unit = self.unit / self.unit
            else:
                value = self.value / val.value
                unit = self.unit / val.unit
            return Quantity(value, unit)
        else:
            return Quantity(self.value / val, self.unit)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __iadd__(self, val):
        return self + val
    
    def __gt__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value > value
            else:
                raise TypeError(f"unsupported operand type(s) for > {self.unit.name} and {val.unit.name}")
        else:
            return self.value > val
    
    def __ge__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value >= value
            else:
                raise TypeError(f"unsupported operand type(s) for >= {self.unit.name} and {val.unit.name}")
        else:
            return self.value >= val

    def __lt__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value < value
            else:
                raise TypeError(f"unsupported operand type(s) for < {self.unit.name} and {val.unit.name}")
        else:
            return self.value < val

    def __le__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value <= value
            else:
                raise TypeError(f"unsupported operand type(s) for <= {self.unit.name} and {val.unit.name}")
        else:
            return self.value <= val

    def __eq__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value == value
            else:
                raise TypeError(f"unsupported operand type(s) for == {self.unit.name} and {val.unit.name}")
        else:
            return self.value == val

    def __ne__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = val.value * val.unit.convert_to(self.unit)
                return self.value != value
            else:
                raise TypeError(f"unsupported operand type(s) for != {self.unit.name} and {val.unit.name}")
        else:
            return self.value != val

    def __float__(self):
        return float(self.value)
    
    def __int__(self):
        return int(self.value)

    def convert_to(self, unit):
        if self.unit.qty_measured == unit.qty_measured:
            value  = self.value * self.unit.convert_to(unit)
            return Quantity(value, unit)
        else:
            raise TypeError(f"unsupported conversion from {self.unit.name} to {unit.name}.")
        
    def invert(self):
        return Quantity(1 / self.value, 1 / self.unit)

if __name__ == '__main__':


    from pod_lca.units import METER, INCH, MILE, M_TON, CUBIC_METER
    from pod_lca.units import KILOGRAM, GRAM, SQUARE_METER, KELVIN, WATT


    for i in range(50): print('')

    a = Quantity(0, METER)
    b = Quantity(1, INCH)
    c = a + b

    c = b.convert_to(METER)
    print(c)

    