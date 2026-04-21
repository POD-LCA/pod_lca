import pytest
from pod_lca.units import Unit
from pod_lca.units import Quantity
# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def meter():
    return Unit.from_basics("meter", "m", "length")

@pytest.fixture
def feet():
    return Unit.from_basics("feet", "ft", "length")

@pytest.fixture
def sqmeter():
    return Unit.from_basics("square meter", "m²", "area")

@pytest.fixture
def sqfeet():
    return Unit.from_basics("square feet", "ft²", "area")

@pytest.fixture
def cubicfeet():
    return Unit.from_basics("cubic feet", "ft³", "volume")

@pytest.fixture
def watt():
    return Unit.from_basics("watt", "W", "power")

def test_quantity_add(meter, feet):
    q1 = Quantity(1, meter)
    q2 = Quantity(2, feet)

    q_new = q1 + q2

    assert q_new.unit == meter
    assert q_new.value ==  pytest.approx(1.6096)

def test_quantity_multiply(meter, feet, sqmeter):
    q1 = Quantity(1, meter)
    q2 = Quantity(2, feet)

    q_new = q1 * q2

    assert q_new.unit == sqmeter
    assert q_new.value ==  pytest.approx(2 * 0.3048)

def test_quantity_multiply_compound(feet, sqmeter, cubicfeet):
    q1 = Quantity(1, sqmeter)
    q2 = Quantity(1, feet)

    q_new = q1 * q2

    assert q_new.unit == cubicfeet
    assert q_new.value ==  pytest.approx(10.7639)

def test_quantity_division(watt, meter, feet):
    q1 = Quantity(1, watt * meter)
    q2 = Quantity(1, feet)

    q_new = q1 / q2

    assert q_new.unit == watt
    assert q_new.value ==  pytest.approx(3.280839)

def test_quantity_division_compound(watt, sqmeter, feet):
    q1 = Quantity(1, watt * sqmeter)
    q2 = Quantity(1, feet)

    q_new = q1 / q2

    assert q_new.unit == watt * feet
    assert q_new.value ==  pytest.approx(10.7639)