

# Master object operations
# change name
# add impact

# calculator

from lca_modules.material.project_manager import Project
from lca_modules.material.calculator import Calculator
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.material.model import Model, Product, Process, transportationProcess, Emission, Waste, Fuel

from utilities.units.common_units import KILOGRAM, KILOMETER, WATT_HOUR
from utilities.units.metric_prefixes import KILO

from pandas import DataFrame, Series
import unittest


class TestBuilder(unittest.TestCase):

    def test_01_create_project(self):
        """ Test createing a project.
        """
        print('testing createing a project')

        project = Project()

        self.assertIsInstance(project, Project, " ")

    def test_02_create_new_model(self):
        """ Test createing a new model in the project.
        """
        print('testing createing a new model in the project')

        project = Project()
        new_model = project.add_model("Model_1")

        no_models = len(project.models)

        self.assertIsInstance(new_model, Model, " ")
        self.assertEqual(no_models, 1)
        
    def test_03_save_load_project(self):
        """ Test save/load project.
        """
        print('testing save/load project')

        file_path = r'save_files/test.pkl'
        project = Project()

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(load_project, Project, " ")

    def test_04_import_database(self):
        """ Test importing data to database.
        """
        print('testing importing data to database.')
        
        database_path = r'data/impact_data_smoothie.csv'

        project = Project()

        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(database_path)
        project.set_database(custom_impact_database)

        self.assertIsInstance(project.get_database().get_data_all(), DataFrame, " ")

    def test_05_importing_from_database(self):
        """ Test importing data from database.
        """
        print('testing importing data from database.')

        database_path = r'data/impact_data_smoothie.csv'

        project = Project.new()

        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(database_path)
        project.set_database(custom_impact_database)

        sand_impacts = project.get_database().get_data_entry("Sand")

        self.assertIsInstance(sand_impacts, Series, " ")

    def test_06_create_custom_impact(self):
        """ Test creating a custom impact.
        """
        print('testing creating a custom impact.')

        project = Project()

        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        custom_impact_database.set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                            {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        project.set_database(custom_impact_database)

        Electricity_New_impacts = project.get_database().get_data_entry("Electricity_New")

        self.assertIsInstance(Electricity_New_impacts, Series, " ")

    def test_07_create_product(self):
        """ Test creating a Product.
        """
        print('testing creating a product.')

        file_path = r'save_files/test.pkl'

        project = Project()
        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        custom_impact_database.set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                            {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        project.set_database(custom_impact_database)

        model_0 = project.add_model("Model_0")

        sprinkles = model_0.add_product(name="Sprinkles", stage="A1", qty=2.0, unit=KILOGRAM, impacts_from="Sprinkles")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(sprinkles, Product, " ")

    def test_08_create_process(self):
        """ Test creating a Product.
        """
        print('testing creating a process.')

        file_path = r'save_files/test.pkl'

        project = Project()

        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        project.set_database(custom_impact_database)

        # product_1 = project.current_model.create_product("Product of mixing", "A3")
        # product_1.update_qty(3.0)
        # product_1.set_unit('kg')

        # project.save(file_path)

        # load_project = Project.load(file_path)

        # self.assertIsInstance(product_1, Process, " ")


    def test_09_create_transport_process(self):
        """ Test creating a Transport Process.
        """
        print('testing creating a transportation process.')

        file_path = r'save_files/test.pkl'

        project = Project()
        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        project.set_database(custom_impact_database)

        model_0 = project.add_model("Model_0")

        sprinkles = model_0.add_product(name="Sprinkles", stage="A1", qty=2.0, unit=KILOGRAM, impacts_from="Sprinkles")

        sprinkles_by_truck = model_0.add_transportation_process(name="Sprinkle Transportation", stage="A2",
                                                                transported_distance=30.0, unit=KILOMETER,
                                                                impacts_from="Transportation by truck")
        sprinkles_by_truck.set_transported_product(sprinkles)

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(sprinkles_by_truck, transportationProcess, " ")

    def test_10_create_emission(self):
        """ Test creating a Emission.
        """
        print('testing creating an emission.')

        file_path = r'save_files/test.pkl'

        project = Project()
        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        project.set_database(custom_impact_database)

        model_0 = project.add_model("Model_0")

        CO2 = model_0.add_emission(name="CO2", stage="A3", qty=0.5, unit=KILOGRAM, impacts_from="CO2")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(CO2, Emission, " ")

    def test_11_create_fuel(self):
        """ Test creating a Fuel.
        """
        print('testing creating a fuel.')

        file_path = r'save_files/test.pkl'

        project = Project()
        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        project.set_database(custom_impact_database)

        project.get_database().set_data_entry("Electricity_New", KILO * WATT_HOUR, 
                                                {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        model_0 = project.add_model("Model_0")

        electricity_2 = model_0.add_energy(name="Electricity for Chemical Reaction", stage="A3",
                                           qty=10.0, unit=KILO * WATT_HOUR, impacts_from="Electricity_New")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(electricity_2, Fuel, " ")

    def test_12_create_waste(self):
        """ Test creating a Waste.
        """
        print('testing creating a waste.')

        file_path = r'save_files/test.pkl'

        project = Project()
        custom_impact_database = ImpactsDatabase.new("My database")
        custom_impact_database.set_data(r'data/impact_data_smoothie.csv')
        project.set_database(custom_impact_database)

        model_0 = project.add_model("Model_0")

        waste = model_0.add_waste(name="Waste to landfill", stage="A3", qty=1.0, unit=KILOGRAM, impacts_from="Waste to landfill")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(waste, Waste, " ")

    def test_13a_units_and_conversions(self):
        """ Test units and there conversions.
        """
        print('testing prefix mutliplication and conversion.')

        from utilities.units.common_units import GRAM
        from utilities.units.metric_prefixes import KILO, MEGA, DEKA

        new_prefix_mult = KILO * MEGA
        new_prefix_div  = KILO / DEKA

        self.assertEqual(new_prefix_mult.get_power(), 9)
        self.assertEqual(new_prefix_div.get_power(), 2)

        kilogram = KILO * GRAM
        megagram = MEGA * GRAM

        self.assertEqual(kilogram.get_conversion_factor(GRAM), 1000)
        self.assertEqual(kilogram.get_conversion_factor(megagram), 1000)

    def test_13b_units_and_conversions(self):
        """ Test units and there conversions.
        """
        print('testing unit mutliplication and conversion.')

        from utilities.units.common_units import GRAM, METER, TON_KILOMETER, POUND, MILE, TON_MILE, CUBIC_METER, CUBIC_FEET
        from utilities.units.metric_prefixes import KILO, MEGA, DEKA

        kilogram = KILO * GRAM
        pound_mile = POUND * MILE
        wt_density_metric = kilogram / CUBIC_METER
        wt_density_imperial = POUND / CUBIC_FEET

        self.assertAlmostEqual(GRAM.get_conversion_factor(POUND), 0.00220462)
        self.assertAlmostEqual(kilogram.get_conversion_factor(POUND), 2.2046226, places=3)
        self.assertAlmostEqual(TON_KILOMETER.get_conversion_factor(TON_MILE), 0.621371, places=3)
        self.assertAlmostEqual(TON_KILOMETER.get_conversion_factor(pound_mile), 1369.891, places=1)
        self.assertAlmostEqual(wt_density_metric.get_conversion_factor(wt_density_imperial), 0.06242796, places=4)

        
    def test_13c_units_and_conversions(self):
        """ Test units and there conversions.
        """
        print('save and load units.')

        from utilities.units.common_units import GRAM
        from utilities.units.metric_prefixes import KILO
        import pickle

        kilogram = KILO * GRAM

        file_path = r'save_files\unit_test.pkl'
        with open(file_path, "wb") as file:
            pickle.dump(kilogram, file)
        with open(file_path, 'rb') as file:
            unit_loaded = pickle.load(file)

        self.assertEqual(unit_loaded.get_name(), kilogram.get_name())
        self.assertEqual(unit_loaded.get_standard_notation(), kilogram.get_standard_notation())
        self.assertEqual(unit_loaded.get_qty_measured(), kilogram.get_qty_measured())
        self.assertEqual(unit_loaded.get_prefix().get_power(), kilogram.get_prefix().get_power())


if __name__ == '__main__':
    unittest.main()