import pandas as pd
import pytest

import pod_lca.lca_modules.materials_screening.product_transportation_mixins as mixin_module
from pod_lca.materials_screening import Product
from pod_lca.units import CUBIC_METER, KILOGRAM, KILOMETER, MILE


class DummyLeg:
    def __init__(self):
        self.transport_scenario = "Local"
        self.mode = "Truck"
        self.efficiency = "Median"
        self.calls = []
        self.emissions = DummyEmissions()

    def set_transport_scenario(self, scenario):
        self.transport_scenario = scenario

    def get_transport_scenario(self):
        return self.transport_scenario

    def set_mode(self, **kwargs):
        self.calls.append(kwargs)
        self.mode = kwargs.get("mode", self.mode)
        self.efficiency = kwargs.get("efficiency", self.efficiency)

    def get_mode(self):
        return DummyMode(self.mode, self.efficiency)

    def get_emissions(self):
        return self.emissions


class DummyEmissions:
    def __init__(self):
        self.profile = None

    def set_temporal_emission_profile(self, profile):
        self.profile = profile


class DummyMode:
    def __init__(self, name, efficiency):
        self.name = name
        self.efficiency = efficiency

    def get_name(self):
        return self.name

    def get_efficiency(self):
        return self.efficiency


class DummyTransportationManager:
    def __init__(self, legs=None, database=None, impacts=None):
        self.legs = legs
        self.database = database
        self.impacts = impacts
        self.add_good_args = None
        self.removed_goods = []

    def get_transportation_leg(self, product):
        return self.legs

    def get_impact_database(self):
        return self.database

    def add_good(self, *args, **kwargs):
        self.add_good_args = (args, kwargs)

    def remove_good(self, product):
        self.removed_goods.append(product)

    def get_impacts(self, product):
        return self.impacts


class DummyProject:
    def __init__(self, location=None, impact_database=None):
        self.location = location
        self.impact_database = impact_database

    def get_location(self):
        return self.location

    def get_impact_database(self):
        return self.impact_database


class DummyModel:
    def __init__(self, manager, project=None):
        self.transportation_manager = manager
        self.project = project

    def get_transportation_manager(self):
        return self.transportation_manager

    def get_project(self):
        return self.project


def test_sctg_code_setter_and_getter_support_precision_and_missing_code():
    product = Product()

    assert product.set_sctg_code("1234") is product
    assert product.get_sctg_code() == 12
    assert product.get_sctg_code(digits=4) == 1234
    with pytest.raises(ValueError, match="shorter than digits requested"):
        product.get_sctg_code(digits=5)

    product.set_sctg_code(None)
    assert product.get_sctg_code() == 12


def test_sctg_code_is_looked_up_by_product_name(monkeypatch):
    product = Product()
    product.set_name("Timber")
    data = pd.DataFrame({"material": ["Timber", "Steel"], "SCTG code": [25, 31]})
    monkeypatch.setattr(mixin_module.DataImporter, "csv_to_pandas", lambda path: data)

    assert product.set_sctg_code() is product
    assert product.sctg_code == "25"


def test_sctg_code_lookup_without_match_keeps_existing_code(monkeypatch):
    product = Product()
    product.set_name("Unknown")
    product.set_sctg_code("42")
    data = pd.DataFrame({"material": ["Timber"], "SCTG code": [25]})
    monkeypatch.setattr(mixin_module.DataImporter, "csv_to_pandas", lambda path: data)

    assert product.set_sctg_code() is product
    assert product.sctg_code == "42"


def test_set_transportation_returns_early_without_unit():
    product = Product()

    assert product.set_transportation(travel_dist=100) is product


def test_set_transportation_adds_good_with_defaults_and_emission_profile():
    leg = DummyLeg()
    manager = DummyTransportationManager([leg], database=object())
    product = Product()
    product.set_unit(KILOGRAM)
    product.set_model(
        DummyModel(manager, project=DummyProject(location="destination"))
    )
    # Set directly: Product.set_production_year also updates item emissions,
    # which is outside the transportation mixin's behavior under test.
    product.production_year = 2035

    assert product.set_transportation() is product

    args, kwargs = manager.add_good_args
    assert args == (product,)
    assert kwargs == {
        "travel_dist": None,
        "shipping_dest": "destination",
        "shipping_org": None,
        "transport_scenario": "Local",
        "distance_unit": KILOMETER,
        "return_trip_factor": None,
        "mode_name": "Truck",
        "mode_efficiency": "Median",
    }
    assert leg.emissions.profile.get_start() == 2035


def test_set_transportation_uses_explicit_options_and_sets_density(monkeypatch):
    manager = DummyTransportationManager([], database=object())
    product = Product()
    product.set_unit(CUBIC_METER)
    product.set_model(
        DummyModel(manager, project=DummyProject(location="destination"))
    )
    monkeypatch.setattr(product, "set_density", lambda: setattr(product, "density", 42))

    assert product.set_transportation(
        travel_dist=12,
        dist_unit=MILE,
        shipping_org="origin",
        transport_scenario="National",
        return_trip_factor=1.5,
        mode_name="Rail",
        mode_efficiency="High",
    ) is product

    assert product.get_density() == 42
    _, kwargs = manager.add_good_args
    assert kwargs == {
        "travel_dist": 12,
        "shipping_dest": "destination",
        "shipping_org": "origin",
        "transport_scenario": "National",
        "distance_unit": MILE,
        "return_trip_factor": None,
        "mode_name": "Rail",
        "mode_efficiency": "High",
    }


def test_set_transportation_does_not_add_good_without_transport_database():
    manager = DummyTransportationManager([], database=None)
    product = Product()
    product.set_unit(KILOGRAM)
    product.set_model(DummyModel(manager, project=DummyProject()))

    assert product.set_transportation(travel_dist=12) is product
    assert manager.add_good_args is None


def test_transportation_getter_returns_none_without_manager():
    product = Product()
    product.set_model(DummyModel(None))

    assert product.get_transportation_manager() is None
    assert product.get_transportation() is None


def test_domestic_transportation_leg_can_be_read_and_updated(monkeypatch):
    leg = DummyLeg()
    monkeypatch.setattr(mixin_module, "DomesticLeg", DummyLeg)
    monkeypatch.setattr(mixin_module, "ForeignLeg", type("ForeignLeg", (), {}))
    product = Product()
    product.set_unit(KILOGRAM)
    product.set_model(DummyModel(DummyTransportationManager([leg])))

    assert product.get_transportation() == [leg]
    product.set_transport_scenario("Regional")
    product.set_transport_mode("Rail")
    product.set_transport_mode_efficiency("High")

    assert product.get_transport_scenario() == "Regional"
    assert product.get_transport_mode() == "Rail"
    assert product.get_transport_mode_efficiency() == "High"
    assert leg.calls == [{"mode": "Rail"}, {"efficiency": "High"}]


def test_foreign_leg_mode_is_updated_but_scenario_is_not(monkeypatch):
    foreign_leg_type = type("ForeignLeg", (DummyLeg,), {})
    leg = foreign_leg_type()
    monkeypatch.setattr(mixin_module, "DomesticLeg", type("DomesticLeg", (), {}))
    monkeypatch.setattr(mixin_module, "ForeignLeg", foreign_leg_type)
    product = Product()
    product.set_model(DummyModel(DummyTransportationManager([leg])))

    product.set_transport_scenario("Global")
    product.set_transport_mode("Ocean")
    product.set_transport_mode_efficiency("Low")

    assert product.get_transport_scenario() == "Local"
    assert product.get_transport_mode() == "Ocean"
    assert product.get_transport_mode_efficiency() == "Low"
    assert leg.calls == [{"mode": "Ocean"}, {"efficiency": "Low"}]


def test_transportation_clear_and_impact_methods_delegate_to_manager():
    impacts = object()
    manager = DummyTransportationManager([], impacts=impacts)
    product = Product()
    product.set_model(DummyModel(manager))

    assert product.clear_transportation() is product
    assert manager.removed_goods == [product]
    assert product.get_transportation_impacts() is impacts


def test_default_sctg_code_uses_database_code_when_available():
    product = Product()
    product.impact_database_entry = "Concrete"
    database = type(
        "DummyDatabase",
        (),
        {"get_data_entry": lambda self, entry: {"SCTG code": 251}},
    )()
    product.set_model(
        DummyModel(None, project=DummyProject(impact_database=database))
    )

    assert product.get_default_sctg_code() == "251"


def test_default_sctg_code_maps_naics_subcategory_and_category(monkeypatch):
    product = Product()
    product.impact_database_entry = "Concrete"
    mapping = pd.DataFrame(
        {
            "NAICS Sub-category": ["ready-mix"],
            "NAICS Category": ["construction"],
            "SCTG Category": pd.Series([327], dtype=object),
        }
    )
    monkeypatch.setattr(
        mixin_module.DataImporter, "csv_to_pandas", lambda path: mapping
    )
    data = {"NAICS Sub-category": "ready-mix"}
    database = type("DummyDatabase", (), {"get_data_entry": lambda self, entry: data})()
    product.set_model(
        DummyModel(None, project=DummyProject(impact_database=database))
    )
    assert product.get_default_sctg_code() == "32"

    data.clear()
    data["NAICS Category"] = "unmapped"
    assert product.get_default_sctg_code() == "N/A"


def test_default_sctg_code_returns_na_for_unmapped_naics(monkeypatch):
    product = Product()
    product.impact_database_entry = "Unknown"
    mapping = pd.DataFrame(
        {"NAICS Sub-category": ["known"], "SCTG Category": [327]}
    )
    monkeypatch.setattr(
        mixin_module.DataImporter, "csv_to_pandas", lambda path: mapping
    )
    database = type(
        "DummyDatabase",
        (),
        {"get_data_entry": lambda self, entry: {"NAICS Sub-category": "unknown"}},
    )()
    product.set_model(
        DummyModel(None, project=DummyProject(impact_database=database))
    )

    assert product.get_default_sctg_code() == "N/A"


def test_default_sctg_code_falls_back_to_configured_default_for_missing_entry():
    product = Product()
    product.impact_database_entry = None

    assert (
        product.get_default_sctg_code()
        == mixin_module.config["setup"]["transportation"]["DEFAULT_SCTG_CODE"]
    )
