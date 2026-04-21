__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


class Quantity(object):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __format__(self, spec):
        formatted = format(self.value, spec or ".4f")
        return f"{formatted}"

    def __hash__(self):
        return hash((self.value, self.unit))

    def __str__(self):
        return '{} ({})'.format(self.value, self.unit.name)

    def __repr__(self):
        return '{} ({})'.format(self.value, self.unit.name)

    def __round__(self, ndigits=None):
        return Quantity(round(self.value, ndigits), self.unit)

    def __add__(self, val):
        if isinstance(val, Quantity):
            if self.unit == val.unit:
                return Quantity(self.value + val.value, self.unit)
            else:
                try:
                    val = val.unit.convert_to(self.unit) * val.value
                    return Quantity(self.value + val, self.unit)
                except:
                    raise TypeError(f"unsupported operand type(s) for + {self.unit.name} and {val.unit.name}")
        else:
            # self.value += val # TODO: This is mathematically incorrect... do we want this to be allowed...
            # return self
            return Quantity(self.value + val, self.unit)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, val):
        if isinstance(val, Quantity):
            if self.unit == val.unit:
                return Quantity(self.value - val.value, self.unit)
            else:
                try:
                    val = val.unit.convert_to(self.unit) * val.value
                    return Quantity(self.value - val, self.unit)
                except:
                    raise TypeError(f"unsupported operand type(s) for - {self.unit.name} and {val.unit.name}")
        else:
            # self.value -= val # TODO: This is mathematically incorrect... do we want this to be allowed...
            # return self
            return Quantity(self.value - val, self.unit)

    def __rsub__(self, val):
        if isinstance(val, Quantity):
            if self.unit == val.unit:
                return Quantity(val.value - self.value, self.unit)
            else:
                try:
                    val = val.unit.convert_to(self.unit) * val.value
                    return Quantity(val - self.value, self.unit)
                except:
                    raise TypeError(f"unsupported operand type(s) for - {self.unit.name} and {val.unit.name}")
        else:
            # self.value = val - self.value # TODO: This is mathematically incorrect... do we want this to be allowed...
            # return self
            return Quantity(val - self.value, self.unit)

    def __mul__(self, val):
        if isinstance(val, Quantity):
            value = self.value * val.value
            unit = self.unit * val.unit
            unit, factor = unit.simplify()
            return Quantity(value * factor, unit)
        else:
            return Quantity(self.value * val, self.unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, val):
        if isinstance(val, Quantity):
            value = self.value / val.value
            unit = self.unit / val.unit
            unit, factor = unit.simplify()
            return Quantity(value * factor, unit)
        else:
            return Quantity(self.value / val, self.unit)

    def __rtruediv__(self, val):
        if isinstance(val, Quantity):
            if self.unit.qty_measured == val.unit.qty_measured:
                value  = (val.value * val.unit.convert_to(self.unit)) / self.value
                unit = val.unit / self.unit
            else:
                value = val.value / self.value
                unit = val.unit / self.unit
            return Quantity(value, unit)
        else:
            return Quantity(val / self.value, 1 / self.unit)

    def __iadd__(self, val):
        return self + val

    def __pow__(self, val):
        if isinstance(val, float) or isinstance(val, int):
            return Quantity(self.value**val, self.unit)
        else:
            raise TypeError(f"unsupported operand type(s) for __pow__ {self.unit.name} and {type(val)}")

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

    def __neg__(self):
        return Quantity(-self.value, self.unit)
        
    def convert_to(self, unit):
        if self.unit.qty_measured == unit.qty_measured:
            value  = self.value * self.unit.convert_to(unit)
            return Quantity(value, unit)
        else:
            raise TypeError(f"unsupported conversion from {self.unit.name} to {unit.name}.")
        
    def invert(self):
        return Quantity(1 / self.value, 1 / self.unit)

if __name__ == '__main__':
    pass
