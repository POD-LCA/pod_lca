from unittest.mock import Mock, call

import pytest

import pod_lca.lca_modules.materials_screening.electricity_product as electricity_module
from pod_lca.materials_screening import Electricity
from pod_lca.units import WATT_HOUR


def test_electricity_new_builds_item_and_registers_it(monkeypatch):
    location = object()
    model = Mock()
    model.get_location.return_value = location
    supplier = Mock()
    supplier.get_declared_unit.return_value = WATT_HOUR
    unit_impacts = object()
    unit_emissions = object()
    supplier.get_unit_impacts.return_value = unit_impacts
    supplier.get_unit_emissions.return_value = unit_emissions
    carbon_storage = object()
    from_location = Mock(return_value=supplier)
    add_inventory_records = Mock()
    monkeypatch.setattr(electricity_module.ElectricitySupply, "from_location", from_location)
    monkeypatch.setattr(electricity_module.CarbonStorage, "from_parent", Mock(return_value=carbon_storage))
    monkeypatch.setattr(Electricity, "add_inventory_records_to_model", add_inventory_records)

    item = Electricity.new(
        7,
        "Grid electricity",
        model,
        "A3",
        12,
        WATT_HOUR,
        year=2035,
        geographical_scope="Regional",
    )

    assert item.get_id() == 7
    assert item.get_name() == "Grid electricity"
    assert item.get_model() is model
    assert item.get_life_cycle_stage() == "A3"
    assert item.get_qty() == 12
    assert item.get_unit() == WATT_HOUR
    assert item.get_supplier() is supplier
    assert item.unit_impacts is unit_impacts
    assert item.unit_emissions is unit_emissions
    assert item.unit_carbon_storage is carbon_storage
    assert item.inventories_declared_unit == WATT_HOUR
    assert item.inventories_declared_qty == 1.0
    from_location.assert_called_once_with(location, 2035)
    supplier.set_geographical_scope.assert_called_once_with("Regional")
    add_inventory_records.assert_called_once_with()


def test_electricity_from_unit_inventories_initializes_declared_inventories():
    impacts = object()
    emissions = object()
    carbon_storage = object()

    item = Electricity.from_unit_inventories(
        "Factory electricity", 4, WATT_HOUR, impacts, emissions, carbon_storage
    )

    assert item.get_name() == "Factory electricity"
    assert item.get_qty() == 4
    assert item.get_unit() == WATT_HOUR
    assert item.get_supplier() is None
    assert item.unit_impacts is impacts
    assert item.unit_emissions is emissions
    assert item.unit_carbon_storage is carbon_storage
    assert item.inventories_declared_unit == WATT_HOUR
    assert item.inventories_declared_qty == 1.0
    assert item.get_impact_database_entry() is None


def test_electricity_setters_forward_changes_to_supplier(monkeypatch):
    supplier = Mock()
    item = Electricity().set_supplier(supplier)
    location = object()
    from_state = Mock(return_value=location)
    monkeypatch.setattr(electricity_module.Location, "from_US_state", from_state)

    assert item.set_year(2040) is item
    assert item.set_geographical_scope("Local") is item
    assert item.set_scenario("LowRECost") is item
    assert item.set_location(state="WA") is item

    assert item.get_year() == 2040
    assert item.get_geographical_scope() == "Local"
    assert item.get_scenario() == "LowRECost"
    assert item.get_location() is location
    supplier.set_year.assert_called_once_with(2040)
    supplier.set_geographical_scope.assert_called_once_with("Local")
    supplier.set_scenario.assert_called_once_with("LowRECost")
    supplier.set_location.assert_called_once_with(location)
    from_state.assert_called_once_with("WA")


def test_electricity_rejects_unknown_scenario_when_supplier_is_present():
    item = Electricity().set_supplier(Mock())

    with pytest.raises(ValueError, match="not a valid scenario"):
        item.set_scenario("FutureCase")


def test_electricity_getters_use_supplier_values_when_not_set():
    location = Mock()
    supplier = Mock()
    supplier.get_year.return_value = 2030
    supplier.get_geographical_scope.return_value = "National"
    supplier.get_location.return_value = location
    supplier.get_scenario.return_value = "MidCase"
    item = Electricity().set_supplier(supplier)
    item.year = None
    item.geographical_scope = None
    item.location = None
    item.scenario = None

    assert item.get_year() == 2030
    assert item.get_geographical_scope() == "National"
    assert item.get_location() is location
    assert item.get_scenario() == "MidCase"
    assert supplier.get_year.call_count >= 1
    supplier.get_geographical_scope.assert_called_once_with()
    supplier.get_location.assert_called_once_with()
    supplier.get_scenario.assert_called_once_with()


def test_electricity_get_data_distribution_expands_weighted_impacts(monkeypatch):
    impacts = [
        Mock(**{"get_record.side_effect": lambda category: {"GWP": 1.5}.get(category, 0)}),
        Mock(**{"get_record.side_effect": lambda category: {"GWP": 2.5}.get(category, 0)}),
    ]
    supplier = Mock()
    supplier.get_impact_distribution.return_value = impacts, [2, 1]
    supplier.get_declared_unit.return_value = WATT_HOUR
    item = Electricity().set_supplier(supplier).set_unit(WATT_HOUR).set_qty(2)
    from_data = Mock(side_effect=lambda data, **kwargs: (data, kwargs))
    monkeypatch.setattr(electricity_module.DataDistribution, "from_data", from_data)

    distributions = item.get_data_distribution("impacts")

    assert len(distributions) == len(
        electricity_module.config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
    )
    assert distributions[0] == (
        [3.0, 3.0, 5.0],
        {"is_cts": True, "name": "GWP", "set_dist": False},
    )
    from_data.assert_any_call(
        [3.0, 3.0, 5.0], is_cts=True, name="GWP", set_dist=False
    )
    supplier.get_impact_distribution.assert_called_once_with()


def test_electricity_get_data_distribution_returns_saved_nonimpact_distribution():
    distribution = object()
    item = Electricity()
    item.data_distributions["quantity"] = distribution

    assert item.get_data_distribution("quantity") is distribution


def test_electricity_impacts_are_cached_until_cache_key_changes(monkeypatch):
    item = Electricity().set_unit(WATT_HOUR).set_qty(2)
    first_impacts = object()
    updated_impacts = object()
    get_impacts = Mock(side_effect=[first_impacts, updated_impacts])
    monkeypatch.setattr(electricity_module.Master, "get_impacts", get_impacts)

    assert item.get_impacts() is first_impacts
    assert item.get_impacts() is first_impacts
    assert item._cache_is_computed is True
    item.set_qty(3)
    assert item.get_impacts() is updated_impacts
    get_impacts.assert_has_calls([call(), call()])
    assert get_impacts.call_count == 2


def test_electricity_update_inventory_records_updates_supplier_and_master(monkeypatch):
    supplier = Mock()
    item = Electricity().set_supplier(supplier)
    update_master = Mock()
    monkeypatch.setattr(electricity_module.Master, "update_inventory_records", update_master)

    assert item.update_inventory_records() is item

    supplier.update_inventory_records.assert_called_once_with()
    update_master.assert_called_once_with()


def test_electricity_update_inventory_records_without_supplier(monkeypatch):
    item = Electricity()
    update_master = Mock()
    monkeypatch.setattr(electricity_module.Master, "update_inventory_records", update_master)

    assert item.update_inventory_records() is item

    update_master.assert_called_once_with()


def test_electricity_cache_key_tracks_consumption_and_location_parameters():
    location = Mock()
    location.get_state.return_value = "WA"
    location.get_zip.return_value = "98101"
    item = Electricity().set_unit(WATT_HOUR).set_qty(5)
    item.set_scenario("MidCase")
    item.set_year(2035)
    item.set_geographical_scope("Local")
    item.location = location

    assert item.get_cache_key() == (5, WATT_HOUR.standard_notation, "MidCase", 2035, "Local", "WA", "98101")
