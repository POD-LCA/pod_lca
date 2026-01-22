import pytest
from pod_lca.units import Unit, MetricPrefix
from pod_lca.units import KILO
from pod_lca.units import INCH
from pod_lca.units import CENTI
from pod_lca.units import UNIT_CONVERSIONS
from pod_lca.units import METER
from pod_lca.units import BTU
from pod_lca.units import THERM
from pod_lca.units import WATT_HOUR
from pod_lca.units import MILE
from pod_lca.units import JOULE 
from pod_lca.units import FEET
from pod_lca.units import YARD
from pod_lca.units import NAUTICAL_MILE   

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def s():
    return Unit.from_basics("second", "s", "time")

@pytest.fixture
def g():
    return Unit.from_basics("gram", "g", "mass")


def test_simple_identity():
    assert METER.convert_to(METER) == 1.0


def test_mile_to_meter():
    assert MILE.convert_to(METER) == pytest.approx(1609.344)
    

def test_prefix_simple_conversion():
    km = KILO * METER
    cm = CENTI * METER

    assert km.convert_to(METER) == pytest.approx(1000)
    assert METER.convert_to(km) == pytest.approx(0.001)
    assert cm.convert_to(METER) == pytest.approx(0.01)
    assert cm.convert_to(km) == pytest.approx(0.00001)


def test_prefix_only_compound():
    km2 = (KILO * METER) * METER

    assert km2.prefix == KILO
    assert len(km2.numerator) == 1
    assert km2.is_compound()


def test_compound_conversion_density(g):
    kg_m2 = (KILO * g) / (METER * METER)
    g_cm2 = g / ((CENTI * METER) * (CENTI * METER))
    f = kg_m2.convert_to(g_cm2)

    assert f == pytest.approx(0.1)


def test_compound_conversion_velocity(s):
    mps = METER / s
    cmps = (CENTI * METER) / s

    assert mps.convert_to(cmps) == pytest.approx(100)


def test_km_over_m():
    km = KILO * METER
    u = km / METER
    factor, simplified = u.simplify(True)

    assert factor == pytest.approx(1000)
    assert simplified.numerator == []
    assert simplified.denominator == []


def test_cubic_meter_conversion():
    u = METER * METER * METER
    v = Unit.from_basics("cubic meter", "m3", "volume")

    assert u.convert_to(v) == 1.0


def test_structural_identity():
    km1 = KILO * METER
    km2 = KILO * METER

    assert km1 == km2
    assert km1 is not km2


def test_basic_unit_not_mutated():
    _ = KILO * METER

    assert METER.prefix is None
    assert METER.numerator == [METER]
    assert METER.denominator == []

# -------------------------
# Length conversions
# -------------------------

def test_mile_to_meter():
    assert MILE.convert_to(METER) == pytest.approx(1609.344)


def test_meter_to_mile():
    assert METER.convert_to(MILE) == pytest.approx(1 / 1609.344)


def test_feet_to_inch():
    assert FEET.convert_to(INCH) == pytest.approx(12)


def test_yard_to_feet():
    assert YARD.convert_to(FEET) == pytest.approx(3)


def test_nautical_mile_to_mile():
    assert NAUTICAL_MILE.convert_to(MILE) == pytest.approx(1 / 1.151)


def test_length_identity():
    assert METER.convert_to(METER) == 1.0


# -------------------------
# Energy conversions
# -------------------------

def test_wh_to_joule():
    assert WATT_HOUR.convert_to(JOULE) == pytest.approx(3600)


def test_joule_to_wh():
    assert JOULE.convert_to(WATT_HOUR) == pytest.approx(1 / 3600)


def test_btu_to_wh():
    assert BTU.convert_to(WATT_HOUR) == pytest.approx(1 / (1.05505585262 * 1000 * 3600))


def test_wh_to_btu():
    assert WATT_HOUR.convert_to(BTU) == pytest.approx(1.05505585262 * 1000 * 3600)


def test_therm_to_wh():
    assert THERM.convert_to(WATT_HOUR) == pytest.approx(1.054804e08 / 3600)


# -------------------------
# Compound conversions
# -------------------------

def test_speed_conversion():
    mph = MILE / Unit.from_basics("hour", "h", "time")
    mps = METER / Unit.from_basics("second", "s", "time")

    factor = mph.convert_to(mps)
    assert factor == pytest.approx(0.44704, rel=1e-4)


def test_energy_density_conversion():
    wh_m2 = WATT_HOUR / (METER * METER)
    j_m2 = JOULE / (METER * METER)

    assert wh_m2.convert_to(j_m2) == pytest.approx(3600)