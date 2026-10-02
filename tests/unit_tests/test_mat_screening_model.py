import csv
from unittest.mock import Mock

import pytest

import pod_lca.lca_modules.materials_screening.model as model_module
from pod_lca.carbon_storage import CarbonStorage
from pod_lca.impacts import Emissions, Impacts
from pod_lca.materials_screening import Electricity, Model, Process, Product, Project
from pod_lca.units import KILOGRAM, KILO, WATT_HOUR, CUBIC_METER


class DummyLocation:
    def __init__(self, country_code=None):
        self.country_code = country_code

    def get_country_code(self):
        return self.country_code


class DummyProject:
    def __init__(self, location=None, year=2025):
        self.location = location
        self.year = year
        self.models = {}
        self.transport_database = None

    def get_location(self):
        return self.location

    def get_year(self):
        return self.year

    def get_transportation_mode_impact_database(self):
        return self.transport_database

    def check_model_names(self, name):
        return name or "Model_1"


class DummyTransportationManager:
    def __init__(self):
        self.legs = []
        self.project_destination = None
        self.impact_database = None
        self.removed_goods = []
        self.set_impact_database_calls = []

    def get_transportation_legs(self):
        return self.legs

    def get_impacts_list(self):
        return []

    def get_impacts(self):
        return Impacts.from_parent(None)

    def get_emissions(self):
        return Emissions.from_parent(None)

    def get_carbon_storage(self):
        return CarbonStorage.from_parent(None)

    def set_project_destination(self, location):
        self.project_destination = location

    def set_impact_database(self, database):
        self.impact_database = database
        self.set_impact_database_calls.append(database)

    def remove_good(self, item):
        self.removed_goods.append(item)

    def get_impact_database(self):
        return self.impact_database

    def get_transportation_leg(self, product):
        return None


class DummyImpact:
    def __init__(self, values, parent=None):
        self.values = values
        self.parent = parent

    def get_record(self, category):
        return self.values.get(category, 0.0)

    def get_weighted_impact(self):
        return self.values.get("weighted", 0.0)

    def get_parent(self):
        return self.parent


def test_model_initialization_setters_and_item_accessors():
    model = Model()
    project = DummyProject()
    location = DummyLocation()
    process = Process()
    product = Product()
    manager = DummyTransportationManager()

    assert model.get_project() is None
    assert model.get_name() is None
    assert model.get_location() is None
    assert model.get_products() == []
    assert model.get_processes() == []
    model.transportation_manager = DummyTransportationManager()
    assert model.get_all_items() == []
    assert model.get_impacts() == {"A1": [], "A3": [], "A2": []}

    model.set_project(project).set_name("Assembly").set_location(location)
    model.products.append(product)
    model.processes.append(process)
    model.transportation_manager = manager
    manager.legs.append("freight")

    assert model.get_project() is project
    assert model.get_name() == "Assembly"
    assert model.get_location() is location
    assert model.get_transportation_manager() is manager
    assert model.get_all_items() == [product, process, "freight"]
    assert model.get_all_items(products=False, transportation=False) == [process]


def test_model_in_project_selects_transport_manager_and_database(monkeypatch):
    manager = DummyTransportationManager()
    regular_factory = Mock()
    regular_factory.new.return_value = manager
    us_factory = Mock()
    us_factory.new.return_value = manager
    monkeypatch.setattr(model_module, "TransportationManager", regular_factory)
    monkeypatch.setattr(model_module, "USTransportationManager", us_factory)
    project = DummyProject(location=DummyLocation("US"))
    project.transport_database = object()

    model = Model.in_project(project, "Model A")

    assert model.get_project() is project
    assert model.get_name() == "Model A"
    assert model.get_location() is project.get_location()
    us_factory.new.assert_called_once_with("Model A")
    assert manager.set_impact_database_calls == [project.transport_database]


@pytest.mark.parametrize(
    ("location", "expected_factory"),
    [
        (None, "regular"),
        (DummyLocation("US"), "us"),
        (DummyLocation("CA"), "regular"),
    ],
)
def test_model_transport_manager_factory_depends_on_project_location(
    monkeypatch, location, expected_factory
):
    regular_manager = DummyTransportationManager()
    us_manager = DummyTransportationManager()
    regular_factory = Mock()
    regular_factory.new.return_value = regular_manager
    us_factory = Mock()
    us_factory.new.return_value = us_manager
    monkeypatch.setattr(model_module, "TransportationManager", regular_factory)
    monkeypatch.setattr(model_module, "USTransportationManager", us_factory)
    model = Model().set_project(DummyProject(location)).set_name("Factory test")

    assert model.set_transportation_manager("global") is model
    if expected_factory == "us":
        us_factory.new.assert_called_once_with("Factory test")
        regular_factory.new.assert_not_called()
        assert model.get_transportation_manager() is us_manager
    else:
        regular_factory.new.assert_called_once_with("Factory test")
        us_factory.new.assert_not_called()
        assert model.get_transportation_manager() is regular_manager


def test_model_set_project():
    model = Model()
    project = DummyProject()
    model.set_project(project)

    assert model.get_project() is project


def test_model_name_set_and_get():
    model = Model()
    model.set_name("Test Model")
    assert model.get_name() == "Test Model"


def test_model_location_is_propagated_to_electricity_and_transport_manager():
    model = Model()

    location = DummyLocation()
    electricity = Electricity()
    electricity.set_location = Mock()

    manager = DummyTransportationManager()
    model.products.append(electricity)
    model.transportation_manager = manager

    assert model.set_location(location) is model
    assert model.get_location() is location

    electricity.set_location.assert_called_once_with(location_obj=location)

    assert manager.project_destination is location


def test_create_model_in_project():
    project = DummyProject()
    model = Model.in_project(project, "Example")

    assert model.get_name() == "Example"
    assert model.get_project() is project
    assert model.get_impacts()["A1"] == []
    assert model.get_impacts()["A3"] == []
    assert model.get_emissions()["A1"] == []
    assert model.get_emissions()["A3"] == []
    assert model.get_carbon_storage()["A1"] == []
    assert model.get_carbon_storage()["A3"] == []


def test_model_from_csv_sets_location_and_transportation_manager(tmp_path):
    project = DummyProject()
    csv_file = tmp_path / "model.csv"
    csv_file.write_text("Name,qty,unit,LC stage\nConcrete,2.5,kg,A1\n")
    model = Model.from_CSV(csv_file, project, name="Example", transport_scope="local")

    assert model.get_name() == "Example"
    assert model.get_project() is project
    assert model.get_location() is None 


def test_model_add_process_registers_item_and_inventory_records():
    model = Model()
    model.set_project(DummyProject())
    model.set_name("Manufacturing")
    model.transportation_manager = DummyTransportationManager()

    process = model.add_process("Mixing", "A3", 2, KILOGRAM, None)

    assert process.get_id() == 0
    assert process.get_name() == "Mixing"
    assert process.get_qty() == 2
    assert model.get_processes() == [process]
    assert process.impacts in model.impacts["A3"]
    assert process.emissions in model.emissions["A3"]
    assert process.carbon_storage in model.carbon_storage["A3"]
    assert model.get_all_items(products=False, transportation=False) == [process]


def test_model_add_product_registers_item_and_inventory_records():
    model = Model()
    model.set_project(DummyProject())
    model.set_name("Manufacturing")
    model.transportation_manager = DummyTransportationManager()

    product = model.add_product("Concrete", "A1", 2, KILOGRAM, None)

    assert product.get_id() == 0
    assert product.get_name() == "Concrete"
    assert product.get_qty() == 2
    assert model.get_products() == [product]
    assert product.impacts in model.impacts["A1"]
    assert product.emissions in model.emissions["A1"]
    assert product.carbon_storage in model.carbon_storage["A1"]
    assert model.get_all_items(transportation=False) == [product]


def test_model_add_fuel_registers_item_and_inventory_records():
    project = DummyProject()
    model = Model()
    model.set_project(project)
    model.set_name("Manufacturing")
    model.transportation_manager = DummyTransportationManager()

    fuel = model.add_energy("Natural gas", "A3", 2, CUBIC_METER, None)

    assert fuel.get_id() == 0
    assert fuel.get_name() == "Natural gas"
    assert fuel.get_qty() == 2
    assert model.get_products() == [fuel]
    assert fuel.impacts in model.impacts["A3"]
    assert fuel.emissions in model.emissions["A3"]
    assert fuel.carbon_storage in model.carbon_storage["A3"]
    assert model.get_all_items(transportation=False) == [fuel]
    assert fuel.get_emissions().get_start_year() == project.get_year()


def test_model_add_electricity_registers_item_and_inventory_records():
    model = Model()
    model.set_project(DummyProject())
    model.set_name("Manufacturing")
    model.transportation_manager = DummyTransportationManager()

    electricity = model.add_electricity("Electricity", "A3", 100, KILO * WATT_HOUR)

    assert electricity.get_id() == 0
    assert electricity.get_name() == "Electricity"
    assert electricity.get_qty() == 100
    assert model.get_products() == [electricity]
    assert electricity.impacts in model.impacts["A3"]
    assert electricity.emissions in model.emissions["A3"]
    assert electricity.carbon_storage in model.carbon_storage["A3"]
    assert model.get_all_items(transportation=False) == [electricity]


def test_model_finds_items_and_returns_none_for_missing_names():
    model = Model()
    product = Product()
    product.set_name("Timber")
    process = Process()
    process.set_name("Curing")
    model.products.append(product)
    model.processes.append(process)

    assert model.find_item("Timber") is product
    assert model.find_item("Curing") is process
    assert model.find_item("missing") is None


@pytest.mark.parametrize("item_type", [Product, Process])
def test_model_deletes_items_and_unregisters_inventory(item_type, monkeypatch):
    model = Model()
    manager = DummyTransportationManager()
    model.transportation_manager = manager
    item = item_type()
    item.set_name("removable")
    item.set_life_cycle_stage("A1")
    item.set_model(model)
    item.remove_inventory_records_from_model = Mock()
    inventory = Impacts.from_parent(item)
    if item_type is Product:
        model.products.append(item)
    else:
        model.processes.append(item)
    model.impacts["A1"].append(inventory)
    monkeypatch.setattr(model_module.gc, "collect", Mock())

    model.delete_item(item)

    assert item not in model.get_all_items(transportation=False)
    assert manager.removed_goods == [item]
    item.remove_inventory_records_from_model.assert_called_once_with("A1")


@pytest.mark.parametrize(
    ("grouping", "plus_minus_accounting", "expected_a1", "expected_a2", "expected_a3"),
    [
        ("not_grouped", True, 10.0, 5.0, 20.0),
        ("all_transportation", True, 10.0, 8.0, 20.0),
        ("with_material", True, 15.0, None, 20.0),
        ("not_grouped", False, 30.0, 5.0, None),
    ],
)
def test_model_get_impacts_respects_grouping_and_plus_minus_options(
    grouping, plus_minus_accounting, expected_a1, expected_a2, expected_a3
):
    model = Model()
    manager = DummyTransportationManager()
    transportation_impacts = Impacts.from_dict({"GWP": 5.0})
    all_transportation_impacts = Impacts.from_dict({"GWP": 8.0})
    manager.get_impacts_list = lambda: [transportation_impacts]
    manager.get_impacts = lambda *args: all_transportation_impacts
    model.transportation_manager = manager

    product = Product()
    product.set_model(model)
    product.set_name("Timber")
    product.set_life_cycle_stage("A1")
    product.get_cache_key = Mock(return_value=("fixed-cache-key",))
    product.update_inventory_records = Mock()
    product._last_params.update(
        {"A1": ("fixed-cache-key",), "A3": ("fixed-cache-key",)}
    )
    product._cache_is_computed.update({"A1": True, "A3": True})
    product_impacts = {
        "A1": Impacts.from_dict({"GWP": 10.0}).set_parent(product),
        "A3": Impacts.from_dict({"GWP": 20.0}).set_parent(product),
        None: Impacts.from_dict({"GWP": 30.0}).set_parent(product),
    }
    product.get_impacts = Mock(side_effect=lambda stage=None: product_impacts[stage])
    product.get_transportation = Mock(return_value=[object()])
    model.products.append(product)

    manager.get_impacts = lambda *args: (
        Impacts.from_dict({"GWP": 5.0})
        if args
        else all_transportation_impacts
    )

    impacts = model.get_impacts(
        transportation_grouping=grouping,
        plus_minus_accounting=plus_minus_accounting,
    )

    assert sum(record.get_record("GWP") for record in impacts["A1"]) == pytest.approx(expected_a1)
    for stage, expected in [("A2", expected_a2), ("A3", expected_a3)]:
        if expected is None:
            assert impacts[stage] == []
        else:
            assert sum(record.get_record("GWP") for record in impacts[stage]) == pytest.approx(
                expected
            )
    if plus_minus_accounting:
        assert product.get_impacts.call_args_list == [(("A1",),), (("A3",),)]
        product.update_inventory_records.assert_not_called()
    else:
        product.get_impacts.assert_called_once_with()


def test_model_calculates_impact_totals_and_stage_breakdown():
    model = Model()
    model.get_impacts = Mock(
        return_value={
            "A1": [DummyImpact({"GWP": 2.0, "weighted": 0.5})],
            "A3": [DummyImpact({"GWP": 3.0, "weighted": 1.25})],
            "A2": [],
        }
    )

    assert model.get_total_impact("GWP") == 5.0
    assert model.get_total_impact("weighted") == pytest.approx(1.75)
    assert model.get_impacts_by_LCstages("GWP") == {
        "A1": 2.0,
        "A2": 0.0,
        "A3": 3.0,
    }
    with pytest.raises(AttributeError, match="not_a_category does not exist"):
        model.get_total_impact("not_a_category")
    with pytest.raises(AttributeError, match="not_a_category does not exist"):
        model.get_impacts_by_LCstages("not_a_category")


def test_model_reports_hotspots_and_category_totals(monkeypatch):
    import pod_lca.lca_modules.materials_screening.model as module

    categories = module.config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
    hotspot = Mock()
    hotspot.is_hotspot = True
    hotspot.get_name.return_value = "Hotspot item"
    ordinary = Mock()
    ordinary.is_hotspot = False
    model = Model()
    model.get_impacts = Mock(
        return_value={
            "A1": [
                DummyImpact({"GWP": 2.0}, hotspot),
                DummyImpact({"GWP": 3.0}, ordinary),
            ],
            "A3": [],
        }
    )

    result = model.get_impacts_by_LCstages_with_hotspots("GWP")
    assert result == {
        "A1": {"Hotspot item": 2.0, "other": 3.0},
        "A3": {"other": 0.0},
    }

    model.get_impacts_by_LCstages = Mock(
        side_effect=lambda category: {"A1": 2.0, "A3": 3.0}
    )
    by_category = model.get_impacts_by_category()
    assert set(by_category) == set(categories)
    assert by_category["GWP"] == 5.0


def test_model_normalizes_impacts_and_validates_missing_factor(monkeypatch):
    categories = model_module.config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
    model = Model()
    model.get_impacts_by_LCstages = Mock(
        side_effect=lambda category: {"A1": 8.0, "A3": 2.0}
    )
    monkeypatch.setattr(
        model_module.DataImporter,
        "json_to_dict",
        lambda path: {category: 2.0 for category in categories},
    )

    results = model.get_normalized_impacts_by_category()

    assert results["GWP"] == 5.0
    assert set(results) == set(categories)

    monkeypatch.setattr(
        model_module.DataImporter,
        "json_to_dict",
        lambda path: {"GWP": 2.0},
    )
    with pytest.raises(KeyError, match="not found in weights"):
        model.get_normalized_impacts_by_category()


def test_model_gets_total_carbon_storage_by_requested_type(monkeypatch):
    class DummyStorage:
        def get_biogenic_carbon_storage_qty(self, unit):
            return 2.0

        def get_mineral_carbon_storage_qty(self, unit):
            return 3.0

    item = Mock()
    item.get_carbon_storage.return_value = DummyStorage()
    model = Model()
    model.get_carbon_storage = Mock(return_value={"A1": [DummyStorage()]})
    model.get_all_items = Mock(return_value=[item])

    assert model.get_total_carbon_storage_effects("biogenic") == 2.0
    assert model.get_total_carbon_storage_effects("mineral") == 3.0
    assert model.get_total_carbon_storage_effects("total") == 5.0
    assert model.get_total_stored_biogenic_carbon() == 2.0


def test_model_sets_electricity_source_for_products_but_skips_electricity():
    model = Model()
    product = Product()
    product.set_electricity_source = Mock()
    electricity = Electricity()
    electricity.set_electricity_source = Mock()
    model.products = [product, electricity]

    assert model.set_products_electricity_source("custom") is model

    product.set_electricity_source.assert_called_once_with("custom")
    electricity.set_electricity_source.assert_not_called()


def test_model_gets_dynamic_radiative_forcing_record(monkeypatch):
    project = DummyProject(year=2040)
    model = Model().set_project(project)
    model.get_all_items = Mock(return_value=["item"])
    drf_record = object()
    from_products = Mock(return_value=drf_record)
    monkeypatch.setattr(
        model_module.DynamicRadiativeForcingRecord,
        "from_products",
        from_products,
    )

    result = model.get_drf_record(time_horizon=50, time_step=0.5)

    assert result is drf_record
    from_products.assert_called_once_with(["item"], 2040, 50, 0.5)
