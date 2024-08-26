from material.projectManager.inputManager import InputManager
from material.model.product import Product

import pandas

class GUIInputManager(InputManager):

    # =================================
    # Products and Processes
    # =================================

    @staticmethod
    def create_product(model, name, project, unit, qty, stage):

        product = model.create_product(name, stage)
        product.set_unit(unit)
        product.update_qty(qty)

        return product
  
    @staticmethod
    def create_process(model, name, project, unit, qty, stage):

        process =  model.create_process(name, stage)
        process.set_unit(unit)
        process.update_qty(qty)

        return process
    
    @staticmethod
    def update_qty(visualizer, item, qty):

        item.update_qty(qty)

        if item.get_transporter() is not None:
            item.get_transporter().set_travel_weight()

        visualizer.set_plot_data()
        visualizer.update_plot()

    @staticmethod
    def update_life_cycle_stage(visualizer, item, stage):

        item.update_life_cycle_stage(stage)
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
    def get_database_row(item):

        return item.get_database_row()
    
    @staticmethod
    def get_qty(item):

        return item.get_qty()
    
    # =================================
    # Processes: Transportation
    # =================================

    @staticmethod
    def create_transport_process(model, name, project, unit, qty, stage):

        transport_process =  model.create_transportation_process(name, stage)
        transport_process.set_unit(unit)
        transport_process.set_transported_distance(qty)

        return transport_process

    @staticmethod
    def update_transport_dist(visualizer, item, qty):

        item.set_transported_distance(qty)
        visualizer.set_plot_data()
        visualizer.update_plot()  

    @staticmethod
    def set_transported_products(visualizer, item, products):

        item.set_transported_products(products)
        if isinstance(products, list):
            for product in products:
                product.set_transporter(item)
        elif isinstance(products, Product) :
            products.set_transporter(item)
        else:
            raise TypeError
        
        GUIInputManager.set_travel_weight(visualizer, item)

    @staticmethod
    def set_travel_weight(visualizer, item):  

        item.set_travel_weight()
        visualizer.set_plot_data()
        visualizer.update_plot()   

    # =================================
    # Database
    # =================================

    @staticmethod
    def import_data_from_JSON(file_path, project):

        project.get_database().import_data_from_JSON(file_path)

    @staticmethod
    def get_database_data(project):

        return project.get_database().get_data()
    