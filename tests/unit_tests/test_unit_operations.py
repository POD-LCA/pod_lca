from copy import deepcopy
import pytest

from pod_lca.units import Unit
from pod_lca.units import MetricPrefix


@pytest.fixture
def second():
    return Unit.from_basics("second", "s", "time")

@pytest.fixture
def meter():
    return Unit.from_basics("meter", "m", "length")

@pytest.fixture
def feet():
    return Unit.from_basics("feet", "ft", "length")

@pytest.fixture
def gram():
    return Unit.from_basics("gram", "g", "mass")

@pytest.fixture
def watt():
    return Unit.from_basics("watt", "W", "power")

@pytest.fixture
def sqmeter():
    return Unit.from_basics("square meter", "m²", "area")

@pytest.fixture
def sqfeet():
    return Unit.from_basics("square feet", "ft²", "area")

@pytest.fixture
def cubicmeter():
    return Unit.from_basics("cubic meter", "m³", "volume")

@pytest.fixture
def kilo():
    return MetricPrefix("kilo", "k", 3)

@pytest.fixture
def mega():
    return MetricPrefix("mega", "M", 6)

@pytest.fixture
def centi():
    return MetricPrefix("kilo", "c", -2)

@pytest.fixture
def deka():
    return MetricPrefix("deka", "da", 1)

@pytest.fixture
def deci():
    return MetricPrefix("deci", "d", -1)

def test_equivalence(meter):

    assert meter ==  meter

def test_equivalence_order(meter, second):

    assert (meter * second) == (second * meter)

def test_simple_units_multiply(second, meter):
    u = meter * second

    assert u.is_compound()
    assert len(u.get_components()) == 2
    assert meter in u.get_components()
    assert second in u.get_components()
    assert not u.denominator


def test_collapse_square_meter(meter, sqmeter):
    u = meter * meter

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == sqmeter
    assert u.name == "square meter"


def test_multiply_with_denominator(meter, second, cubicmeter):
    speed = meter / second
    area = meter * meter
    u = speed * area

    assert cubicmeter in u.get_components()
    assert second in u.get_components()

def inverse_unit(meter):
    u = 1 / meter

    assert u.numerator == []
    assert meter in u.denominator

def test_cancel_units_with_no_remainder(meter):
    u = meter / meter

    assert u.numerator == []
    assert u.denominator == []
    assert not u.is_compound()
    assert u.name == "dimensionless" or u.name == ""
    assert u.standard_notation == ""


def test_cancel_unit_with_remainder(meter, second):
    u = (meter / second) * second

    assert not u.is_compound()
    assert u == meter


def test_cancel_multiple_components(meter, second):
    u = (meter / second) * (second / meter)

    assert not u.is_compound()
    assert u.name == ""
    assert u.standard_notation == ""


def test_metric_prefix_error(meter):
    class DummyPrefix: ...
    with pytest.raises(TypeError):
        meter * DummyPrefix()


def test_multiply_unit_with_prefix(meter, kilo):
    unit = kilo * meter

    assert unit.prefix == kilo
    assert unit.numerator is not None
    assert len(unit.numerator) == 1
    assert unit.numerator[0] is meter
    assert unit.denominator == []

def test_prefix_divide(meter, gram, kilo):
    u = kilo * meter
    v = kilo * gram
    result = u / v

    assert result.prefix is None
    assert meter in result.numerator
    assert gram in result.denominator

def test_prefix_resulting_non_standard(meter, centi):
    v = centi * meter
    result = v * v

    assert result.prefix is not None
    assert result.prefix.get_power() == -4
    assert len(result.numerator) > 0
    assert result.denominator == []

def test_prefix_resulting_standard(meter, gram, centi, deka, deci):
    u = deka * gram
    v = centi * meter
    result = u * v

    assert result.prefix is not None
    assert result.prefix.get_power() == -1
    assert result.prefix == deci


def test__prefix_multiply(kilo, mega):
    result = kilo * mega

    assert result.get_symbol() == 'G'
    assert result.get_power() == 9


def test_same_prefix_multiply(kilo, mega):
    result = kilo * kilo

    assert result == mega
    assert result.get_symbol() == 'M'
    assert result.get_power() == 6


def test_units_with_prefix_multiply(meter, gram, kilo, mega):
    u = kilo * meter
    v = kilo * gram
    result = u * v

    assert result.prefix == mega
    assert meter in result.numerator
    assert gram in result.numerator 
    assert result.denominator == []


def test_multiple_components(meter, second, gram, kilo):
    u = (kilo * gram * meter / second) * (second * meter)

    assert u.prefix == kilo
    assert gram in u.get_components()
    assert second not in u.get_components()
    assert not u.denominator


def test_identity_roundtrip(meter, second):
    u = (meter / second) * second
    v = meter * (second / second)

    assert u == v == meter


def test_collapse_single(meter):
    u = Unit.from_basics("meter", "m", "length")
    u.collapse_standard_compounds()

    assert u == meter


def test_collapse_after_expand(kilo, gram, sqmeter, meter, watt):
    u = (kilo * gram  *  sqmeter)  / (watt * meter)

    assert len(u.numerator) == 2
    assert len(u.denominator) == 1
    assert u.prefix == kilo
    assert u.denominator[0] == watt


def negative_powers_collapse(meter, watt, sqmeter):
    u = watt / (meter * meter)

    assert len(u.numerator) == 1
    assert len(u.denominator) == 1
    assert u.numerator[0] == watt
    assert u.denominator[0] == sqmeter


def test_collapse_cubic_meter(meter, cubicmeter):
    u = meter * meter * meter

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == cubicmeter
    assert u.name == "cubic meter"


def test_collapse_square_feet(feet, sqfeet):
    u = feet * feet

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == sqfeet
    assert u.name == "square feet"


def test_collapse_mixed_units_no_change(meter, feet):
    u = meter * feet

    assert len(u.get_components()) == 2
    assert meter in u.get_components()
    assert feet in u.get_components()


def test_simplify_with_multiple_matches_more_in_numerator(meter, watt):
    u = meter *  watt
    v = meter *  watt *  watt
    result = u / v

    assert len(result.get_components()) == 1
    assert meter not in result.get_components()
    assert watt in result.get_components()    

def test_simplify_with_multiple_matches_more_in_denomenator(meter, watt):
    u = meter * meter * meter  * watt
    v = meter * meter 
    result = u / v

    assert len(result.get_components()) == 2
    assert meter in result.get_components()
    assert watt in result.get_components()    


def test_collapse_after_simplify(meter, sqmeter):
    u = (meter / meter) * (meter * meter)

    assert len(u.get_components()) == 1
    assert u.get_components()[0] == sqmeter


def test_cancel_after_collapse(meter, gram, sqmeter):
    density = gram / sqmeter
    area = meter * meter
    result = density * area

    assert len(result.get_components()) == 1
    assert result.get_components()[0] == gram
    assert result.denominator is None or len(result.denominator) == 0
    assert result.name == "gram"
    assert result.standard_notation == "g"
    assert result.qty_measured == "mass"
    assert not result.is_compound()
