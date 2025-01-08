from lca_modules.material.projectManager import Project
from lca_modules.material.product import Product, Fuel, Waste
from lca_modules.material.process import Process, transportationProcess
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from lca_modules.uncertainity.data_quality_assessment import DataQualityAnalysis

from utilities.units.common_units import METER, MILE, GRAM, POUND, GRAM, CUBIC_METER, JOULE, WATT_HOUR
from utilities.units.metric_prefixes import KILO, MEGA

from tkinter import messagebox


class GUIInputManager():

    units_map = {'kg': KILO * GRAM, 'lb': POUND, 'g': GRAM, 'm3':CUBIC_METER,
                 'kJ': KILO * JOULE, 'MJ': MEGA * JOULE, 'kWh': KILO * WATT_HOUR, 'MWh': MEGA * WATT_HOUR,
                 'km': KILO * METER, 'mi': MILE, 'kgkm': (KILO * GRAM) * (KILO * METER), 'lbmi': POUND * MILE}

    @staticmethod
    def create_project(name=None):

        return Project(name)
    
    @staticmethod
    def clear_project(project, model=True, database=True):

        project.clear_project(model, database)

    @staticmethod
    def create_model(project, name):

        return project.create_model(name)
    
    @staticmethod
    def set_model(project, model, model_name):
        
        project.models[model_name] = model

    @staticmethod
    def set_current_model(project, name):

        project.set_current_model(name)

    @staticmethod
    def import_model_from_csv(project, file_path, name):

        return project.create_model_from_csv(file_path, name)
    
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
    def create_product(project, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        product = project.get_current_model().create_product(name, stage)
        product.set_unit(unit) 
        product.update_qty(qty)
        try:
            if not (lca_data == 'None'):
                product.set_impact_database_entry(lca_data)
        except ImportError as e:
            project.get_current_model().delete_obj(product)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
            
        return product
    
    @staticmethod
    def create_energy(project, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        energy = project.get_current_model().create_energy(name, stage)
        energy.set_unit(unit)
        energy.update_qty(qty)
        try:
            if not (lca_data == 'None'):
                energy.set_impact_database_entry(lca_data)  
        except ImportError as e:
            project.get_current_model().delete_obj(energy)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return energy
  
    @staticmethod
    def create_emission(project, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        emission = project.get_current_model().create_emission(name, stage)
        emission.set_unit(unit)
        emission.update_qty(qty)
        try:
            if not (lca_data == 'None'):
                emission.set_impact_database_entry(lca_data)   
        except ImportError as e:
            project.get_current_model().delete_obj(emission)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
            
        return emission

    @staticmethod
    def create_waste(project, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        waste = project.get_current_model().create_waste(name, stage)
        waste.set_unit(unit)
        waste.update_qty(qty)
        try:
            if not (lca_data == 'None'):
                waste.set_impact_database_entry(lca_data)
        except ImportError as e:
            project.get_current_model().delete_obj(waste)
            GUIInputManager.show_error_popup("ImportError", str(e))
            return None
        
        return waste
    
    @staticmethod
    def create_process(project, name, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        process =  project.get_current_model().create_process(name, stage)
        process.set_unit(unit)
        process.update_qty(qty)
        try:
            if not (lca_data == 'None'):
                process.set_impact_database_entry(lca_data)
        except ImportError as e:
            project.get_current_model().delete_obj(process)
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
            item.update_qty(qty)
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

        return item.get_database_row()
    
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
            obj.change_units(unit)
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

        item.overide_id(new_id)

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

        model = visualizer.project.get_current_model().delete_obj(obj)
        visualizer.update_plot()

    @staticmethod
    def copy(obj):

        cls = type(obj)

        return cls.copy(obj)

    # =================================
    # Processes: Transportation
    # =================================

    @staticmethod
    def create_transport_process(name, project, unit, qty, stage, lca_data):

        unit = GUIInputManager.units_map[unit]

        transport_process =  project.get_current_model().create_transportation_process(name, stage)
        transport_process.set_transported_distance_unit(unit)
        transport_process.set_transported_distance(qty)
        try:
            if not (lca_data == 'None'):
                transport_process.set_impact_database_entry(lca_data)
        except ImportError as e:
            project.get_current_model().delete_obj(transport_process)
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

        item.set_travel_weight()
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
    def import_data_from_CSV(file_path, project, headers=None, multipliers=None):

        project.get_database().set_data(file_path, headers, multipliers)

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
