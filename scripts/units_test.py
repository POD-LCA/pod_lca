from pod_lca.units import SQUARE_FEET, KILOGRAM, SQUARE_METER, WATT, HOUR, CUBIC_METER, CUBIC_FEET, METER, WATT_HOUR, KILO

unit_1 = KILOGRAM / CUBIC_METER
unit_2 = CUBIC_METER

new_unit = KILO * WATT_HOUR / SQUARE_FEET
print(new_unit)

# factor, new_unit_simplified = new_unit.simplify()
# print(factor)
# print(new_unit_simplified)
# # FIXME: fix the loss of dash in the name and qty_measured

# unit_1 = CUBIC_FEET / HOUR
# unit_2 = KILOGRAM * WATT / CUBIC_METER

# new_unit = unit_1 * unit_2
# factor, new_unit_simplified = new_unit.simplify()
# print(factor)
# print(new_unit_simplified)
# # FIXME: fix the loss of dash in the name and qty_measured
