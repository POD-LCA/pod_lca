from pod_lca.units import METER, FEET, SQUARE_FEET, KILOGRAM, SQUARE_METER, WATT, HOUR, CUBIC_METER, CUBIC_FEET

unit_1 = SQUARE_FEET
unit_2 = KILOGRAM * WATT / SQUARE_METER

new_unit = unit_1 * unit_2
factor, new_unit_simplified = new_unit.simplify()
print(factor)
print(new_unit_simplified)
# FIXME: fix the loss of dash in the name and qty_measured

unit_1 = CUBIC_FEET / HOUR
unit_2 = KILOGRAM * WATT / CUBIC_METER

new_unit = unit_1 * unit_2
factor, new_unit_simplified = new_unit.simplify()
print(factor)
print(new_unit_simplified)
# FIXME: fix the loss of dash in the name and qty_measured