# Common Units

The basics units are defined for this package, based on common units of measurements used in life cycle assessments. The units include both metric and imperial units of measurements. The units of measurements defined are categoriesed based on the quantity measured (e.g., 'time', 'length').

If a user want to create a new basic unit, they are encouraged to use the Unit.from_basics(name, standard_notation, qty_measured) method. For conversions to work as expected, they need to add the corresponding conversion factor to UNIT_CONVERSIONS, keyed by the measurement category and the standard_notation. The values in UNIT_CONVERSIONS[category] are equivalent. The conversion factors defined are based on references [1] and [2] below.

The units presented here can be used to create new units of measurements. These can be derived by multiplication and/or division of units by other units or metric prefixes, where applicable.

```python
KILOMETER = KILO * METER
UNIT_WEIGHT = KILOGRAM / CUBIC_METER
```

The list below defines the derived units of KILOMETER and KILOGRAM as these are common units. The users are encouraged to add their commonly used units here and import from this central source.

A method is defined for obtaining the conversion factor for converting a unit to another within the same category. In this note the special case of 'area' and 'volume', when conversion across metric and imperial units are envisaged. Although you can define a new unit of measurement (say) METER \* METER this would be categorized as 'length-length' and thus cannot be converted to ACRE, which is categorized as 'area'. Thus, the users are encouraged to use the predeefined unit of SQUARE_METER instead. The similar is applied to 'volume' calculations

## Time

| Unit Object Name   | Unit Name   | Standard Notation   | Conversion Factor   |
|--------------------|-------------|---------------------|---------------------|
| SECOND             | second      | sec                 | 3600                |
| MINUTE             | minute      | min                 | 60                  |
| HOUR               | hour        | hr                  | 1                   |
| DAY                | day         | d                   | 1 / 24              |

## Mass

| Unit Object Name   | Unit Name   | Standard Notation   |   Conversion Factor |
|--------------------|-------------|---------------------|---------------------|
| GRAM               | gram        | g                   |       907185        |
| M_TON              | metric Ton  | t                   |            0.907185 |
| S_TON              | short Ton   | tn                  |            1        |
| POUND              | pound       | lb                  |         2000        |
| OUNCE              | ounce       | oz                  |        32000        |

KILOGRAM = KILO \* GRAM

Reference: [1] pp. C-19/20

## Length

| Unit Object Name   | Unit Name     | Standard Notation   |   Conversion Factor |
|--------------------|---------------|---------------------|---------------------|
| METER              | meter         | m                   |            1609.34  |
| FEET               | feet          | ft                  |            5280     |
| INCH               | inch          | in                  |           63360     |
| YARD               | yard          | yd                  |            1760     |
| MILE               | mile          | mi                  |               1     |
| NAUTICAL_MILE      | nautical mile | nmi                 |               1.151 |

KILOMETER = KILO \* METER

Reference: [1] pp. C-10

## Transportation

TON_KILOMETER = M_TON \* KILOMETER

TON_MILE = M_TON \* MILE

## Area

| Unit Object Name   | Unit Name    | Standard Notation   |   Conversion Factor |
|--------------------|--------------|---------------------|---------------------|
| SQUARE_METER       | square meter | m2                  |         4046.86     |
| SQUARE_FEET        | square feet  | ft2                 |        43560        |
| ACRE               | acre         | acre                |            1        |
| HECTARE            | hectare      | ha                  |            0.404686 |

Reference: [1] pp. C-14/15

## Volume

| Unit Object Name   | Unit Name   | Standard Notation   | Conversion Factor          |
|--------------------|-------------|---------------------|----------------------------|
| LITER              | liter       | l                   | 28.316846592               |
| US_GALLON          | US gallon   | US gal              | 28.316846592 / 3.785411784 |
| CUBIC_METER        | cubic meter | m3                  | 0.028316846592             |
| CUBIC_FEET         | cubic feet  | ft3                 | 1.0                        |

Reference: [1] pp. C-17/18

## Power

| Unit Object Name   | Unit Name   | Standard Notation   |   Conversion Factor |
|--------------------|-------------|---------------------|---------------------|
| WATT               | watt        | W                   |                   1 |

## Energy

| Unit Object Name   | Unit Name   | Standard Notation   | Conversion Factor   |
|--------------------|-------------|---------------------|---------------------|
| WATT_HOUR          | watt-hour   | Wh                  | 1.0                 |
| JOULE              | joule       | J                   | 3600                |
| THERM              | therm       | thm                 | 3600 / 1.054804e+08 |

Reference: [2] pp. 55

## Count

| Unit Object Name   | Unit Name   | Standard Notation   |   Conversion Factor |
|--------------------|-------------|---------------------|---------------------|
| ITEM               | item        | Item(s)             |                  12 |
| DOZEN              | dozen       | Doz                 |                   1 |

## Carbon Storage

| Unit Object Name   | Unit Name            | Standard Notation   | Conversion Factor   |
|--------------------|----------------------|---------------------|---------------------|
| KG_CARBON          | kg of Carbon         | kg C                | 1.0                 |
| KG_CARBON_DIOXIDE  | kg of Carbon dioxide | kg CO2              | 44.01 / 12.01       |

References:

[1]  National Institute of Standards and Technology (NIST) Handbook 44 (2024). Specifications, Tolerances, and Other Technical Requirements for Weighing and Measuring Devices.

[2]  National Institute of Standards and Technology (NIST) Special Publication 811 (2008). Guide for the Use of the International System of Units (SI)
