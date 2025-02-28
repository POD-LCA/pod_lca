
from lca_modules.impacts.units_map import UNITS_MAP

from tqdm import tqdm
import zipfile
import io
import json

try:
    import olca_ipc as ipc
    import olca_schema as schema

    OLCA_IMPORTED = True
except ImportError:
    OLCA_IMPORTED = False


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class openLCA:

    # =================================
    # Server Connection
    # =================================
    def set_connection():
        """ Connect to the openLCA server.
         
            Returns
            -------
            olca_ipc.Client
                The client object for the openLCA server.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        client = ipc.Client(8080)

        return client

    # =================================
    # Setters
    # =================================

    # def set_impact_categoreis(client, impact_categories_list):
    #     """ Set the impact categories for the openLCA server.

    #         Parameters
    #         ----------
    #         client : olca_ipc.Client
    #             The client object for the openLCA server.
    #         impact_categories_list : list
    #             List of impact categories to be set for the openLCA server.

    #         Returns
    #         -------
    #         list
    #             List of impact category references.
    #     """

    #     if not OLCA_IMPORTED:
    #         raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

    #     impact_category_references = []

    #     for impact_category in impact_categories_list:
    #         impact_category_object = schema.ImpactCategory().from_dict(impact_category)
    #         client.put(impact_category_object)  
    #         impact_category_references.append(client.get_descriptor(schema.ImpactCategory, impact_category["@id"]))

    #     return impact_category_references

    # def set_impact_method(client, impact_category_references):
    #     """ Set the impact method for the openLCA server.
        
    #         Parameters
    #         ----------
    #         client : olca_ipc.Client
    #             The client object for the openLCA server.
    #         impact_category_references : list
    #             List of impact category references to be set for the openLCA server.

    #         Returns
    #         -------
    #         schema.ImpactMethod
    #             The impact method object.
    #     """

    #     if not OLCA_IMPORTED:
    #         raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

    #     # TODO: remove hard coding of impact method dict input 
    #     impact_method = schema.ImpactMethod().from_dict({"@type":"ImpactMethod","@id":"68c8e8cd-e64a-49b1-954e-bec0da4e4574","name":"ISO21930-LCIA-US (POD|LCA)","description":"ISO21930-LCIA-US is built from LCIA Formatter v1.1.3 and flows from the Federal Elementary Flow List (FEDEFL) v1.2.2\n\n","version":"01.01.005","lastChange":"2025-01-24T00:10:23.424Z"})
    #     impact_method.impact_categories = impact_category_references
    #     client.put(impact_method)

    #     return impact_method

    def create_product_system(client, process):
        """ Set the product system for the process.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            process : Schema.Process or schema.Ref 
                Process object or reference to the process object.

            Returns
            -------
            schema.ProductSystem
                Product system object.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        config = schema.LinkingConfig(prefer_unit_processes=True, provider_linking=schema.ProviderLinking.PREFER_DEFAULTS, )
        product_system_ref = client.create_product_system(process, config)
        product_system = client.get(schema.ProductSystem, product_system_ref.id)

        return product_system
    
    # =================================
    # Getters
    # =================================
    def get_impact_method(client, impact_method_uuid):
        """ Get the impact method from the openLCA server.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.

            Returns
            -------
            schema.ImpactMethod
                The impact method object.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        impact_method = client.get_descriptor(schema.ImpactMethod, impact_method_uuid)

        return impact_method

    def get_process_list(client):
        """ Get the list of processes from the openLCA server.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            
            Returns
            -------
            list
                List of processes reference objects from the openLCA server.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        process_list = client.get_descriptors(schema.Process)

        return process_list

    def get_impacts(client, result, impact_dict):
        """ Get the impact results of the product system.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            result : olca_ipc.Result
                The result of the calculation.
            impact_dict : dict
                Dictionary of impact categories.

            Returns
            -------
            dict
                Dictionary of impact results.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        results_dict = {'Amount': result.get_demand().amount, 'Unit':result.get_demand().tech_flow.flow.ref_unit}
        for impact in impact_dict:
            uid = impact_dict[impact]['@id']
            unit = impact_dict[impact]['refUnit']
            impact_category_ref = client.get_descriptor(schema.ImpactCategory, uid)

            impact_qty = result.get_total_impact_value_of(impact_category_ref).amount

            results_dict[impact + ' [' + unit + ']'] = impact_qty

        return results_dict
    
    def get_category_in_process(categories, node, level, impact, qty, unit, conversion_map, max_levels=3):
        """ This function recursively expands an upstream tree.
            The maximum number of levels and maximum number of child nodes are defined with the constants above.
        
            Parameters
            ----------
            categories : list or int.
                IDs of categories to be identified. 
                Category IDs from the North American Industry Classification System (NAICS) or International Standard Industrial Classification (ISIC).
            node : utree.Node
                The node object.
            level : int
                The level of the node in the tree.
            impact : float
                The impact from the category.
            qty : float
                The declared quantity of the category.
            unit : Unit Obj.
                The declared unit of the category.
            max_levels : int
                The maximum number of levels to expand the tree.

            Returns
            -------
            float
                The electricity impact.
            float   
                The electricity required sum.
            Unit Obj.
                The declared unit of the category.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")
        
        if isinstance(categories, int):
            categories = [categories]
        
        for category in categories:
            category = str(category)
            if category.isdigit(): # ISIC division / NAICS code
                test = '/' + category + ':' in node.product.category
            else: # ISIC section
                test = node.product.category.startswith(category + ':')

            if test:
                if unit is None:
                    unit = UNITS_MAP[node.product.ref_unit]
                    conversion_factor = 1.0
                elif unit.get_standard_notation() == node.product.ref_unit:
                    conversion_factor = 1.0
                else:
                    conversion_factor = UNITS_MAP[node.product.ref_unit].get_conversion_factor(unit)

                qty += node.required_amount * conversion_factor
                impact += node.result

                return impact, qty, unit

        if level < max_levels:
            for child in node.childs:
                impact, qty, unit = openLCA.get_category_in_process(categories, child, level + 1, impact, qty, unit, max_levels)
        
        return impact, qty, unit

    def get_process_in_process(processes, node, level, impact, qty, unit, conversion_map, max_levels=3):
        """ This function recursively expands an upstream tree.
            The maximum number of levels and maximum number of child nodes are defined with the constants above.
        
            Parameters
            ----------
            processes : list or str.
                UUIDs of processess to be identified.
            node : utree.Node
                The node object.
            level : int
                The level of the node in the tree.
            impact : float
                The impact from the category.
            qty : float
                The declared quantity of the category.
            unit : Unit Obj.
                The declared unit of the category.
            max_levels : int
                The maximum number of levels to expand the tree.

            Returns
            -------
            float
                The electricity impact.
            float   
                The electricity required sum.
            Unit Obj.
                The declared unit of the category.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")
        
        if isinstance(processes, str):
            processes = [processes]
        
        if node.provider.id in processes:
            if unit is None:
                unit = UNITS_MAP[node.product.ref_unit]
                conversion_factor = 1.0
            elif unit.get_standard_notation() == node.product.ref_unit:
                conversion_factor = 1.0
            else:
                if conversion_map is None:
                    conversion_factor = UNITS_MAP[node.product.ref_unit].get_conversion_factor(unit)        
                else:
                    if node.provider.id in conversion_map:
                        conversion_factor_a = UNITS_MAP[node.product.ref_unit].get_conversion_factor(UNITS_MAP[conversion_map[node.provider.id]['declared_unit']])
                        conversion_factor_b = float(conversion_map[node.provider.id]['heating_value']) / float(conversion_map[node.provider.id]['declared_qty'])
                        conversion_factor_c = UNITS_MAP[conversion_map[node.provider.id]['heating_unit']].get_conversion_factor(unit)
                        
                        conversion_factor = conversion_factor_a * conversion_factor_b * conversion_factor_c
                    else:
                        conversion_factor = UNITS_MAP[node.product.ref_unit].get_conversion_factor(unit)
                    

            qty += node.required_amount * conversion_factor
            impact += node.result

            impact += node.result

            return impact, qty, unit

        if level < max_levels:
            for child in node.childs:
                impact, qty, unit = openLCA.get_process_in_process(processes, child, level + 1, impact, qty, unit, conversion_map, max_levels)
        
        return impact, qty, unit
    
    # =================================
    # Utilities
    # =================================
    def compare_dicts(d1, d2):
        """ Compare two dictionaries.
        
            Parameters
            ----------
            d1 : dict
                The first dictionary to be compared.
            d2 : dict
                The second dictionary to be compared.
            
            Returns
            -------
            bool
                True if the dictionaries are equal, False otherwise.
        """
        if d1.keys() != d2.keys():
            return False

        for key in d1:
            if key not in d2:
                return False 

            if d1[key].keys() != d2[key].keys():
                return False

            for sub_key in d1[key]:
                if sub_key in ['Name', 'UUID', 'Unit']:
                    if d1[key][sub_key] != d2[key].get(sub_key):
                        return False 
                else:
                    if not (float(d1[key][sub_key]) == 0 and float(d2[key].get(sub_key)) == 0):
                        if abs(float(d1[key][sub_key]) - float(d2[key].get(sub_key)))/ abs(float(d1[key][sub_key]) + float(d2[key].get(sub_key)))  > 0.005:
                            return False

        return True 

    @staticmethod
    def is_UUID(uuid):
        """ Check if the input is a valid UUID.

            Parameters
            ----------
            uuid : str or int
                The input to be checked.
            
            Returns
            -------
            bool
                True if the input is a valid UUID, False otherwise.
        """
        try:
            uuid = uuid.replace('-', '')
            val = int(uuid, 16)
        except AttributeError:
            return False
        except ValueError:
            return False

        return len(uuid) == 32

    @staticmethod
    def is_NAICS(naics):
        """ Check if the input is a valid North American Industry Classification System (NAICS) code.

            Parameters
            ----------
            naics : int
                The input integer to be checked.
            
            Returns
            -------
            bool
                True if the input is a valid NAICS code, False otherwise.
        """
        return len(str(naics)) >= 2 and len(str(naics)) <= 6

    @staticmethod
    def is_ISIC(isic):
        """ Check if the input is a valid International Standard Industrial Classification (ISIC) code.

            Parameters
            ----------
            isic : int
                The input integer to be checked.
            
            Returns
            -------
            bool
                True if the input is a valid ISIC code, False otherwise.
        """ 
        if isinstance(isic, int):
            return len(str(isic)) >= 2 and len(str(isic)) <= 4

        if isinstance(isic, str):
            if isic.isdigit():
                return len(isic) >= 2 and len(isic) <= 4
            else: # ISIC section
                return len(isic) == 1

    @staticmethod     
    def import_from_zip(client, path, duplicates='overwrite'):
        """ Import a database from a zip file. Handle only the first level of nested zip files.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            path : str
                The path to the zip file.
            duplicates : str
                The action to take if a duplicate item is found. Options are 'overwrite', 'update', 'never'.
        """
        
        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        with zipfile.ZipFile(path, 'r') as zipObject:
            files = zipObject.namelist()
            for file in files:
                client = openLCA._handle_file(file, zipObject, client, duplicates)
                # if file.endswith('.zip'): # handle nested zip files
                #     with zipObject.open(file) as inner_zip_file:
                #         with zipfile.ZipFile(io.BytesIO(inner_zip_file.read())) as inner_zip:
                #             inner_files = inner_zip.namelist()
                #             for inner_file in inner_files:
                #                 if not inner_file.endswith('/'):  # Ignore directories
                #                     with inner_zip.open(inner_file) as data:
                #                         openLCA.import_from_json(client, inner_file, data, duplicates)

                # elif not file.endswith('/'): # Ignore directories
                #     with zipObject.open(file) as data:
                #         openLCA.import_from_json(client, file, data, duplicates)
    

        print("database loaded")
        return client
    
    @staticmethod
    def _handle_file(file, zipObject, client, duplicates):

        if file.endswith('.zip'): # handle nested zip files
            with zipObject.open(file) as inner_zip_file:
                with zipfile.ZipFile(io.BytesIO(inner_zip_file.read())) as inner_zip:
                    inner_files = inner_zip.namelist()
                    for inner_file in inner_files:
                        client = openLCA._handle_file(inner_file, inner_zip, client, duplicates)

        elif not file.endswith('/'): # Ignore directories
            with zipObject.open(file) as data:
                openLCA.import_from_json(client, file, data, duplicates)

        return client
    
    @staticmethod
    def import_from_json(client, file_name, data, duplicates):
        """ Import a database item from a json file.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            file_name : str
                The name of the file.
            data : ZipExtFile
                The data from the file.
            duplicates : str
                The action to take if a duplicate item is found. Options are 'overwrite', 'update', 'never'.
        """

        if file_name.startswith('actors/'):         
            obj = schema.Actor()
            model_type = 'Actor'
        elif file_name.startswith('currencies/'):
            obj = schema.Currency()
            model_type = 'Currency'
        elif file_name.startswith('dq_systems/'):
            obj = schema.DQSystem()
            model_type = 'DQSystem'
        elif file_name.startswith('epds/'):
            obj = schema.Epd()
            model_type = 'Epd'
        elif file_name.startswith('flows/'):
            obj = schema.Flow()
            model_type = 'Flow'
        elif file_name.startswith('flow_properties/'):
            obj = schema.FlowProperty()
            model_type = 'FlowProperty'
        elif file_name.startswith('lcia_categories/'):
            obj = schema.ImpactCategory()
            model_type = 'ImpactCategory'
        elif file_name.startswith('lcia_methods/'):
            obj = schema.ImpactMethod()
            model_type = 'ImpactMethod'
        elif file_name.startswith('locations/'):
            obj = schema.Location()
            model_type = 'Location'
        elif file_name.startswith('parameters/'):
            obj = schema.Parameter()
            model_type = 'Parameter'
        elif file_name.startswith('processes/'):
            obj = schema.Process()
            model_type = 'Process'
        elif file_name.startswith('projects/'):
            obj = schema.Project()
            model_type = 'Project'
        elif file_name.startswith('results/'):
            obj = schema.Result()
            model_type = 'Result'
        elif file_name.startswith('social_indicators/'):
            obj = schema.SocialIndicator()
            model_type = 'SocialIndicator'
        elif file_name.startswith('sources/'):
            obj = schema.Source()
            model_type = 'Source'
        elif file_name.startswith('unit_groups/'):
            obj = schema.UnitGroup()
            model_type = 'UnitGroup'
        else:
            return None
        
        json_dict = json.load(data)

        result, _ = client.rpc_call("data/get", {'@type': model_type, '@id': json_dict['@id']})

        if not result: # new item
            type_object = obj.from_dict(json_dict)
            client.put(type_object)
        else:
            if duplicates == 'overwrite':
                type_object = obj.from_dict(json_dict)
                client.put(type_object)
            elif duplicates == 'update':
                for key, value in json_dict.items():
                    if value is not None and not key in ['@type', '@id']:
                        result[key] = value
                type_object = obj.from_dict(result)
                client.put(type_object)
            elif duplicates == 'never':
                pass
            else:
                raise ValueError("Invalid duplicates option.")
                
        return client

    # =================================
    # Operations
    # =================================
    def compute_impacts(client, product_system, impact_method_ref , qty=1.0):
        """ Compute the impacts of the product system.
        
            Notes
            -----
            1. Allocation method set to 'As Defined in Processes' by default (same as openLCA GUI default). For other allocation method names see https://greendelta.github.io/olca-schema/enums/AllocationType.html.
            2. The calculation of the impact method does not occur asynchronously, therefore the wait_until_ready() method called after the results object is created.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            product_system : schema.ProductSystem
                Product system object.
            impact_method_ref : schema.Ref
                Reference to the impact method object.

            Returns
            -------
            olca_ipc.Result
                The result of the calculation.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        setup = schema.CalculationSetup(allocation=schema.AllocationType.USE_DEFAULT_ALLOCATION, 
                                        target=product_system, 
                                        impact_method=impact_method_ref, 
                                        amount=qty)

        result = client.calculate(setup)
        result.wait_until_ready()

        return result
    
    def generate_impacts_dir(client, process_list, impact_dict, impact_method, group_by=None):
        """ Generate the impacts of the processes in the openLCA server.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            process_list : list
                List of UUIDs of the processess to be tested
            impact_dict : dict
                Dictionary of impact categories.
            impact_method : str
                UUID of the impact method.
            group_by : dict
                Dictionary of group categorization: {category name (str) : [categoty id (int) or product uuid (str)]}
                Category IDs are from the North American Industry Classification System (NAICS).
            
            Returns
            -------
            dict
                Dictionary of impact results.
        """
        if OLCA_IMPORTED:
            import olca_ipc.utree as utree
        else:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        impact_method = openLCA.get_impact_method(client, impact_method_uuid=impact_method)

        results = {}
        for process in tqdm(process_list):
            process_results = {'Name': process.name, 'UUID': process.id}

            product_system = openLCA.create_product_system(client, process)
            result = openLCA.compute_impacts(client, product_system, impact_method)
            impact_results = openLCA.get_impacts(client, result, impact_dict)

            if not group_by is None:
                for group in group_by:
                    ids = group['ids']
                    name = group['name']
                    unit = group['unit'] if 'unit' in group else None
                    conversion_map = group['conversion_map'] if 'conversion_map' in group else None
                    
                    if not isinstance(ids, list):
                        ids = [ids]

                    for impact_cat in impact_dict:
                        impact_cat_ref = client.get_descriptor(schema.ImpactCategory, impact_dict[impact_cat]['@id'])
                        
                        root = utree.of(result, impact_cat_ref)
                        if all(openLCA.is_UUID(item) for item in ids):
                            group_impact, ref_qty, ref_unit = openLCA.get_process_in_process(ids, root, 0, impact=0, qty=0, unit=unit, conversion_map=conversion_map, max_levels=1)
                        elif all([openLCA.is_ISIC(item) or openLCA.is_NAICS(item) for item in ids]):
                            group_impact, ref_qty, ref_unit = openLCA.get_category_in_process(ids, root, 0, impact=0, qty=0, unit=unit, conversion_map=conversion_map, max_levels=1)
                        else:
                            raise ValueError("ids should be all NAICS/ISIC ids or all UUIDs.")
                    
                        impact_results[name + '_' + impact_cat] = group_impact

                    impact_results[name + '_qty'] = ref_qty
                    impact_results[name + '_unit'] = 'N/A' if ref_unit is None else ref_unit.get_standard_notation() 

            results[process.id] = process_results | impact_results

            result.dispose()

            client.delete(product_system)

        return results


if __name__ == '__main__':
    pass
