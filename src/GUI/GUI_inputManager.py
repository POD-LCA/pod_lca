from material.projectManager.inputManager import InputManager
from material.databaseManager.databaseManager import DatabaseManager

import pandas

class GUIInputManager(InputManager, DatabaseManager):

    @staticmethod
    def create_process(model, name, project, unit, qty, stage):

        process =  model.create_process(name, stage)
        process.set_unit(unit)
        process.update_qty(qty)

        return process


    @staticmethod
    def create_product(model, name, project, unit, qty, stage):

        product = model.create_product(name, stage)
        product.set_unit(unit)
        product.update_qty(qty)

        return product
    
    @staticmethod
    def update_qty(visualizer, item, qty):

        item.update_qty(qty)
        visualizer.set_plot_data()
        visualizer.update_plot()

    @staticmethod
    def get_impact_data(project, row):

        return project.get_database().get_impact_data(row)
    
    @staticmethod
    def set_impact_data(visualizer, item, database_row):

        item.set_database_row(database_row)
        visualizer.set_plot_data()
        visualizer.update_plot()

    @staticmethod
    def update_life_cycle_stage(visualizer, item, stage):

        item.update_life_cycle_stage(stage)
        visualizer.set_plot_data()
        visualizer.update_plot()
    
    @staticmethod
    def import_data_from_JSON(file_path, project):

        impacts = pandas.read_csv(filepath_or_buffer=file_path)

        project.get_database().set_data(impacts)

    @staticmethod
    def get_database_data(project):

        return project.get_database().get_data()
    
    @staticmethod
    def get_database_row(item):

        return item.get_database_row()
