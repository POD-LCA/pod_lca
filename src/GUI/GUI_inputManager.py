from material.projectManager.projectManager import Project
from material.model.product import Product, Fuel, Waste
from material.model.process import Process, transportationProcess

class GUIInputManager():

    @staticmethod
    def create_project(name=None):

        return Project(name)
    
    @staticmethod
    def clear_project(project, model=True, database=True):

        project.clear_project(model, database)

    @staticmethod
    def create_model(project, name):

        project.create_model(name)

    @staticmethod
    def set_current_model(project, name):

        project.set_current_model(name)

    # =================================
    # Products and Processes
    # =================================

    @staticmethod
    def create_product(project, name, unit, qty, stage, lca_data):

        product = project.get_current_model().create_product(name, stage)
        product.set_unit(unit)
        product.update_qty(qty)
        if not (lca_data == 'None'):
            product.set_impact_database_entry(lca_data)

        return product
    
    @staticmethod
    def create_energy(project, name, unit, qty, stage, lca_data):

        energy = project.get_current_model().create_energy(name, stage)
        energy.set_unit(unit)
        energy.update_qty(qty)
        if not (lca_data == 'None'):
            energy.set_impact_database_entry(lca_data)  

        return energy
  
    @staticmethod
    def create_emission(project, name, unit, qty, stage, lca_data):

        emission = project.get_current_model().create_emission(name, stage)
        emission.set_unit(unit)
        emission.update_qty(qty)
        if not (lca_data == 'None'):
            emission.set_impact_database_entry(lca_data)   

        return emission

    @staticmethod
    def create_waste(project, name, unit, qty, stage, lca_data):

        waste = project.get_current_model().create_waste(name, stage)
        waste.set_unit(unit)
        waste.update_qty(qty)
        if not (lca_data == 'None'):
            waste.set_impact_database_entry(lca_data)

        return waste
    
    @staticmethod
    def create_process(project, name, unit, qty, stage, lca_data):

        process =  project.get_current_model().create_process(name, stage)
        process.set_unit(unit)
        process.update_qty(qty)
        if not (lca_data == 'None'):
            process.set_impact_database_entry(lca_data)

        return process
    
    @staticmethod
    def update_qty(visualizer, item, qty):

        item.update_qty(qty)

        if isinstance(item, Product):
            if item.get_transporter() is not None:
                item.get_transporter().set_travel_weight()

        visualizer.update_dependent_qtys(item, qty)
        visualizer.update_plot()

    @staticmethod
    def update_life_cycle_stage(visualizer, item, stage):

        item.update_life_cycle_stage(stage)
        visualizer.update_plot()

    def edit_name(visulizer, item, name):

        item.set_name(name)

    @staticmethod
    def get_impact_data(project, row):

        return project.get_database().get_impact_data(row)
    
    @staticmethod
    def set_impact_data(visualizer, item, database_row):

        item.set_impact_database_entry(database_row)
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

        model = visualizer.project.get_current_model().delete_obj(obj)
        visualizer.update_plot()

    # =================================
    # Processes: Transportation
    # =================================

    @staticmethod
    def create_transport_process(name, project, unit, qty, stage, lca_data):

        transport_process =  project.get_current_model().create_transportation_process(name, stage)
        transport_process.set_transported_distance_unit(unit)
        transport_process.set_transported_distance(qty)
        if not (lca_data == 'None'):
            transport_process.set_impact_database_entry(lca_data)

        return transport_process

    @staticmethod
    def update_transport_dist(visualizer, item, qty):

        item.set_transported_distance(qty)
        visualizer.update_plot()  

    @staticmethod
    def set_transported_product(visualizer, item, product):

        product.set_transporter(item)

    @staticmethod
    def remove_transported_product(visualizer, item, product):

        item.remove_transported_product(product)
        visualizer.update_plot()  


    @staticmethod
    def set_travel_weight(visualizer, item):  

        item.set_travel_weight()
        visualizer.update_plot()

    @staticmethod
    def get_travel_distance(item):

        return item.get_transported_distance()

    @staticmethod
    def set_travel_unit(obj, new_unit):

        obj.set_transported_distance_unit(new_unit)

    @staticmethod
    def get_travel_unit(obj):

        return obj.get_transported_distance_unit()
    
    @staticmethod
    def set_density(visualizer, obj, density, weight_unit):

        obj.set_density(density)
        obj.set_weight_unit(weight_unit)

        visualizer.update_plot()

    @staticmethod
    def get_density(item):

        return item.get_density()

    @staticmethod
    def get_weight_unit(item):

        return item.get_weight_unit()

    # =================================
    # Database
    # =================================

    @staticmethod
    def import_data_from_CSV(file_path, project, headers=None, multipliers=None):

        project.get_database().import_data_from_CSV(file_path, headers, multipliers)

    @staticmethod
    def get_database_data(project):

        return project.get_database().get_data()
    
    @staticmethod
    def set_impact_categories(project, impact_cats):

        project.get_database().set_impact_categories(impact_cats)

    @staticmethod
    def get_all_units_list(project):
        
        return project.get_calculator().get_units_list()
    
    def set_custom_entry(project, flow, unit, impacts):

        project.get_database().set_custom_entry(flow, unit, impacts)
    