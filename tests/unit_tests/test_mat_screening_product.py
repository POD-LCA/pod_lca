import pytest
from unittest.mock import Mock

import pod_lca.lca_modules.materials_screening.product as product_module
from pod_lca.materials_screening import Master, Product, Fuel
from pod_lca.units import GRAM, KILOGRAM, Unit, CUBIC_METER, KG_CARBON_DIOXIDE, METER


class DummyModel:
    def __init__(self):
        self.project = object()
        self.impacts = {"A1": [], "A3": []}
        self.emissions = {"A1": [], "A3": []}
        self.carbon_storage = {"A1": [], "A3": []}

    def get_project(self):
        return self.project

    def get_impacts(self):
        return self.impacts

    def get_emissions(self):
        return self.emissions

    def get_carbon_storage(self):
        return self.carbon_storage

    def get_transportation_manager(self):
        return None

class DummyImpacts:
    def __init__(self, values):
        self.values = dict(values)

    def get_record(self, category):
        return self.values[category]

    def get_categories(self):
        return list(self.values)

    def update_qty(self, values):
        self.values.update(values)

    def copy(self):
        return DummyImpacts(self.values)

    
@pytest.fixture
def dummy_model():
    return DummyModel()


def test_master_initializes_with_expected_defaults():
    item = Master()

    assert item.get_id() is None
    assert item.get_model() is None
    assert item.get_name() is None
    assert item.get_life_cycle_stage() is None
    assert item.get_impact_database_entry() is None
    assert item.get_qty() == 0.0
    assert item.get_unit() is None
    assert item.is_hotspot is False
    assert item.get_data_distributions() == {}
    assert item.get_pedigree_score() is not None


def test_master_new_sets_core_fields_and_registers_record_in_model(dummy_model):
    item = Master.new(7, "Concrete", dummy_model, "A1", 2.5, KILOGRAM, None)

    assert item.get_id() == 7
    assert item.get_name() == "Concrete"
    assert item.get_model() is dummy_model
    assert item.get_life_cycle_stage() == "A1"
    assert item.get_qty() == 2.5
    assert item.get_unit() == KILOGRAM
    assert item.get_impact_database_entry() is None
    assert item.get_impacts() is item.impacts
    assert item.get_emissions() is item.emissions
    assert item.get_carbon_storage() is item.carbon_storage
    assert item.impacts in dummy_model.impacts["A1"]
    assert item.emissions in dummy_model.emissions["A1"]
    assert item.carbon_storage in dummy_model.carbon_storage["A1"]


def test_master_set_id(dummy_model):
    item = Master.new(1, "Plastic", dummy_model, "A1", 1.0, KILOGRAM, None)

    assert item.get_id() == 1

    item.set_id(10)
    assert item.get_id() == 10


def test_master_set_model(dummy_model):
    item = Master.new(2, "Aluminum", dummy_model, "A1", 1.0, KILOGRAM, None)

    assert item.get_model() is dummy_model
    assert item.get_parent() is dummy_model

    new_model = DummyModel()
    item.set_model(new_model)
    assert item.get_model() is new_model
    assert item.get_parent() is new_model


def test_master_set_name_and_life_cycle_stage_updates_properties(dummy_model):
    item = Master.new(5, "Steel", dummy_model, "A1", 1.0, KILOGRAM, None)

    item.set_name("Reinforced Steel")
    item.set_life_cycle_stage("A3")

    assert item.get_name() == "Reinforced Steel"
    assert item.get_life_cycle_stage() == "A3"
    assert item.impacts in dummy_model.impacts["A3"]
    assert item.emissions in dummy_model.emissions["A3"]
    assert item.carbon_storage in dummy_model.carbon_storage["A3"]


def test_master_set_qty_and_unit_conversion_are_supported():
    item = Master()
    item.set_unit(KILOGRAM)
    item.set_qty("2.5")

    assert item.get_qty() == 2.5
    assert item.get_qty(GRAM) == 2500.0

    with pytest.raises(ValueError):
        item.set_unit(Unit.from_basics("meter", "m", "length"))


def test_master_set_impact_database_entry_none_zeroes_records(dummy_model):
    item = Master.new(3, "Glass", dummy_model, "A3", 1.0, KILOGRAM, None)

    assert item.inventories_declared_qty == 1.0
    assert item.inventories_declared_unit == KILOGRAM
    assert all(quantity == 0.0 for quantity in item.get_impacts().get_record_dict().values())
    assert all(quantity == 0.0 for quantity in item.get_emissions().get_record_dict().values())
    assert all(quantity == 0.0 for quantity in item.get_carbon_storage().get_record_dict().values())


def test_master_set_impact_database_entry(monkeypatch):
    model = DummyModel()
    item = Master.new(2, "Aluminum", model, "A1", 1.0, KILOGRAM, None)
    database = Mock()
    database.get_qty_key.return_value = "qty"
    database.get_unit_key.return_value = "unit"
    inventory = {
        **{category: 1.0 for category in item.unit_impacts.get_categories()},
        **{category: 2.0 for category in item.unit_emissions.get_categories()},
        **{category: 3.0 for category in item.unit_carbon_storage.get_categories()},
        "qty": 2.0,
        "unit": KILOGRAM,
    }
    monkeypatch.setattr(item, "get_impact_database", lambda: database)
    monkeypatch.setattr(item, "get_data_from_database", lambda _: inventory)
    monkeypatch.setattr(item, "update_mineral_carbon_storage", Mock())
    monkeypatch.setattr(item, "update_bio_carbon_storage", Mock())

    item.set_impact_database_entry("Aluminum_Impact_Entry")

    assert item.get_impact_database_entry() == "Aluminum_Impact_Entry"
    assert item.inventories_declared_qty == 2.0
    assert item.inventories_declared_unit == KILOGRAM
    assert all(
        item.unit_impacts.get_record(category) == 1.0
        for category in item.unit_impacts.get_categories()
    )
    assert all(
        item.unit_emissions.get_record(category) == 2.0
        for category in item.unit_emissions.get_categories()
    )
    assert all(
        item.unit_carbon_storage.get_record(category) == 3.0
        for category in item.unit_carbon_storage.get_categories()
    )


def test_master_set_life_cycle_stage_moves_inventory_records_between_stages(dummy_model):
    item = Master.new(1, "Wood", dummy_model, "A1", 10.0, KILOGRAM, None)

    assert item.impacts in dummy_model.impacts["A1"]
    assert item.emissions in dummy_model.emissions["A1"]
    assert item.carbon_storage in dummy_model.carbon_storage["A1"]

    item.set_life_cycle_stage("A3")

    assert item.impacts in dummy_model.impacts["A3"]
    assert item.impacts not in dummy_model.impacts["A1"]
    assert item.emissions in dummy_model.emissions["A3"]
    assert item.carbon_storage in dummy_model.carbon_storage["A3"]


def test_product_new_initializes_master_inventories_and_product_properties(dummy_model):
    product = Product.new(4, "Timber", dummy_model, "A1", 2.5, KILOGRAM, None)

    assert isinstance(product, Master)
    assert product.get_id() == 4
    assert product.get_name() == "Timber"
    assert product.get_model() is dummy_model
    assert product.get_life_cycle_stage() == "A1"
    assert product.get_qty() == 2.5
    assert product.get_unit() == KILOGRAM
    assert product.is_material is True
    assert product.electricity == {
        "default": None,
        "custom": None,
        "_current": None,
        "_tag": None,
    }
    assert product.impacts in dummy_model.impacts["A1"]
    assert product.emissions in dummy_model.emissions["A1"]
    assert product.carbon_storage in dummy_model.carbon_storage["A1"]


def test_product_updates_master_quantity_and_mass_properties(dummy_model):
    product = Product.new(0, "Aggregate", dummy_model, "A1", 2, KILOGRAM, None)
    product.set_qty("3.5")
    product.set_density(1800)
    product.set_moisture_content(0.2)

    assert product.get_qty() == 3.5
    assert product.get_weight().value == 3.5
    assert product.get_density() == 1800
    assert product.get_dry_density() == pytest.approx(1.0 / 1.2)
    assert product.get_dry_mass().value == pytest.approx(3.5 / 1.2)

@pytest.mark.parametrize(
    ("product_type", "prefix"),
    [(Product, "Product"), (Fuel, "Fuel")],
)
def test_product_initialization_and_string_representation(product_type, prefix):
    product = product_type()
    product.set_name("Concrete").set_life_cycle_stage("A1").set_unit(KILOGRAM)
    product.set_qty(2)

    assert product.is_material is True
    if product_type is Fuel:
        assert product.is_energy is True
    else:
        assert not hasattr(product, "is_energy")
    assert str(product) == f"{prefix}(name=Concrete, LC stage=A1, qty=2 kg)"


def test_product_production_year_updates_emission_transport_and_electricity_profiles(
    monkeypatch,
):
    product = Product()
    product.emissions = object()
    emission = Mock()
    transport_emission = Mock()
    leg = Mock()
    leg.get_emissions.return_value = transport_emission
    custom_electricity = Mock()
    product.get_emissions = Mock(return_value=emission)
    product.get_transportation = Mock(return_value=[leg])
    product.electricity["custom"] = custom_electricity
    profile = object()
    pulse = Mock(return_value=profile)
    monkeypatch.setattr(product_module.UniformEmissionProfile, "unit_pulse", pulse)

    assert product.set_production_year("2035") is product

    assert product.get_production_year() == 2035
    assert profile == transport_emission.set_temporal_emission_profile.call_args.args[0]
    emission.set_temporal_emission_profile.assert_called_once_with(profile)
    pulse.assert_called_once_with(at=2035)
    custom_electricity.set_year.assert_called_once_with(2035)


@pytest.mark.parametrize(
    ("unit", "density_unit", "density", "qty", "expected"),
    [
        (KILOGRAM, None, None, 4, (4, KILOGRAM)),
        (CUBIC_METER, KILOGRAM / CUBIC_METER, 1000, 2, (2000, KILOGRAM)),
        (CUBIC_METER, CUBIC_METER / KILOGRAM, 2, 6, (3, KILOGRAM)),
    ],
)
def test_product_get_weight_converts_mass_or_density(
    unit, density_unit, density, qty, expected
):
    product = Product().set_unit(unit).set_qty(qty)
    product.unit_carbon_storage = Mock()
    if density_unit is not None:
        product.set_density(density, density_unit)

    weight = product.get_weight()

    assert weight.value == pytest.approx(expected[0])
    assert weight.unit == expected[1]


def test_product_get_weight_without_density_or_mass_result():
    product = Product().set_unit(CUBIC_METER).set_qty(2)
    product.unit_carbon_storage = Mock()

    assert product.get_weight() is None

    product.set_density(2, METER)
    assert product.get_weight() is None


def test_product_density_loads_database_value_and_recalculates_carbon_content():
    product = Product()
    product.unit_carbon_storage = Mock()
    product.get_impact_database_entry = Mock(return_value="wood")
    product.get_impact_database = Mock()
    database = product.get_impact_database.return_value
    database.get_data_entry.return_value = {
        "density": "650",
        "density_unit": KILOGRAM / CUBIC_METER,
    }
    database.get_density_unit_key.return_value = "density_unit"
    database.get_density_key.return_value = "density"

    assert product.set_density() is product

    assert product.get_density() == 650
    assert product.get_density_unit() == KILOGRAM / CUBIC_METER
    product.unit_carbon_storage.update_biogenic_carbon_content.assert_called()


@pytest.mark.parametrize(
    ("method", "value", "error", "message"),
    [
        ("set_density", "heavy", TypeError, "Density"),
        ("set_density", object(), ValueError, "Density input"),
        ("set_thickness", "thick", TypeError, "Thickness"),
        ("set_thickness", object(), ValueError, "Thickness input"),
    ],
)
def test_product_rejects_invalid_density_and_thickness(method, value, error, message):
    product = Product()
    product.unit_carbon_storage = Mock()

    with pytest.raises(error, match=message):
        getattr(product, method)(value)


def test_product_density_and_thickness_normalize_nan_to_none():
    product = Product()
    product.unit_carbon_storage = Mock()

    product.set_density(float("nan"))
    product.set_thickness(float("nan"))

    assert product.get_density() is None
    assert product.get_thickness() is None


def test_product_get_impacts_caches_unstaged_results(monkeypatch):
    product = Product()
    product.get_cache_key = Mock(return_value=("same",))
    result = DummyImpacts({"GWP": 10})
    super_get_impacts = Mock(return_value=result)
    monkeypatch.setattr(product_module.Master, "get_impacts", super_get_impacts)

    first_result = product.get_impacts()
    second_result = product.get_impacts()

    assert first_result is result
    assert second_result is not result
    assert second_result.values == result.values
    super_get_impacts.assert_called_once_with()
    assert product._cache_is_computed[None] is True
    assert product._last_params[None] == ("same",)


@pytest.mark.parametrize(
    ("stage", "requested_stage", "storage_qty", "expected_records"),
    [
        ("A1", "A1", 3, {"GWP": 7, "GWP_biogenic": -3, "Other": 4}),
        ("A1", "A3", 3, {"GWP": 3, "GWP_biogenic": 3, "Other": 0}),
        ("A3", "A3", 3, {"GWP": 10, "GWP_biogenic": 0, "Other": 4}),
    ],
)
def test_product_get_impacts_adjusts_carbon_storage_by_life_cycle_stage(
    monkeypatch, stage, requested_stage, storage_qty, expected_records
):
    product = Product().set_life_cycle_stage(stage).set_model(object())
    product.get_cache_key = Mock(return_value=("stage-key",))
    storage = Mock()
    storage.get_biogenic_carbon_storage_qty.return_value = storage_qty
    product.get_carbon_storage = Mock(return_value=storage)
    result = DummyImpacts({"GWP": 10, "GWP_biogenic": 0, "Other": 4})
    super_get_impacts = Mock(return_value=result)
    monkeypatch.setattr(product_module.Master, "get_impacts", super_get_impacts)

    impacts = product.get_impacts(requested_stage)

    assert impacts.values == expected_records
    assert product._cache_impacts[requested_stage] is not impacts
    assert product._cache_is_computed[requested_stage] is True
    storage.get_biogenic_carbon_storage_qty.assert_called_once_with(KG_CARBON_DIOXIDE)
    super_get_impacts.assert_called_once_with()


def test_product_get_impacts_caches_unavailable_stage_result(monkeypatch):
    product = Product().set_life_cycle_stage("A3")
    product.get_cache_key = Mock(return_value=("stage-key",))
    product.get_carbon_storage = Mock()
    super_get_impacts = Mock(return_value=DummyImpacts({"GWP": 10, "GWP_biogenic": 0}))
    monkeypatch.setattr(product_module.Master, "get_impacts", super_get_impacts)

    assert product.get_impacts("A1") is None
    assert product.get_impacts("A1") is None
    assert product._cache_is_computed["A1"] is True
    super_get_impacts.assert_called_once_with()


def test_product_get_carbon_storage_updates_inventory_when_cache_is_stale():
    product = Product()
    product.get_cache_key = Mock(return_value=("new-key",))
    product._last_params["A1"] = ("old-key",)
    product.carbon_storage = object()
    product.update_inventory_records = Mock()

    assert product.get_carbon_storage() is product.carbon_storage

    product.update_inventory_records.assert_called_once_with()


def test_product_get_carbon_storage_skips_update_for_current_cache():
    product = Product()
    product.get_cache_key = Mock(return_value=("current-key",))
    product._last_params["A1"] = ("current-key",)
    product._cache_is_computed["A1"] = True
    product.carbon_storage = object()
    product.update_inventory_records = Mock()

    assert product.get_carbon_storage() is product.carbon_storage

    product.update_inventory_records.assert_not_called()


def test_product_update_inventory_records_updates_base_and_electricity(monkeypatch):
    product = Product()
    base_update = Mock()
    electricity_update = Mock()
    monkeypatch.setattr(product_module.Master, "update_inventory_records", base_update)
    product.update_electricity_records = electricity_update

    assert product.update_inventory_records() is product

    base_update.assert_called_once_with()
    electricity_update.assert_called_once_with()


def test_product_cache_key_contains_inventory_and_electricity_inputs():
    product = Product().set_unit(KILOGRAM).set_qty(2).set_life_cycle_stage("A1")
    product.set_impact_database_entry = Mock(return_value=None)
    product.unit_carbon_storage = Mock()
    product.unit_carbon_storage.get_mineral_carbonation_potential.return_value = False
    product.unit_carbon_storage.get_biogenic_carbon_storage_potential.return_value = True
    product.unit_carbon_storage.get_biogenic_carbon_composition.return_value = 0.5
    product.unit_carbon_storage.get_mineral_carbon_storage_qty.return_value = 0

    cache_key = product.get_cache_key()

    assert cache_key[:4] == (2, KILOGRAM.standard_notation, None, "A1")
    assert cache_key[4:11] == (None, None, None, None, None, None, 0.0)
    assert cache_key[11] is None
    assert cache_key[12:] == (False, True, 0.5, 0)


def test_product_cache_key_includes_selected_electricity_and_declared_density():
    product = Product().set_unit(KILOGRAM).set_qty(2).set_life_cycle_stage("A1")
    product.electricity["_current"] = "custom"
    custom_electricity = Mock()
    custom_electricity.get_scenario.return_value = "MidCase"
    custom_electricity.get_year.return_value = 2035
    custom_electricity.get_geographical_scope.return_value = "regional"
    custom_electricity.get_location.return_value.get_state.return_value = "WA"
    custom_electricity.get_location.return_value.get_zip.return_value = "98101"
    product.electricity["custom"] = custom_electricity
    product.get_impact_database_entry = Mock(return_value="wood")
    product.inventories_declared_unit = KILOGRAM
    product.get_dry_density = Mock(return_value=800)
    product.unit_carbon_storage = Mock()

    cache_key = product.get_cache_key()

    assert cache_key[2:12] == (
        "wood",
        "A1",
        "custom",
        "MidCase",
        2035,
        "regional",
        "WA",
        "98101",
        0.0,
        800,
    )
    product.get_dry_density.assert_called_once_with()