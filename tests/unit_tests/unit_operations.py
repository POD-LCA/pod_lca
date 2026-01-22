from copy import deepcopy
import pytest

from pod_lca.units import Unit
from pod_lca.units import METER
from pod_lca.units import FEET
from pod_lca.units import SQUARE_METER
from pod_lca.units import SQUARE_FEET
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILOMETER
from pod_lca.units import GRAM
from pod_lca.units import KILO
from pod_lca.units import MEGA
from pod_lca.units import GIGA


@pytest.fixture
def s():
    return Unit.from_basics("second", "s", "time")


def test_simple_units_multiply(s):
    u = METER * s

    assert u.is_compound()
    assert len(u.get_components()) == 2
    assert METER in u.get_components()
    assert s in u.get_components()
    assert not u.denominator


def test_collapse_square_meter():
    u = METER * METER

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == SQUARE_METER
    assert u.name == "square meter"


def test_multiply_with_denominator(s):
    speed = METER / s
    area = METER * METER
    u = speed * area

    assert CUBIC_METER in u.get_components()
    assert s in u.get_components()


def test_cancel_units_with_no_remainder():
    u = METER / METER

    assert u.numerator == []
    assert u.denominator == []
    assert not u.is_compound()
    assert u.name == "dimensionless" or u.name == ""
    assert u.standard_notation == ""


def test_cancel_unit_with_remainder(s):
    u = (METER / s) * s

    assert not u.is_compound()
    assert u == METER


def test_cancel_multiple_components(s):
    u = (METER / s) * (s / METER)

    assert not u.is_compound()
    assert u.name == ""
    assert u.standard_notation == ""


def test_metric_prefix_error():
    class DummyPrefix: ...
    with pytest.raises(TypeError):
        METER * DummyPrefix()


def test_multiply_unit_with_prefix():
    unit = KILO * METER

    assert unit.prefix == KILO
    assert unit.numerator is not None
    assert len(unit.numerator) == 1
    assert unit.numerator[0] is METER
    assert unit.denominator is None or len(KILOMETER.denominator) == 0


def test_prefix_divide():
    u = KILO * METER
    v = KILO * GRAM
    result = u / v

    assert result.prefix is None
    assert METER in result.numerator
    assert GRAM in result.denominator


def test__prefix_multiply():
    result = KILO * MEGA

    assert result.get_symbol() == 'G'
    assert result.get_power() == 9


def test_same_prefix_multiply():
    result = KILO * KILO

    assert result == MEGA
    assert result.get_symbol() == 'M'
    assert result.get_power() == 6


def test_units_with_prefix_multiply():
    u = KILO * METER
    v = KILO * GRAM
    result = u * v

    assert result.prefix == MEGA
    assert METER in result.numerator
    assert GRAM in result.numerator 
    assert result.denominator == []


def test_multiple_components(s):
    u = (KILO * GRAM * METER / s) * (s * METER)
    u = u.simplify()

    assert u.prefix == KILO
    assert GRAM in u.get_components()
    assert s not in u.get_components()
    assert not u.denominator


def test_identity_roundtrip(s):
    u = (METER / s) * s
    v = METER * (s / s)
    u = u.simplify()
    v = v.simplify()

    assert u == v == METER


def test_collapse_single():
    u = deepcopy(METER)
    u.collapse_powers()

    assert u == METER


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

    assert len(u.get_components()) == 2
    assert METER in u.get_components()
    assert FEET in u.get_components()


def test_collapse_after_simplify():
    u = (METER / METER) * (METER * METER)

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == SQUARE_METER


def test_cancel_after_collapse():
    density = GRAM / SQUARE_METER
    area = METER * METER
    result = density * area

    assert len(result.get_components()) == 1
    assert result.get_components()[0] == GRAM
    assert result.denominator is None or len(result.denominator) == 0
    assert result.name == "gram"
    assert result.standard_notation == "g"
    assert result.qty_measured == "mass"
    assert not result.is_compound()


def test_kilo_meter():

    assert KILOMETER.prefix == KILO
    assert KILOMETER.numerator is not None
    assert len(KILOMETER.numerator) == 1
    assert KILOMETER.numerator[0] is METER
    assert KILOMETER.denominator is None or len(KILOMETER.denominator) == 0
