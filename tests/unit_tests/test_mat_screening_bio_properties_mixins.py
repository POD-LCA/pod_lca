import pytest

from pod_lca.carbon_storage import CarbonStorage
from pod_lca.materials_screening import Product
from pod_lca.units import KILOGRAM, METER


def test_bio_properties_mixin_sets_moisture_and_derived_dry_mass():
    product = Product()
    product.set_unit(KILOGRAM)
    product.set_qty(12)
    product.inventories_declared_unit = KILOGRAM
    product.inventories_declared_qty = 12
    product.unit_carbon_storage = CarbonStorage.from_parent(product)

    assert product.get_moisture_content() == 0.0
    assert product.set_moisture_content(0.2) is product

    assert product.get_dry_density() == pytest.approx(10.0)
    assert product.get_dry_mass().value == pytest.approx(10.0)
    assert product.get_dry_mass().unit == KILOGRAM


def test_bio_properties_mixin_non_numeric_moisture_does_not_replace_value():
    product = Product()
    product.unit_carbon_storage = CarbonStorage.from_parent(product)
    product.set_moisture_content(0.15)

    product.set_moisture_content("wet")

    assert product.get_moisture_content() == 0.15


def test_product_quantity_density_and_moisture_properties():
    class MinimalModel:
        def __init__(self):
            self.impacts = {"A1": [], "A3": []}
            self.emissions = {"A1": [], "A3": []}
            self.carbon_storage = {"A1": [], "A3": []}

        def get_impacts(self):
            return self.impacts

        def get_emissions(self):
            return self.emissions

        def get_carbon_storage(self):
            return self.carbon_storage

    product = Product.new(0, "Aggregate", MinimalModel(), "A1", 2, KILOGRAM, None)
    product.set_qty("3.5")
    product.set_density(1800)
    product.set_moisture_content(0.2)

    assert product.get_qty() == 3.5
    assert product.get_weight().value == 3.5
    assert product.get_density() == 1800
    assert product.get_dry_density() == pytest.approx(1.0 / 1.2)
    assert product.get_dry_mass().value == pytest.approx(3.5 / 1.2)


def test_product_material_properties_validate_numeric_values():
    product = Product()
    product.unit_carbon_storage = CarbonStorage.from_parent(product)
    product.set_density("500")
    product.set_thickness("0.2", METER)

    assert product.get_density() == 500.0
    assert product.get_thickness() == 0.2
    assert product.get_thickness_unit() == METER
    with pytest.raises(TypeError, match="Density"):
        product.set_density("heavy")
    with pytest.raises(TypeError, match="Thickness"):
        product.set_thickness("thick")
    with pytest.raises(ValueError, match="Thickness input"):
        product.set_thickness(object())
