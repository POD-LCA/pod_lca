from copy import deepcopy
import pytest

from pod_lca.units import Unit
from pod_lca.units import METER, FEET, SQUARE_METER, SQUARE_FEET, CUBIC_METER, CUBIC_FEET, KILOGRAM


@pytest.fixture
def m():
    return Unit.from_basics("meter", "m", "length")

@pytest.fixture
def m3():
    return Unit.from_basics("cubic meter", "m3", "volume")

@pytest.fixture
def s():
    return Unit.from_basics("second", "s", "time")

@pytest.fixture
def kg():
    return Unit.from_basics("kilogram", "kg", "mass")


def test_simple_multiply(m, s):
    u = m * s
    assert u.convert_compound
    assert len(u.get_components()) == 2
    assert m in u.get_components()
    assert s in u.get_components()
    assert not u.denominator

def test_multiply_with_denominator(m, s, m3):
    speed = m / s
    area = m * m
    u = speed * area

    assert m3 in u.get_components()
    assert s in u.get_components()

def test_cancel_same_unit(m, s):
    u = (m / s) * s
    assert not u.convert_compound
    assert u == m

def test_double_cancel(m, s):
    u = (m / s) * (s / m)
    assert not u.convert_compound
    assert u.name == ""
    assert u.standard_notation == ""

def test_simplify_basic(m, s):
    u = (m / s) * s
    factor, new = u.simplify()
    assert factor == 1.0
    assert new == m

def test_multiple_components(m, s, kg):
    u = (kg * m / s) * (s * m)
    _, u = u.simplify()

    assert kg in u.get_components()
    assert s not in u.get_components()
    assert not u.denominator

def test_simplify_no_change(m, s):
    u = m * s
    factor, new = u.simplify()
    assert factor == 1.0
    assert new == u

def test_metric_prefix_error(m):
    class DummyPrefix: ...
    with pytest.raises(TypeError):
        m * DummyPrefix()

def test_identity_roundtrip(m, s):
    u = (m / s) * s
    v = m * (s / s)
    _, u = u.simplify()
    _, v = v.simplify()
    assert u == v == m

def test_collapse_single():
    u = deepcopy(METER)
    u.collapse_powers()
    assert u == METER

def test_collapse_square_meter():
    u = METER * METER
    u.collapse_powers()
    assert len(u.get_components()) == 1
    assert u.get_components()[0] == SQUARE_METER
    assert u.name == "square meter"

def test_collapse_cubic_meter():
    u = METER * METER * METER
    assert len(u.get_components()) == 1
    assert u.get_components()[0] == CUBIC_METER
    assert u.name == "cubic meter"

def test_collapse_square_feet():
    u = FEET * FEET
    assert len(u.get_components()) == 1
    assert u.get_components()[0] == SQUARE_FEET
    assert u.name == "square feet"

def test_collapse_mixed_units_no_change():
    u = METER * FEET
    # different units should not collapse
    assert len(u.get_components()) == 2
    assert METER in u.get_components()
    assert FEET in u.get_components()

def test_collapse_after_simplify():
    # e.g., (meter / meter) * (meter*meter)
    u = (METER / METER) * (METER * METER)
    _, u = u.simplify()  # cancels one meter in numerator/denominator
    u.collapse_powers()
    assert len(u.get_components()) == 1
    assert u.get_components()[0] == SQUARE_METER

def test_mul_automatically_collapses():
    u = METER * METER
    # __mul__ should automatically collapse repeated units
    v = deepcopy(u)  # trigger __mul__ internally
    assert v.get_components()[0] == SQUARE_METER

def test_mul_mixed_units():
    u = METER * FEET
    v = deepcopy(u)
    # should not collapse mixed units
    assert len(v.get_components()) == 2
    assert METER in v.get_components()
    assert FEET in v.get_components()

def test_density_times_area():
    # Density: kg / m²
    density = KILOGRAM / SQUARE_METER

    # Area: m²
    area = SQUARE_METER

    # Multiply density by area: should return kg
    result = density * area

    # Collapse powers and simplify automatically
    # Components should contain only KG
    assert len(result.get_components()) == 1
    assert result.get_components()[0] == KILOGRAM

    # Denominator should be None
    assert result.denominator is None or len(result.denominator) == 0

    # Name, standard notation, qty_measured
    assert result.name == "kilogram"
    assert result.standard_notation == "kg"
    assert result.qty_measured == "mass"

    # Not a compound unit anymore
    assert not result.convert_compound

def test_meter_divided_by_meter(m):
    u = m / m

    assert u.numerator == []
    assert u.denominator is None

    assert not u.convert_compound

    assert u.name == "dimensionless" or u.name == ""
    assert u.standard_notation == ""