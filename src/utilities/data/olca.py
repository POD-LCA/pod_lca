
from lca_modules.impacts.units_map import UNITS_MAP

from tqdm import tqdm

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
    def set_impact_categoreis(client, impact_categories_list):
        """ Set the impact categories for the openLCA server.

            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            impact_categories_list : list
                List of impact categories to be set for the openLCA server.

            Returns
            -------
            list
                List of impact category references.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        impact_category_references = []

        for impact_category in impact_categories_list:
            impact_category_object = schema.ImpactCategory().from_dict(impact_category)
            client.put(impact_category_object)  
            impact_category_references.append(client.get_descriptor(schema.ImpactCategory, impact_category["@id"]))

        return impact_category_references

    def set_impact_method(client, impact_category_references):
        """ Set the impact method for the openLCA server.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            impact_category_references : list
                List of impact category references to be set for the openLCA server.

            Returns
            -------
            schema.ImpactMethod
                The impact method object.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        impact_method = schema.ImpactMethod().from_dict({"@type":"ImpactMethod","@id":"68c8e8cd-e64a-49b1-954e-bec0da4e4574","name":"ISO21930-LCIA-US (POD|LCA)","description":"ISO21930-LCIA-US is built from LCIA Formatter v1.1.3 and flows from the Federal Elementary Flow List (FEDEFL) v1.2.2\n\n","version":"01.01.005","lastChange":"2025-01-24T00:10:23.424Z"})
        impact_method.impact_categories = impact_category_references
        client.put(impact_method)

        return impact_method

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

        config = schema.LinkingConfig(prefer_unit_processes=True, provider_linking=schema.ProviderLinking.PREFER_DEFAULTS, )
        product_system_ref = client.create_product_system(process, config)

        return product_system_ref
    
    # =================================
    # Getters
    # =================================
    def get_impact_method(client):
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

        #for FLCAC use impact method uuid: 68c8e8cd-e64a-49b1-954e-bec0da4e4574 ; for ecoinvent use impact method uuid: 1bd6fac2-7dd4-400a-8e56-3c677967c3d8
        impact_method = client.get_descriptor(schema.ImpactMethod, '68c8e8cd-e64a-49b1-954e-bec0da4e4574')

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

    def get_product_amount(client, product_system_ref):
        """ Get the target amount and unit for the product system.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            product_system_ref : schema.Ref
                Reference to the product system object.

            Returns
            -------
            tuple
                The target amount and unit for the product system.
        """

        if not OLCA_IMPORTED:
            raise ImportError("Please install the 'olca-ipc' package to use the openLCA API.")

        product_system = client.get(schema.ProductSystem, product_system_ref.id)
        product_amount = product_system.target_amount
        unit = product_system.target_unit.name

        return product_amount, unit

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

        results_dict = {}
        for impact in impact_dict:
            uid = impact_dict[impact]['@id']
            unit = impact_dict[impact]['refUnit']
            impact_category_ref = client.get_descriptor(schema.ImpactCategory, uid)

            impact_qty = result.get_total_impact_value_of(impact_category_ref).amount

            results_dict[impact + ' [' + unit + ']'] = impact_qty

        return results_dict
    
    def get_category_in_process(categories, node, level, impact, qty, unit, max_levels=3):
        """ This function recursively expands an upstream tree.
            The maximum number of levels and maximum number of child nodes are defined with the constants above.
        
            Parameters
            ----------
            categories : list or int.
                IDs of categories to be identified. Category IDs from the North American Industry Classification System (NAICS)
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
            if '/' + str(category) + ':' in node.product.category:
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

    # =================================
    # Utilities
    # =================================
    def compare_dicts(d1, d2):
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

    # =================================
    # Operations
    # =================================
    def compute_impacts(client, product_system_ref, impact_method_ref):
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

        setup = schema.CalculationSetup(allocation=schema.AllocationType.USE_DEFAULT_ALLOCATION, target=product_system_ref, impact_method=impact_method_ref)

        result = client.calculate(setup)
        result.wait_until_ready()

        return result
    
    def generate_impacts_dir(impact_dict, group_by=None):
        """ Generate the impacts of the processes in the openLCA server.
        
            Parameters
            ----------
            impact_dict : dict
                Dictionary of impact categories.
            group_by : dict
                Dictionary of group categorization: {category name (str) : [category id (int)]}
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

        openLCA_client = openLCA.set_connection()

        process_list = openLCA.get_process_list(openLCA_client)

        # TODO: Update and expand data import methods for openLCA
        # impact_category_references = openLCA.set_impact_categoreis(openLCA_client, list(impact_dict.values()))
        # impact_method = openLCA.set_impact_method(openLCA_client, impact_category_references)
        impact_method = openLCA.get_impact_method(openLCA_client)

        results = {}

        category_filter = '' #ADD CATEGORY NAME IDENTIFIER HERE, OR LEAVE EMPTY TO RUN ALL PROCESSES IN ACTIVE DATABASE
        process_list = [process for process in process_list if category_filter in process.category]

        for process in tqdm(process_list):

            process_results = {'Category': process.category,'Name': process.name, 'UUID': process.id}

            product_system_ref = openLCA.create_product_system(openLCA_client, process)
            process_results['Amount'], process_results['Unit'] = openLCA.get_product_amount(openLCA_client, product_system_ref)
            result = openLCA.compute_impacts(openLCA_client, product_system_ref, impact_method)
            impact_results = openLCA.get_impacts(openLCA_client, result, impact_dict)

            if not group_by is None:
                for name, ids in group_by.items():
                    for impact_cat in impact_dict:
                        impact_cat_ref = openLCA_client.get_descriptor(schema.ImpactCategory, impact_dict[impact_cat]['@id'])
                        
                        root = utree.of(result, impact_cat_ref)
                        group_impact, ref_qty, ref_unit = openLCA.get_category_in_process(ids, root, 0, impact=0, qty=0, unit=None, max_levels=1)

                        impact_results[name + '_' + impact_cat] = group_impact

                    impact_results[name + '_qty'] = ref_qty
                    impact_results[name + '_unit'] = 'N/A' if ref_unit is None else ref_unit.get_standard_notation() 

            results[process.id] = process_results | impact_results

            result.dispose()

            openLCA_client.delete(product_system_ref)

        return results


if __name__ == '__main__':
    pass
