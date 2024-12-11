

# Master object operations
# change name
# change units
# add impact

# calculator

from lca_modules.material.projectManager import Project
from lca_modules.material.calculator import Calculator
from lca_modules.material.databaseManager import DatabaseManager
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
        database = project.get_database()
        calculator = project.get_calculator()
        current_model = project.get_current_model()

        self.assertIsInstance(project, Project, " ")
        self.assertIsInstance(database, DatabaseManager, " ")
        self.assertIsInstance(calculator, Calculator, " ")
        self.assertIsInstance(current_model, Model, " ")

    def test_02_create_new_model(self):
        """ Test createing a new model in the project.
        """
        print('testing createing a new model in the project')

        project = Project()
        new_model = project.create_model("Model_1")

        no_models = len(project.models)

        self.assertIsInstance(new_model, Model, " ")
        self.assertEqual(no_models, 2)
        
    def test_03_save_load_project(self):
        """ Test save/load project.
        """
        print('testing save/load project')

        file_path = r'save_files/test.pkl'
        project = Project()

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(load_project, Project, " ")
        self.assertIsInstance(project.get_database(), DatabaseManager, " ")
        self.assertIsInstance(project.get_calculator(), Calculator, " ")
        self.assertIsInstance(project.get_current_model(), Model, " ")

    def test_04_import_database(self):
        """ Test importing data to database.
        """
        print('testing importing data to database.')
        
        database_path = r'data/impact_data.csv'

        project = Project()
        project.get_database().import_data_from_CSV(database_path)

        self.assertIsInstance(project.get_database().get_data(), DataFrame, " ")

    def test_05_importing_from_database(self):
        """ Test importing data from database.
        """
        print('testing importing data from database.')

        database_path = r'data/impact_data.csv'

        project = Project()
        project.get_database().import_data_from_CSV(database_path)

        sand_impacts = project.get_database().get_impact_data("Sand")

        self.assertIsInstance(sand_impacts, Series, " ")

    def test_06_create_custom_impact(self):
        """ Test creating a custom impact.
        """
        print('testing creating a custom impact.')

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        project.get_database().set_custom_entry("Electricity_New", KILO * WATT_HOUR, 
                                                {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        Electricity_New_impacts = project.get_database().get_impact_data("Electricity_New")

        self.assertIsInstance(Electricity_New_impacts, Series, " ")

    def test_07_create_product(self):
        """ Test creating a Product.
        """
        print('testing creating a product.')

        file_path = r'save_files/test.pkl'

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        project.get_database().set_custom_entry("Electricity_New", KILO * WATT_HOUR, 
                                                {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        sprinkles = project.current_model.create_product("Sprinkles", "A1")
        sprinkles.update_qty(2.0)
        sprinkles.set_unit(KILOGRAM)
        sprinkles.set_impact_database_entry("Sprinkles")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(sprinkles, Product, " ")

    def test_08_create_process(self):
        """ Test creating a Product.
        """
        print('testing creating a process.')

        file_path = r'save_files/test.pkl'

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

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
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        sprinkles = project.current_model.create_product("Sprinkles", "A1")
        sprinkles.update_qty(2.0)
        sprinkles.set_unit(KILOGRAM)
        sprinkles.set_impact_database_entry("Sprinkles")

        sprinkles_by_truck = project.current_model.create_transportation_process("Sprinkle Transportation", "A2")
        sprinkles_by_truck.set_transported_product(sprinkles)
        sprinkles_by_truck.set_transported_distance(30.0)
        sprinkles_by_truck.set_transported_distance_unit(KILOMETER)
        sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(sprinkles_by_truck, transportationProcess, " ")

    def test_10_create_emission(self):
        """ Test creating a Emission.
        """
        print('testing creating an emission.')

        file_path = r'save_files/test.pkl'

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        CO2 = project.current_model.create_emission("CO2", "A3")
        CO2.update_qty(0.5)
        CO2.set_unit(KILOGRAM)
        CO2.set_impact_database_entry("CO2")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(CO2, Emission, " ")

    def test_11_create_fuel(self):
        """ Test creating a Fuel.
        """
        print('testing creating a fuel.')

        file_path = r'save_files/test.pkl'

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        project.get_database().set_custom_entry("Electricity_New", KILO * WATT_HOUR, 
                                                {"GWP":0.503, "AP":0.0036, "EP":5.83e-05, "ODP":7.6e-11, "SFP":3.37e-2})

        electricity_2 = project.current_model.create_energy("Electricity for Chemical Reaction", "A3")
        electricity_2.update_qty(10.0)
        electricity_2.set_unit(KILO * WATT_HOUR)
        electricity_2.set_impact_database_entry("Electricity_New")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(electricity_2, Fuel, " ")

    def test_12_create_waste(self):
        """ Test creating a Waste.
        """
        print('testing creating a waste.')

        file_path = r'save_files/test.pkl'

        project = Project()
        project.get_database().import_data_from_CSV(r'data/impact_data_new.csv')

        waste = project.current_model.create_waste("Waste to landfill", "A3")
        waste.update_qty(1.0)
        waste.set_unit(KILOGRAM)
        waste.set_impact_database_entry("Waste to landfill")

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(waste, Waste, " ")


if __name__ == '__main__':
    unittest.main()