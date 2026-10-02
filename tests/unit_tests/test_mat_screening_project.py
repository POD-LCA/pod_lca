from unittest.mock import Mock

import pytest

from pod_lca.materials_screening import Project


class DummyLocation:
    pass


class DummyItem:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class DummyImpact:
    def __init__(self, parent, values):
        self.parent = parent
        self.values = values

    def get_parent(self):
        return self.parent

    def get_record(self, category):
        return self.values[category]


class DummyModel:
    def __init__(self, name, stage_impacts, items_by_stage=None):
        self.name = name
        self.stage_impacts = stage_impacts
        self.items_by_stage = items_by_stage or {}
        self.location = None

    def get_name(self):
        return self.name

    def set_location(self, location):
        self.location = location

    def get_impacts_by_LCstages(self, category):
        return {
            stage: values.get(category, 0.0)
            for stage, values in self.stage_impacts.items()
        }

    def get_impacts(self):
        return self.items_by_stage


@pytest.fixture
def named_project():
    return Project.new("Project tests")


def test_new_project_initializes_with_name_and_empty_models():
    project = Project.new("Buildings")

    assert isinstance(project, Project)
    assert project.get_name() == "Buildings"
    assert project.get_model_names() == []


def test_project_defaults_setters_and_string_representation():
    project = Project()

    assert project.get_name() is None
    assert project.get_model_names() == []
    assert project.get_location() is None
    assert project.get_year() is None
    assert project.get_impact_database() is None
    assert project.get_transportation_mode_impact_database() is None

    location = DummyLocation()
    assert project.set_name("Buildings") is project
    assert project.set_location(location) is project
    assert project.set_year(2030) is project

    model = DummyModel("Baseline", {})
    project.models["Baseline"] = model
    assert project.get_location() is location
    assert project.get_year() == 2030
    assert project.get_model_names() == ["Baseline"]
    assert "Project: Buildings" in str(project)
    assert "Baseline" in str(project)


def test_project_location_updates_existing_models(named_project):
    model = DummyModel("Baseline", {})
    named_project.models[model.name] = model
    location = DummyLocation()

    named_project.set_location(location)

    assert named_project.get_location() is location
    assert model.location is location


def test_add_model_from_csv_and_retrieve_by_name(named_project, tmp_path):
    csv_file = tmp_path / "model.csv"
    csv_file.write_text("Name,qty,unit,LC stage\nConcrete,2.5,kg,A1\n")
    model = named_project.add_model("Baseline", csv_file)

    assert model.get_name() == "Baseline"
    assert named_project.get_model("Baseline") is model
    assert named_project.get_model_names() == ["Baseline"]


def test_project_adds_and_names_models(named_project):
    baseline = named_project.add_model("Baseline")
    renamed_baseline = named_project.add_model("Baseline")
    unnamed = named_project.add_model(None)

    assert baseline.get_name() == "Baseline"
    assert renamed_baseline.get_name() == "Baseline_2"
    assert unnamed.get_name() == "Model_1"
    assert baseline.get_project() is named_project
    assert named_project.get_model("Baseline") is baseline
    assert named_project.get_model("Baseline_2") is renamed_baseline
    assert named_project.get_model("Model_1") is unnamed


@pytest.mark.parametrize(
    ("existing_names", "requested", "expected"),
    [
        ([], "Option", "Option"),
        (["Option"], "Option", "Option_2"),
        (["Option", "Option_2", "Option_8"], "Option", "Option_9"),
        (["Model_1", "Model_4"], None, "Model_5"),
    ],
)
def test_project_checks_for_duplicate_model_names(
    named_project, existing_names, requested, expected
):
    named_project.models = {name: object() for name in existing_names}

    assert named_project.check_model_names(requested) == expected


def test_project_removes_and_clears_models_and_database(named_project):
    model = DummyModel("Baseline", {})
    named_project.models[model.name] = model
    database = object()
    named_project.impact_database = database
    named_project.transport_mode_impact_database = object()

    named_project.remove_model("missing")
    assert named_project.get_model_names() == ["Baseline"]

    named_project.clear_project(model=False, database=True)
    assert named_project.get_model_names() == ["Baseline"]
    assert named_project.get_impact_database() is None

    named_project.impact_database = database
    named_project.clear_project(database=False)
    assert named_project.get_model_names() == []
    assert named_project.get_impact_database() is database


def test_project_sets_and_gets_material_impact_database(named_project, monkeypatch, tmp_path):
    import pod_lca.lca_modules.materials_screening.project_manager as project_module

    database = Mock()
    database_factory = Mock()
    database_factory.new.return_value = database
    monkeypatch.setattr(project_module, "ImpactsDatabase", database_factory)
    csv_path = tmp_path / "materials.csv"

    named_project.set_material_database(csv_path)

    database_factory.new.assert_called_once_with("impact database")
    database.set_primary_key.assert_called_once_with("Name")
    database.set_qty_key.assert_called_once_with("Qty")
    database.set_unit_key.assert_called_once_with("Unit")
    database.set_data.assert_called_once()
    assert database.set_data.call_args.args == (csv_path,)
    assert database.set_data.call_args.kwargs["grouped_data"] == "Electricity"
    assert database.set_data.call_args.kwargs["density_headers"] == [
        "Density",
        "Density unit",
    ]
    assert named_project.get_impact_database() is database


def test_project_sets_and_gets_transportation_impact_database(
    named_project, monkeypatch, tmp_path
):
    import pod_lca.lca_modules.materials_screening.project_manager as project_module

    database = Mock()
    database_factory = Mock()
    database_factory.new.return_value = database
    monkeypatch.setattr(
        project_module,
        "TranportationModeImpactsDatabase",
        database_factory,
    )
    csv_path = tmp_path / "transportation.csv"

    assert named_project.set_transportation_mode_impact_database(csv_path) is named_project

    database_factory.new.assert_called_once_with("impact database")
    database.set_data.assert_called_once_with(csv_path)
    assert named_project.get_transportation_mode_impact_database() is database


def test_project_sets_eol_database_with_custom_headers(named_project, monkeypatch, tmp_path):
    import pod_lca.lca_modules.materials_screening.project_manager as project_module

    database = Mock()
    database_factory = Mock()
    database_factory.new.return_value = database
    monkeypatch.setattr(project_module, "EOLImpactsDatabase", database_factory)
    csv_path = tmp_path / "eol.csv"

    assert named_project.set_eol_process_impact_database(
        csv_path,
        primary_key="Material name",
        process_key="Pathway",
        lc_stage_key="Stage",
    ) is named_project

    database_factory.new.assert_called_once_with("EOL database")
    database.set_primary_key.assert_called_once_with("Material name")
    database.set_process_key.assert_called_once_with("Pathway")
    database.set_life_cycle_stage_key.assert_called_once_with("Stage")
    database.set_data.assert_called_once_with(csv_path)
    assert named_project.eol_impact_database is database


def test_project_rejects_invalid_database_inputs(named_project):
    with pytest.raises(TypeError, match="Database input not recognized"):
        named_project.set_material_database(123)
    with pytest.raises(TypeError, match="Database input not recognized"):
        named_project.set_transportation_mode_impact_database(123)
    with pytest.raises(TypeError, match="Database input not recognized"):
        named_project.set_eol_process_impact_database(123)


def test_project_sets_eol_transport_dataset(named_project, monkeypatch):
    import pod_lca.lca_modules.materials_screening.project_manager as project_module

    dataset = object()
    assert named_project.set_eol_transport_dataset(dataset) is named_project
    assert named_project.eol_transport_dataset is dataset

    default_dataset = object()
    dataset_factory = Mock(return_value=default_dataset)
    monkeypatch.setattr(project_module, "EOLTransportDataset", dataset_factory)

    assert named_project.set_eol_transport_dataset() is named_project
    dataset_factory.assert_called_once_with()
    assert named_project.eol_transport_dataset is default_dataset


def test_project_set_databases_initializes_each_database_and_dataset(named_project):
    named_project.set_material_database = Mock()
    named_project.set_transportation_mode_impact_database = Mock()
    named_project.set_eol_process_impact_database = Mock()
    named_project.set_eol_transport_dataset = Mock()

    assert named_project.set_databases() is named_project

    named_project.set_material_database.assert_called_once_with()
    named_project.set_transportation_mode_impact_database.assert_called_once_with()
    named_project.set_eol_process_impact_database.assert_called_once_with()
    named_project.set_eol_transport_dataset.assert_called_once_with()


def test_project_save_and_load_round_trip(named_project, tmp_path):
    named_project.set_year(2040)
    named_project.models["Reference"] = DummyModel("Reference", {})
    path = tmp_path / "project.pkl"

    named_project.save(path)
    restored = Project.load(path)

    assert isinstance(restored, Project)
    assert restored.get_name() == "Project tests"
    assert restored.get_year() == 2040
    assert restored.get_model_names() == ["Reference"]
    assert restored.get_model("Reference").get_name() == "Reference"


def test_project_aggregates_impact_summaries_across_models(named_project):
    baseline = DummyModel(
        "Baseline",
        {"A1": {"GWP": 2.0}, "A3": {"GWP": 3.0}},
    )
    alternative = DummyModel(
        "Alternative",
        {"A1": {"GWP": 4.0}, "A3": {"GWP": 1.0}},
    )
    named_project.models = {baseline.name: baseline, alternative.name: alternative}

    assert named_project.get_impacts_by_LCstages_models("GWP") == {
        "Baseline": {"A1": 2.0, "A3": 3.0},
        "Alternative": {"A1": 4.0, "A3": 1.0},
    }
    assert named_project.get_impacts_by_LCstages_models(
        "GWP", model_lst=["Alternative"]
    ) == {"Alternative": {"A1": 4.0, "A3": 1.0}}

    category_totals = named_project.get_impacts_by_category_models(
        model_lst=["Baseline"]
    )
    assert category_totals["Baseline"]["GWP"] == 5.0
    assert set(category_totals["Baseline"]) == set(
        named_project.get_impacts_by_category_models()["Baseline"]
    )


def test_project_returns_item_and_category_stage_impact_breakdowns(named_project):
    timber = DummyItem("Timber")
    concrete = DummyItem("Concrete")
    named_project.models["Baseline"] = DummyModel(
        "Baseline",
        {"A1": {"GWP": 4.0}, "A3": {"GWP": 1.0}},
        {
            "A1": [DummyImpact(timber, {"GWP": 4.0})],
            "A3": [DummyImpact(concrete, {"GWP": 1.0})],
            "A2": [],
        },
    )

    assert named_project.get_impacts_by_LCstages_models_items("GWP") == {
        "Baseline": {
            "A1": {"Timber": 4.0},
            "A3": {"Concrete": 1.0},
            "A2": {},
        }
    }
    assert named_project.get_impacts_by_impactcategorys_models_LCstage(
        ["GWP"], ["Baseline"]
    ) == {
        "Baseline": {
            "GWP": {"A1": 4.0, "A3": 1.0},
        }
    }


def test_project_normalized_impacts_apply_configured_factors(
    named_project, monkeypatch
):
    import pod_lca.lca_modules.materials_screening.project_manager as project_module

    categories = project_module.config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
    named_project.models["Baseline"] = DummyModel(
        "Baseline",
        {"A1": {"GWP": 2.0}, "A3": {"GWP": 3.0}},
    )
    monkeypatch.setattr(
        project_module,
        "config",
        {
            "setup": {"INVENTORY_ITEMS": {"IMPACT_CATEGORIES": categories}},
            "file_paths": {"IMPACT_NORMALIZATION_FACTOR": "normalization.json"},
        },
    )
    monkeypatch.setattr(
        project_module.DataImporter,
        "json_to_dict",
        lambda path: {category: 2.0 for category in categories},
    )

    results = named_project.get_normalized_impacts_by_category_models()

    assert results["Baseline"]["GWP"] == 10.0
    assert set(results["Baseline"]) == set(categories)

