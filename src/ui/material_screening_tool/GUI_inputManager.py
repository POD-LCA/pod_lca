from lca_modules.material.project_manager import Project
from lca_modules.material.product import Product, Fuel, Waste
from lca_modules.material.process import Process, transportationProcess
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from lca_modules.uncertainty.data_quality_assessment import DataQualityAnalysis

from utilities.units.common_units import METER, MILE, GRAM, POUND, GRAM, CUBIC_METER, JOULE, WATT_HOUR
from utilities.units.metric_prefixes import KILO, MEGA

from tkinter import messagebox


class GUIInputManager():

    units_map = {'kg': KILO * GRAM, 'lb': POUND, 'g': GRAM, 'm3':CUBIC_METER,
                 'kJ': KILO * JOULE, 'MJ': MEGA * JOULE, 'kWh': KILO * WATT_HOUR, 'MWh': MEGA * WATT_HOUR,
                 'km': KILO * METER, 'mi': MILE, 'kgkm': (KILO * GRAM) * (KILO * METER), 'lbmi': POUND * MILE}

    @staticmethod
    def create_project(name=None):

        return Project.new(name)
    
    @staticmethod
    def clear_project(project, model=True, database=True):

        project.clear_project(model, database)

    @staticmethod
    def create_model(project, name):

        return project.add_model(name)
    
    @staticmethod
    def set_model(project, model, model_name):
        
        project.models[model_name] = model

    @staticmethod
    def import_model_from_csv(project, file_path, name):

        return project.add_model(name, file_path)
    
    @staticmethod
    def get_model(project, model_id):

        return project.get_model(model_id)

    @staticmethod
    def get_all_model_names(project):

        return project.models.keys() 

    @staticmethod
    def get_all_products(visualizer, model):

        return visualizer.project.models[model].products          

    @staticmethod
    def get_all_processes(visualizer, model):

        return visualizer.project.models[model].processes  
    # =================================
    # Products and Processes
    # =================================

    @staticmethod
    def create_product(project, model_name, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)

        try:
            lca_data = None if lca_data == 'None' else lca_data
            product = model.add_product(name, stage, qty, unit, lca_data)
        except ImportError as e:
            model.delete_item(product)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
            
        return product
    
    @staticmethod
    def create_energy(project, model_name, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)

        try:
            lca_data = None if lca_data == 'None' else lca_data
            energy = model.add_energy(name, stage, qty, unit, lca_data)
        except ImportError as e:
            model.delete_item(energy)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return energy
  
    @staticmethod
    def create_emission(project, model_name, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)

        
        try:
            lca_data = None if lca_data == 'None' else lca_data
            emission = model.add_emission(name, stage, qty, unit, lca_data)  
        except ImportError as e:
            model.delete_item(emission)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
            
        return emission

    @staticmethod
    def create_waste(project, model_name, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)
        
        try:
            lca_data = None if lca_data == 'None' else lca_data
            waste = model.add_waste(name, stage, qty, unit, lca_data)
        except ImportError as e:
            model.delete_item(waste)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return waste
    
    @staticmethod
    def create_process(project, model_name, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)

        try:
            lca_data = None if lca_data == 'None' else lca_data
            process =  model.add_process(name, stage, qty, unit, lca_data)
        except ImportError as e:
            model.delete_item(process)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return process
    
    @staticmethod
    def add_product(project, model, obj):
        
        project.models[model].products.append(obj)

        LC_stage = obj.get_life_cycle_stage()
        project.models[model].impacts[LC_stage].append(obj.get_impacts())

        return obj

    @staticmethod
    def add_process(project, model, obj):
        
        project.models[model].processes.append(obj)

        LC_stage = obj.get_life_cycle_stage()
        project.models[model].impacts[LC_stage].append(obj.get_impacts())

        return obj
    
    @staticmethod
    def update_qty(visualizer, item, qty, close_error=True):

        try: 
            item.set_qty(qty)
        except ImportError as e:
            GUIInputManager.show_error_popup("ImportError", str(e))
            if not close_error:
                raise
            return None
        except TypeError as e:
            GUIInputManager.show_error_popup("TypeError", str(e))
            if not close_error:
                raise
            return None
        
        if isinstance(item, Product):
            if item.get_transporter() is not None:
                item.get_transporter().set_travel_weight()

        visualizer.update_dependent_qtys(item, qty)
        visualizer.update_plot()
        if visualizer.hotspot_on_off.get():
            visualizer.show_hotspots()

        return item

    @staticmethod
    def update_life_cycle_stage(visualizer, item, stage):

        item.update_life_cycle_stage(stage)
        visualizer.update_plot()

        return item

    @staticmethod
    def edit_name(visulizer, item, name):

        item.set_name(name)

        return item

    @staticmethod
    def get_impact_data(project, row):

        return project.get_database().get_impact_data(row)
    
    @staticmethod
    def set_impact_data(visualizer, item, database_row, close_error=True):

        try: 
            if not (database_row == 'None'):
                item.set_impact_database_entry(database_row)
                visualizer.update_plot()
        except ImportError as e:
            GUIInputManager.show_error_popup("ImportError", str(e))
            if not close_error:
                raise e
            return None
            
        return item

    @staticmethod
    def get_database_row(item):

        return item.get_impact_database_entry()
    
    @staticmethod
    def get_qty(item):

        return item.get_qty()
    
    @staticmethod
    def get_transporter(item):
        
        if isinstance(item, Product):
            return item.get_transporter()
    
    @staticmethod
    def set_unit(obj, unit):

        unit = GUIInputManager.units_map[unit]

        obj.set_unit(unit)

    @staticmethod
    def change_unit(visualizer, obj, unit, close_error=True):

        unit = GUIInputManager.units_map[unit]

        try:
            obj.set_unit(unit)
        except ValueError as e:
            GUIInputManager.show_error_popup("TypeError", str(e))
            if not close_error:
                raise
            return None
        
        return obj

    @staticmethod
    def get_unit(obj):

        return obj.get_unit().get_standard_notation()
    
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

        item.set_id(new_id)

    @staticmethod
    def unit_conversion(project, old_unit, new_unit, close_error=True):

        old_unit = GUIInputManager.units_map[old_unit]
        new_unit = GUIInputManager.units_map[new_unit]
        
        factor = old_unit.get_conversion_factor(new_unit)
        if factor is None:
            e = f"Units {old_unit} and {new_unit} are incompatible." 
            GUIInputManager.show_error_popup("TypeError", str(e))
            if not close_error:
                raise TypeError(e)
            return None
    
        return factor
    # =================================
    # Processes/Products
    # =================================

    @staticmethod
    def get_name(obj):

        return obj.get_name()

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
    def get_impact_val(obj, impact_cat):

        return obj.get_impacts().get_impact(impact_cat)
    
    @staticmethod
    def get_weighted_impact(obj):

        return obj.get_impacts().get_weighted_impact()
    
    @staticmethod
    def delete(visualizer, obj):

        model = visualizer.project.get_model(visualizer.get_current_model())

        model.delete_item(obj)
        visualizer.update_plot()

    @staticmethod
    def copy(obj):

        cls = type(obj)

        return cls.copy(obj)

    # =================================
    # Processes: Transportation
    # =================================

    @staticmethod
    def create_transport_process(name, model_name, project, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        model = project.get_model(model_name)

        try:
            lca_data = None if lca_data == 'None' else lca_data
            transport_process =  model.add_transportation_process(name, stage, qty, unit, lca_data)
        except ImportError as e:
            model.delete_item(transport_process)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return transport_process

    @staticmethod
    def update_transport_dist(visualizer, item, qty, close_error=True):

        try:
            item.set_transported_distance(qty)                
        except TypeError as e:
            GUIInputManager.show_error_popup("TypeError", str(e))
            if not close_error:
                raise
            return None

        visualizer.update_plot()  
        if visualizer.hotspot_on_off.get():
            visualizer.show_hotspots()
        return item

    @staticmethod
    def set_transported_product(visualizer, transporter, product):

        product.set_transporter(transporter)

    @staticmethod
    def remove_transported_product(visualizer, item, product):

        item.remove_transported_product(product)
        visualizer.update_plot()  


    @staticmethod
    def set_travel_weight(visualizer, item):  

        item.set_transported_weight()
        visualizer.update_plot()

    @staticmethod
    def get_travel_distance(item):

        return item.get_transported_distance()

    @staticmethod
    def set_travel_unit(obj, new_unit):

        new_unit = GUIInputManager.units_map[new_unit]

        obj.set_transported_distance_unit(new_unit)

    @staticmethod
    def get_travel_unit(obj):

        return obj.get_transported_distance_unit().get_standard_notation()
    
    @staticmethod
    def set_density(visualizer, obj, density, weight_unit):

        weight_unit = GUIInputManager.units_map[weight_unit]

        obj.set_density(density)
        obj.set_weight_unit(weight_unit)

        visualizer.update_plot()

        return obj

    @staticmethod
    def get_density(item):

        return item.get_density()

    @staticmethod
    def get_weight_unit(item):

        return item.get_weight_unit().get_standard_notation()
    
    # =================================
    # Database
    # =================================

    @staticmethod
    def set_database(file_path, project, headers=None, multipliers=None):

        project_impact_database = ImpactsDatabase.new("Project database")
        project_impact_database.set_data(file_path, headers, multipliers)

        project.set_database(project_impact_database)

    @staticmethod
    def get_database_data(project):

        return project.get_database().get_data_all()
    
    @staticmethod
    def get_impact_categories():

        return IMPACT_CATEGOREIS

    @staticmethod
    def get_all_units_list(project):
        
        return list(GUIInputManager.units_map.keys())
    
    @staticmethod
    def set_custom_entry(project, flow, unit, impacts):
        
        unit = GUIInputManager.units_map[unit]

        project.get_database().set_custom_entry(flow, unit, impacts)
    
    # =================================
    # Error handling
    # =================================

    @staticmethod
    def show_error_popup(error_type, message):
        messagebox.showerror(error_type, message)

    # =================================
    # Analysis
    # =================================

    @staticmethod
    def create_DQA(project):

        DQA = DataQualityAnalysis(project)
        for model_name in project.get_model_names():
            DQA.setPedigreeScores(model_name)

        return
    
    @staticmethod
    def DQA_inidcators(project):

        return project.DataQualityAnalysis.get_indicators()
    
    @staticmethod
    def get_pedigree_score_objs(project, model_name):

        return project.DataQualityAnalysis.pedigreeScores[model_name]
    
    @staticmethod
    def get_pedigree_score(pedigree_obj, indicator):

        return getattr(pedigree_obj, indicator)

    @staticmethod
    def set_pedigree_score(pedigree_obj, indicator, value):

        setattr(pedigree_obj, indicator, value)
      
    @staticmethod
    def get_DQS(pedigree_obj):

        return pedigree_obj.calculate_DQS()
    
    @staticmethod
    def get_DQS_range(project):

        min = project.DataQualityAnalysis.min_score
        max = project.DataQualityAnalysis.max_score

        return range(min, max + 1, 1)
    
    @staticmethod
    def calculate_model_DQS(project, model_name):

        return project.DataQualityAnalysis.calculate_DQS(model_name, printout=False)
