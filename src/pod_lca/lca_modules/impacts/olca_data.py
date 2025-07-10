
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

import io
import json
import zipfile

from tqdm import tqdm

from ...utilities import log
from ...units import UNITS_MAP

try:
    import olca_ipc as ipc
    import olca_schema as schema

    OLCA_IMPORTED = True
except ImportError:
    OLCA_IMPORTED = False


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

    # def set_impact_categories(client, impact_categories_list):
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
        schema.Ref
            Reference to the product system object.
        """
        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        config = schema.LinkingConfig(prefer_unit_processes=True, provider_linking=schema.ProviderLinking.PREFER_DEFAULTS)
        product_system_ref = client.create_product_system(process, config)

        return product_system_ref
    
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

    def get_process_list(client, uuids=None):
        """ Get the list of processes from the openLCA server.
        
        Parameters
        ----------
        client : olca_ipc.Client
            The client object for the openLCA server.
        uuids : list of str
            List of UUIDs of the processes to be filtered. If None, all processes are returned.
        
        Returns
        -------
        list
            List of processes reference objects from the openLCA server.
        """
        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        if uuids is None:
            process_list = client.get_descriptors(schema.Process)
        else:
            process_list = []
            for uuid in uuids:
                if openLCA.is_UUID(uuid):
                    process_ref = client.get_descriptor(schema.Process, uuid)
                    process_list.append(process_ref)
                else:
                    raise ValueError(f"Invalid UUID: {uuid}")

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
                    conversion_factor = UNITS_MAP[node.product.ref_unit].convert_to(unit)

                qty += node.required_amount * conversion_factor
                impact += node.result

                return impact, qty, unit

        if level < max_levels:
            for child in node.childs:
                impact, qty, unit = openLCA.get_category_in_process(categories, child, level + 1, impact, qty, unit, conversion_map, max_levels)
        
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
        conversion_map: dict
            A mapping for conversion of declared units of a given set of processes (e.g., fuel group unit conversion to energy units)
            {uuid (str): {'name' : name of the process (str), 
                            'declared_qty': declared quantity of the process (str or float),
                            'declared_unit': standard notation of the declared units of the process (str),
                            'conversion_factor': conversion factor (str or float),
                            'converted_unit': standard notation of the unit to which the process quantity is converted (str)}}

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
                    conversion_factor = UNITS_MAP[node.product.ref_unit].convert_to(unit)        
                else:
                    if node.provider.id in conversion_map:
                        conversion_factor_a = UNITS_MAP[node.product.ref_unit].convert_to(UNITS_MAP[conversion_map[node.provider.id]['declared_unit']])
                        conversion_factor_b = float(conversion_map[node.provider.id]['conversion_factor']) / float(conversion_map[node.provider.id]['declared_qty'])
                        conversion_factor_c = UNITS_MAP[conversion_map[node.provider.id]['converted_unit']].convert_to(unit)
                        
                        conversion_factor = conversion_factor_a * conversion_factor_b * conversion_factor_c
                    else:
                        conversion_factor = UNITS_MAP[node.product.ref_unit].convert_to(unit)
      
            qty += node.required_amount * conversion_factor
            impact += node.result

            return impact, qty, unit

        if level < max_levels:
            for child in node.childs:
                impact, qty, unit = openLCA.get_process_in_process(processes, child, level + 1, impact, qty, unit, conversion_map, max_levels)
        
        return impact, qty, unit
    
    # =================================
    # Utilities
    # =================================
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

    def fix_last_internal_ids(client, process_list):
        """ Finds any processes in process_list for which last_internal_id < len(exchanges), and fixes by setting last_internal_id = len(exchanges).
        
        Parameters
        ----------
        client : olca_ipc.Client
            The client object for the openLCA server.
        process_list : list
            List of UUIDs of the processess to be tested
        """
        if OLCA_IMPORTED:
            import olca_ipc.utree as utree
        else:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")
        
        lastid_count = 0
        exchangeid_count = 0
        for process_ref in tqdm(process_list):
            process = client.get(schema.Process, process_ref.id)
            if process.last_internal_id < len(process.exchanges):
                process.last_internal_id = len(process.exchanges)
                lastid_count += 1
               
            if any(exchange.internal_id > process.last_internal_id for exchange in process.exchanges):
                exchangeid_count += 1
                i=1
                for exchange in process.exchanges:
                    exchange.internal_id = i
                    i+=1
            client.put(process) 

        log("Fixed process last_internal_id for:" + str(lastid_count) + "processes", "Info")
        log("Fixed exchange internal_ids for:" + str(exchangeid_count) + "processes", "Info")

        return client

    @staticmethod
    def filter_processes_by(process_list, filter_by):
        """ Filters the process list by the category given by NAICS or ISIC ids.
        
        Parameters
        ----------
        process_list : list of Schema.Process Obj
            List of processes.
        filter_by : str, int, or list of str, int
            NAICS or ISIC ids of Categories to be filter by.

        Returns
        -------
        list of Schema.Process Obj.
            List of processess.
        """
        if not isinstance(filter_by, list):
            filter_by = [filter_by] 

        new_process_lst = []
        if not filter_by is None:
            for filter in filter_by:
                if isinstance(filter, int):
                    filter = str(filter)

                for process in process_list:
                    if filter.isdigit(): # ISIC division / NAICS code
                        test = ('/' + filter + ':' in process.category) or process.category.startswith(filter + ':')
                    else: # ISIC section
                        test = ('/' + filter + ':' in process.category) or process.category.startswith(filter + ':')

                    if test:
                        new_process_lst.append(process)

        return new_process_lst 
    
    # =================================
    # Import Methods
    # =================================    
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
    

        log("database loaded", "Trace")
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
    def compute_impacts(client, product_system_ref, impact_method_ref , qty=1.0):
        """ Compute the impacts of the product system.
        
        Notes
        -----
        1. Allocation method set to 'As Defined in Processes' by default (same as openLCA GUI default). For other allocation method names see https://greendelta.github.io/olca-schema/enums/AllocationType.html.
        2. The calculation of the impact method does not occur asynchronously, therefore the wait_until_ready() method called after the results object is created.
    
        Parameters
        ----------
        client : olca_ipc.Client
            The client object for the openLCA server.
        product_system_ref : schema.Ref
            Reference to the product system object.
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
                                        target=product_system_ref, 
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
        group_by : dict or list of dict
            Dictionary of group categorization: {'name' : category name (str),
                                                    'ids' : [category id (int) or product uuid (str)], 
                                                    'unit': unit to be reported - optional (Unit Obj), 
                                                    'conversion_map': conversion map - optional (dict)}
            Category IDs are from the North American Industry Classification System (NAICS).
            When unit is not given the default unit of the first item in the group is used.
            Conversion map needs the following keys: 'UUID', 'declared_unit', 'declared_qty', 'conversion_factor', 'converted_unit'.
        
        Returns
        -------
        dict
            Dictionary of impact results.
        """
        if OLCA_IMPORTED:
            import olca_ipc.utree as utree
        else:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        # prerocessing
        for impact_cat in impact_dict:
            impact_cat_ref = client.get_descriptor(schema.ImpactCategory, impact_dict[impact_cat]['@id'])
            impact_dict[impact_cat]['@ref'] = impact_cat_ref

        for group in group_by:
            ids = group['ids']
            if not isinstance(ids, list):
                ids = [ids]
            group['is_uuid'] = all([openLCA.is_UUID(item) for item in ids])
            group['is_isic'] = all([openLCA.is_ISIC(item) for item in ids])
            group['is_naics'] = all([openLCA.is_NAICS(item) for item in ids])

        # process 
        impact_method_ref = openLCA.get_impact_method(client, impact_method_uuid=impact_method)
        results = {}
        for process in tqdm(process_list):
            process_object = client.get(schema.Process, process.id)

            if process_object.description is str:
                process_description = process_object.description.encode("utf-8")
            else:
                process_description = process_object.description

            process_results = {'Category': process.category,'Name': process.name, 'UUID': process.id, 'Location': process.location, 'Process Type': process.process_type.name, 'Description': process_description}

            product_system_ref = openLCA.create_product_system(client, process)
            result = openLCA.compute_impacts(client, product_system_ref, impact_method_ref)
            impact_results = openLCA.get_impacts(client, result, impact_dict)

            impact_amounts_list = []
            for impact in impact_dict:
                unit = impact_dict[impact]['refUnit']
                amount = impact_results[impact + ' [' + unit + ']']
                impact_amounts_list.append(amount)
           
            if ((not group_by is None) and (not all(impact_amount==0 for impact_amount in impact_amounts_list))):
                if not isinstance(group_by, list):
                    group_by = [group_by]

                for group in group_by:
                    ids = group['ids']
                    name = group['name']
                    unit = group['unit'] if 'unit' in group else None
                    conversion_map = group['conversion_map'] if 'conversion_map' in group else None

                    if not isinstance(ids, list):
                        ids = [ids]

                    for impact_cat in impact_dict:
                        root = utree.of(result, impact_dict[impact_cat]['@ref'] )
                        if group['is_uuid']:
                            group_impact, ref_qty, ref_unit = openLCA.get_process_in_process(ids, root, 0, impact=0, qty=0, unit=unit, conversion_map=conversion_map, max_levels=1)
                        elif group['is_isic'] or group['is_naics']:
                            group_impact, ref_qty, ref_unit = openLCA.get_category_in_process(ids, root, 0, impact=0, qty=0, unit=unit, conversion_map=conversion_map, max_levels=1)
                        else:
                            raise ValueError("ids should be all NAICS/ISIC ids or all UUIDs.")
                    
                        impact_results[name + '_' + impact_cat] = group_impact

                    impact_results[name + '_qty'] = ref_qty
                    impact_results[name + '_unit'] = 'N/A' if ref_unit is None else ref_unit.get_standard_notation()

            results[process.id] = process_results | impact_results

            result.dispose()

            client.delete(product_system_ref)

        return results


if __name__ == '__main__':
    pass
