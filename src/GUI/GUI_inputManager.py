from material.projectManager.inputManager import InputManager
from material.projectManager.projectManager import Project
from material.model.product import Product, Fuel, Waste
from material.model.process import Process, transportationProcess

class GUIInputManager(InputManager):

    @staticmethod
    def create_project(name=None):

        return Project(name)
    
    @staticmethod
    def clear_project(project, model=True, database=True):

        project.clear_project(model, database)

    # =================================
    # Products and Processes
    # =================================

    @staticmethod
    def create_product(model, name, unit, qty, stage):

        product = model.create_product(name, stage)
        product.set_unit(unit)
        product.update_qty(qty)

        return product
    
    @staticmethod
    def create_energy(model, name, unit, qty, stage):

        energy = model.create_energy(name, stage)
        energy.set_unit(unit)
        energy.update_qty(qty)

        return energy
  
    @staticmethod
    def create_emission(model, name, unit, qty, stage):

        emission = model.create_emission(name, stage)
        emission.set_unit(unit)
        emission.update_qty(qty)

        return emission

    @staticmethod
    def create_waste(model, name, unit, qty, stage):

        waste = model.create_waste(name, stage)
        waste.set_unit(unit)
        waste.update_qty(qty)

        return waste
    
    @staticmethod
    def create_process(model, name, unit, qty, stage):

        process =  model.create_process(name, stage)
        process.set_unit(unit)
        process.update_qty(qty)

        return process
    
    @staticmethod
    def update_qty(visualizer, item, qty):

        item.update_qty(qty)

        if isinstance(item, Product):
            if item.get_transporter() is not None:
                item.get_transporter().set_travel_weight()

        visualizer.update_dependent_qtys(item, qty)

        visualizer.set_plot_data()
        visualizer.update_plot()

    @staticmethod
    def update_life_cycle_stage(visualizer, item, stage):

        item.update_life_cycle_stage(stage)
        visualizer.set_plot_data()
        visualizer.update_plot()

    def edit_name(visulizer, item, name):

        item.set_name(name)

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
    
    @staticmethod
    def set_unit(obj, unit):

        obj.set_unit(unit)

    @staticmethod
    def get_unit(obj):

        return obj.get_unit()
    
    @staticmethod
    def is_product(obj):

        return isinstance(obj, Product)
    
    @staticmethod
    def is_process(obj):

        return isinstance(obj, Process)
    
    @staticmethod
    def is_transport(obj):

        return isinstance(obj, transportationProcess)
    
    @staticmethod
    def is_fuel(obj):

        return isinstance(obj, Fuel)
    
    @staticmethod
    def set_id(item, new_id):

        item.overide_id(new_id)

    @staticmethod
    def unit_conversion(project, old_unit, new_unit):
        
        return project.get_calculator().conversion_factor(from_unit=old_unit, to_unit=new_unit)
    
    # =================================
    # Processes/Products
    # =================================

    @staticmethod
    def get_name(obj):

        return obj.get_name()

    @staticmethod
    def get_unit(obj):

        return obj.get_unit()

    @staticmethod
    def get_stage(obj):

        return obj.get_life_cycle_stage()

    @staticmethod
    def get_qty(obj):

        return obj.get_qty()
    
    @staticmethod
    def get_id(obj):

        return obj.get_id()   
    
    @staticmethod
    def get_impacts(obj):

        return obj.get_impacts()
    
    @staticmethod
    def delete(visualizer, obj):

        model = visualizer.project.get_model().delete_obj(obj)
        visualizer.set_plot_data()
        visualizer.update_plot()

    # =================================
    # Processes: Transportation
    # =================================

    @staticmethod
    def create_transport_process(model, name, project, unit, qty, stage):

        transport_process =  model.create_transportation_process(name, stage)
        transport_process.set_transported_distance_unit(unit)
        transport_process.set_transported_distance(qty)

        return transport_process

    @staticmethod
    def update_transport_dist(visualizer, item, qty):

        item.set_transported_distance(qty)
        visualizer.set_plot_data()
        visualizer.update_plot()  

    @staticmethod
    def set_transported_product(visualizer, item, product):

        product.set_transporter(item)
        item.set_transported_products(product)

    @staticmethod
    def remove_transported_product(visualizer, item, product):

        product.set_transporter(None)
        item.remove_transported_product(product) # TODO: Check if this is done properly and the corresponding materials removed
        visualizer.set_plot_data()
        visualizer.update_plot()  


    @staticmethod
    def set_travel_weight(visualizer, item):  

        item.set_travel_weight()
        visualizer.set_plot_data()
        visualizer.update_plot()

    @staticmethod
    def get_travel_distance(item):

        return item.get_transported_distance()
    
    @staticmethod
    def get_travel_unit(obj):

        return obj.get_transported_distance_unit()
    
    @staticmethod
    def set_density(visualizer, obj, density, weight_unit):

        obj.set_density(density)
        obj.set_weight_unit(weight_unit)

        visualizer.set_plot_data()
        visualizer.update_plot()


    # =================================
    # Database
    # =================================

    @staticmethod
    def import_data_from_CSV(file_path, project, order=None):

        project.get_database().import_data_from_CSV(file_path, order)

    @staticmethod
    def get_database_data(project):

        return project.get_database().get_data()
    
    @staticmethod
    def set_impact_categories(project, impact_cats):

        project.get_database().set_impact_categories(impact_cats)

    @staticmethod
    def get_all_units_list(project):
        
        return project.get_calculator().get_units_list()
    