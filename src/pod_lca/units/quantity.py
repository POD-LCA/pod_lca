__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


class Quantity(object):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return '{} ({})'.format(self.value, self.unit.name)

    def __add__(self, val):
        f = val.unit.convert_to(self.unit)
        return Quantity(self.value + (val.value * f), self.unit)

    def __sub__(self, val):
        f = val.unit.convert_to(self.unit)
        return Quantity(self.value - (val.value * f), self.unit)

    def __mul__(self, val):
        f = val.unit.convert_to(self.unit)
        return Quantity(self.value * (val.value * f), self.unit)

    def __truediv__(self, val):
        f = val.unit.convert_to(self.unit)
        return Quantity(self.value / (val.value * f), self.unit)


if __name__ == '__main__':

    from pod_lca.units import METER, INCH, MILE

    for i in range(50): print('')

    a = Quantity(1, METER)
    b = Quantity(1, INCH)
    c = Quantity(1, MILE)

    print(a + b * c)