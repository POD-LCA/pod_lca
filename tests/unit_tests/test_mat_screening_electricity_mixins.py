from unittest.mock import Mock

import pandas as pd
import pytest

import pod_lca.lca_modules.materials_screening.product_electricity_mixins as mixin_module
from pod_lca.materials_screening import Product
from pod_lca.units import UNITS_MAP


class DummyProject:
    def __init__(self, database, location=None):
        self.database = database
        self.location = location

    def get_impact_database(self):
        return self.database

    def get_location(self):
        return self.location


class DummyModel:
    def __init__(self, database, location=None):
        self.project = DummyProject(database, location)

    def get_project(self):
        return self.project

    def get_location(self):
        return self.project.get_location()


@pytest.mark.parametrize(
    ("tag", "qty_key"),
    [
        ("Electricity_", "Electricity_Qty"),
        ("electricity_", "electricity_Qty"),
        ("elec_", "elec_Qty"),
        ("Elec_", "Elec_Qty"),
    ],
)
def test_electricity_mixin_finds_each_supported_database_tag(tag, qty_key):
    database = Mock()
    database.get_data_entry.return_value = {qty_key: 1.0}
    database.get_qty_key.return_value = "Qty"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.set_model(DummyModel(database))

    assert product.set_electricity_database_tag() is product
    assert product.get_electricity_database_tag() == tag


def test_electricity_mixin_database_tag_is_unchanged_when_no_prefix_matches():
    database = Mock()
    database.get_data_entry.return_value = {"Qty": 1.0}
    database.get_qty_key.return_value = "Qty"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.set_model(DummyModel(database))

    assert product.set_electricity_database_tag() is product
    assert product.electricity["_tag"] is None
    assert product.get_electricity_database_tag() is None


def test_electricity_mixin_parameter_getters_return_custom_values_and_location():
    location = Mock()
    location.get_state.return_value = "WA"
    location.get_zip.return_value = "98101"
    custom = Mock()
    custom.get_scenario.return_value = "MidCase"
    custom.get_year.return_value = 2035
    custom.get_geographical_scope.return_value = "Local"
    custom.get_location.return_value = location
    product = Product()
    product.electricity.update({"custom": custom, "_current": "custom"})
    product.electricity_combo = "High"

    assert product.get_electricity() is custom
    assert product.get_electricity_source() == "custom"
    assert product.get_electricity_combo() == "High"
    assert product.get_electricity_scenario() == "MidCase"
    assert product.get_electricity_year() == 2035
    assert product.get_electricity_geographical_scope() == "Local"
    assert product.get_electricity_location_regional() == "WA"
    assert product.get_electricity_location_local() == "98101"


def test_electricity_mixin_custom_parameter_getters_return_none_for_default_source():
    product = Product()
    product.electricity["_current"] = "default"

    assert product.get_electricity_scenario() is None
    assert product.get_electricity_year() is None
    assert product.get_electricity_geographical_scope() is None
    assert product.get_electricity_location_regional() is None
    assert product.get_electricity_location_local() is None


@pytest.mark.parametrize(
    ("setter_name", "setter_args", "scope", "location_args"),
    [
        ("set_electricity_location_regional", ("OR",), "Regional", {"state": "OR"}),
        ("set_electricity_location_local", ("97201",), "Local", {"zip_code": "97201"}),
    ],
)
def test_electricity_mixin_location_setters_select_custom_electricity(
    setter_name, setter_args, scope, location_args
):
    product = Product()
    default = object()
    custom = Mock()
    product.electricity.update(
        {"default": default, "custom": custom, "_current": "default"}
    )
    product.get_impacts = Mock()

    assert getattr(product, setter_name)(*setter_args) is product

    assert product.get_electricity_source() == "custom"
    custom.set_geographical_scope.assert_called_once_with(scope)
    custom.set_location.assert_called_once_with(**location_args)


@pytest.mark.parametrize(
    "setter_name", ["set_electricity_location_regional", "set_electricity_location_local"]
)
def test_electricity_mixin_clearing_location_restores_project_location(
    setter_name,
):
    project_location = object()
    custom = Mock()
    product = Product()
    product.set_model(DummyModel(database=None, location=project_location))
    product.electricity.update(
        {"default": object(), "custom": custom, "_current": "custom"}
    )
    product.get_impacts = Mock()

    assert getattr(product, setter_name)(None) is product

    assert product.get_electricity_source() == "default"
    custom.set_geographical_scope.assert_called_once_with(
        mixin_module.config["setup"]["electricity"]["DEFAULT_REIGIONAL_RESOLUTION"]
    )
    custom.set_location.assert_called_once_with(location_obj=project_location)


def test_electricity_mixin_calculates_database_quantity_in_declared_units():
    database = Mock()
    database.get_data_entry.return_value = {
        "elec_Qty": 80.0,
        "Qty": 4.0,
        "Unit": UNITS_MAP["kg"],
    }
    database.get_qty_key.return_value = "Qty"
    database.get_unit_key.return_value = "Unit"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.electricity["_tag"] = "elec_"
    product.set_model(DummyModel(database))
    product.get_qty = Mock(return_value=2.0)

    assert product.get_electricity_qty() == 40.0
    product.get_qty.assert_called_once_with(UNITS_MAP["kg"])


def test_set_electricity_product_builds_custom_and_database_inventory_products(monkeypatch):
    class ElectricityDatabase:
        DATA_IMPORTS = {
            "impacts": ("impact_a",),
            "emissions": ("emission_a",),
            "carbon_storage": ("storage_a",),
        }

        def get_data_entry(self, entry):
            return pd.Series(
                {
                    "elec_Qty": 10.0,
                    "Qty": 2.0,
                    "Unit": "kWh",
                    "elec_Unit": "MWh",
                    "elec_impact_a": 20.0,
                    "elec_emission_a": 6.0,
                    "elec_storage_a": 4.0,
                }
            )

        def get_qty_key(self):
            return "Qty"

        def get_unit_key(self):
            return "Unit"

    database = ElectricityDatabase()
    product = Product()
    product.impact_database_entry = "Concrete"
    product.set_name("Cement")
    product.production_year = 2035
    product.set_model(DummyModel(database))
    product.get_electricity_qty = Mock(return_value=3.0)
    product.set_electricity_source = Mock(return_value=product)

    custom_electricity = object()
    default_electricity = object()
    electricity = Mock()
    electricity.new.return_value = custom_electricity
    electricity.from_unit_inventories.return_value = default_electricity
    monkeypatch.setattr(mixin_module, "Electricity", electricity)
    monkeypatch.setattr(mixin_module.Impacts, "from_dict", Mock(return_value="impacts"))
    monkeypatch.setattr(mixin_module.Emissions, "from_dict", Mock(return_value="emissions"))
    monkeypatch.setattr(
        mixin_module.CarbonStorage, "from_dict", Mock(return_value="carbon_storage")
    )

    assert product.set_electricity_product() is product

    assert product.electricity["custom"] is custom_electricity
    assert product.electricity["default"] is default_electricity
    electricity.new.assert_called_once_with(
        id=None,
        name="Cement_electricity",
        model=product.get_model(),
        stage=None,
        qty=3.0,
        unit=UNITS_MAP["MWh"],
        year=2035,
    )
    assert electricity.from_unit_inventories.call_args.kwargs == {
        "name": "Cement_electricity",
        "qty": 3.0,
        "unit": UNITS_MAP["MWh"],
        "impacts": "impacts",
        "emissions": "emissions",
        "carbon_storage": "carbon_storage",
    }
    product.set_electricity_source.assert_called_once_with()


def test_set_electricity_product_without_tag_leaves_sources_unchanged():
    database = Mock()
    database.get_data_entry.return_value = {"Qty": 1.0}
    database.get_qty_key.return_value = "Qty"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.set_model(DummyModel(database))
    product.set_electricity_source = Mock(return_value=product)

    assert product.set_electricity_product() is product
    assert product.electricity["custom"] is None
    assert product.electricity["default"] is None
    product.set_electricity_source.assert_called_once_with()


def test_update_electricity_records_creates_products_and_selects_default_source():
    database = Mock()
    database.get_data_entry.return_value = {"Qty": 1.0}
    database.get_qty_key.return_value = "Qty"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.electricity["_current"] = None
    product.set_model(DummyModel(database))
    product.set_electricity_product = Mock()

    assert product.update_electricity_records() is product
    product.set_electricity_product.assert_called_once_with()
    assert product.get_electricity_source() == "default"


def test_update_electricity_records_updates_qty_for_both_sources():
    database = Mock()
    database.get_data_entry.return_value = {"elec_Qty": 3.0}
    database.get_qty_key.return_value = "Qty"
    database.get_unit_key.return_value = "Unit"
    default = Mock()
    custom = Mock()
    product = Product()
    product.impact_database_entry = "Concrete"
    product.electricity.update(
        {"default": default, "custom": custom, "_current": "default", "_tag": "elec_"}
    )
    product.set_model(DummyModel(database))
    product.get_electricity_qty = Mock(return_value=7.5)

    assert product.update_electricity_records() is product

    default.set_qty.assert_called_once_with(7.5)
    custom.set_qty.assert_called_once_with(7.5)


def test_update_electricity_records_replaces_custom_inventory_contributions():
    class ElectricityDatabase:
        DATA_IMPORTS = {"impacts": (), "emissions": (), "carbon_storage": ()}

        def get_data_entry(self, entry):
            return {"elec_Qty": 1.0}

        @staticmethod
        def get_qty_key():
            return "Qty"

    class InventoryRecord:
        def __init__(self):
            self.operations = []

        def __isub__(self, other):
            self.operations.append(("subtract", other))
            return self

        def __iadd__(self, other):
            self.operations.append(("add", other))
            return self

    database = ElectricityDatabase()
    product_records = [InventoryRecord() for _ in range(3)]
    default = Mock()
    custom = Mock()
    default_records = [object() for _ in range(3)]
    custom_records = [object() for _ in range(3)]
    for getter, default_record, custom_record in zip(
        ("get_impacts", "get_emissions", "get_carbon_storage"),
        default_records,
        custom_records,
    ):
        getattr(default, getter).return_value = default_record
        getattr(custom, getter).return_value = custom_record
    product = Product()
    product.impact_database_entry = "Concrete"
    product.electricity.update(
        {"default": default, "custom": custom, "_current": "custom", "_tag": "elec_"}
    )
    product.set_model(DummyModel(database))
    product.get_electricity_qty = Mock(return_value=1.0)
    product.impacts, product.emissions, product.carbon_storage = product_records

    assert product.update_electricity_records() is product

    for record, default_record, custom_record in zip(
        product_records, default_records, custom_records
    ):
        assert record.operations == [
            ("subtract", default_record),
            ("add", custom_record),
        ]

def test_electricity_mixin_switches_sources_and_updates_custom_parameters():
    product = Product()
    default_source = object()
    custom_source = Mock()
    product.electricity["default"] = default_source
    product.electricity["custom"] = custom_source
    product.get_impacts = Mock()

    assert product.set_electricity_source("custom") is product
    assert product.get_electricity_source() == "custom"
    assert product.get_electricity() is custom_source

    product.set_electricity_scenario("MidCase")
    product.set_electricity_year(2035)
    product.set_electricity_geographical_scope("Local")

    custom_source.set_scenario.assert_called_with("MidCase")
    custom_source.set_year.assert_called_with(2035)
    custom_source.set_geographical_scope.assert_called_with("Local")

    product.set_electricity_scenario(None)
    assert product.get_electricity_source() == "default"
    custom_source.set_scenario.assert_called_with("MidCase")

    product.set_electricity_source("custom")
    product.set_electricity_year(None)
    assert product.get_electricity_source() == "default"
    custom_source.set_year.assert_called_with(product.get_production_year())

    product.set_electricity_source("custom")
    product.set_electricity_geographical_scope(None)
    assert product.get_electricity_source() == "default"
    custom_source.set_geographical_scope.assert_called_with("National")


def test_electricity_mixin_rejects_unknown_source_and_reset_clears_state():
    product = Product()

    with pytest.raises(KeyError, match="Source of electricty"):
        product.set_electricity_source("unknown")

    product.electricity["default"] = object()
    product.electricity["_current"] = "default"
    product.electricity["_tag"] = "Electricity_"
    product.reset_electricity()

    assert product.electricity == {
        "default": None,
        "custom": None,
        "_current": None,
        "_tag": None,
    }


def test_electricity_mixin_finds_supported_database_tag():
    database = Mock()
    database.get_data_entry.return_value = {
        "elec_Qty": 1.0,
        "elec_Unit": "MWh",
    }
    database.get_qty_key.return_value = "Qty"
    database.get_unit_key.return_value = "Unit"
    product = Product()
    product.impact_database_entry = "Concrete"
    product.set_model(DummyModel(database))

    assert product.get_electricity_database_tag() == "elec_"
    assert product.electricity["_tag"] == "elec_"
    assert product.get_electricity() is None


def test_electricity_mixin_returns_no_tag_when_item_has_no_database_entry():
    product = Product()

    assert product.get_electricity_database_tag() is None
