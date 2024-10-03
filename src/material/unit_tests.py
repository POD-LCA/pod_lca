# database load data
# import data
# custom entry
# get impact data

# create product
# change name
# change units
# add impact

# calculator


from material import HOME
from material.projectManager.projectManager import Project
from material.calculator.calculator import Calculator
from material.databaseManager.databaseManager import DatabaseManager
from material.model.model import Model

import unittest

class TestBuilder(unittest.TestCase):

    def test01_create_project(self):
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

    def test02_create_new_model(self):
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

        file_path = HOME + '\Examples\\test.pkl'
        project = Project()

        project.save(file_path)

        load_project = Project.load(file_path)

        self.assertIsInstance(load_project, Project, " ")
        self.assertIsInstance(project.get_database(), DatabaseManager, " ")
        self.assertIsInstance(project.get_calculator(), Calculator, " ")
        self.assertIsInstance(project.get_current_model(), Model, " ")

    def test04_import_database(self):
        """ Test importing data to database.
        """
        print('testing importing data to database.')

    



if __name__ == '__main__':
    unittest.main()