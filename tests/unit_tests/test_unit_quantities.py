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


def test_quantity_add(meter, feet):
    q1 = Quantity(1, meter)
    q2 = Quantity(2, feet)

    q_new = q1 + q2

    assert q_new.unit == meter
    assert q_new.value ==  pytest.approx(1.6096)