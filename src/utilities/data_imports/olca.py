
import olca_ipc as ipc
import olca_schema as schema
import olca_ipc.utree as utree

from tqdm import tqdm
import csv


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
        """Connect to the openLCA server."""
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
            process : schema.Process
                The process object.

            Returns
            -------
            schema.ProductSystem
                The product system object.
        """

        config = schema.LinkingConfig(prefer_unit_processes=True, provider_linking=schema.ProviderLinking.PREFER_DEFAULTS)
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
                List of processes from the openLCA server
        """

        process_list = client.get_descriptors(schema.Process)

        return process_list

    def get_product_amount(client, product_system_ref):
        """ Get the target amount and unit for the product system.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            product_system_ref : schema.ProductSystem
                The product system object.

            Returns
            -------
            tuple
                The target amount and unit for the product system.
        """

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
            result : schema.CalculationResult
                The result of the calculation.
            impact_dict : dict
                Dictionary of impact categories.

            Returns
            -------
            dict
                Dictionary of impact results.
        """

        results_dict = {}
        for impact in impact_dict:
            uid = impact_dict[impact]['@id']
            unit = impact_dict[impact]['refUnit']
            impact_category_ref = client.get_descriptor(schema.ImpactCategory, uid)

            impact_qty = result.get_total_impact_value_of(impact_category_ref).amount

            results_dict[impact + ' [' + unit + ']'] = impact_qty

        return results_dict
    
    def get_electricity_in_process(node, level, elec_impact, elec_required_sum, max_levels=3):
        """ This function recursively expands an upstream tree.
            The maximum number of levels and maximum number of child nodes are defined with the constants above.
        
            Parameters
            ----------
            node : utree.Node
                The node object.
            level : int
                The level of the node in the tree.
            elec_impact : float
                The electricity impact.
            elec_required_sum : float
                The electricity required sum.
            max_levels : int
                The maximum number of levels to expand the tree.

            Returns
            -------
            float
                The electricity impact.
            float   
                The electricity required sum.
        """

        if "electricity" in node.provider.name.lower():
            elec_required_sum += node.required_amount
            elec_impact += node.result

            return elec_impact, elec_required_sum

        elif level < max_levels:
            for childs in node.childs:
                elec_impact, elec_required_sum = openLCA.get_electricity_in_process(childs, level + 1, elec_impact, elec_required_sum, max_levels)
            return elec_impact, elec_required_sum
    
        else:
            return elec_impact, elec_required_sum

    # =================================
    # Utilities
    # =================================
    def write_results_to_csv(results, file_path):
        """Write the results to a CSV file."""

        fieldnames = list(next(iter(results.values())).keys())

        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in results.values():
                writer.writerow(data)

    def csv_to_dict(file_path):
        """Convert a CSV file to a dictionary."""

        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row["UUID"]
                data[id] = {key: value for key, value in row.items()} 

        return data 

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

    def compute_impacts(client, product_system_ref, impact_method):
        """ Compute the impacts of the product system.
        
            Notes
            -----
            1. Allocation method set to 'As Defined in Processes' by default (same as openLCA GUI default). For other allocation method names see https://greendelta.github.io/olca-schema/enums/AllocationType.html.
            2. The calculation of the impact method does not occur asynchronously, therefore the wait_until_ready() method called after the results object is created.
        
            Parameters
            ----------
            client : olca_ipc.Client
                The client object for the openLCA server.
            product_system_ref : schema.ProductSystem
                The product system object.
            impact_method : schema.ImpactMethod
                The impact method object.

            Returns
            -------
            schema.CalculationResult
                The result of the calculation.
        """
        setup = schema.CalculationSetup(allocation=schema.AllocationType.USE_DEFAULT_ALLOCATION, target=product_system_ref, impact_method=impact_method)

        result = client.calculate(setup)
        result.wait_until_ready()

        return result
    
    def generate_impacts_dir(impact_dict):

        openLCA = openLCA.set_connection()

        process_list = openLCA.get_process_list(openLCA)

        impact_category_references = openLCA.set_impact_categoreis(openLCA, list(impact_dict.values()))
        impact_method = openLCA.set_impact_method(openLCA, impact_category_references)

        results = {}
        for process in tqdm(process_list):
            process_results = {'name': process.name, 'UUID': process.id}

            product_system_ref = openLCA.create_product_system(openLCA, process)
            process_results['product_amount'], process_results['unit'] = openLCA.get_product_amount(openLCA, product_system_ref)
            result = openLCA.compute_impacts(openLCA, product_system_ref, impact_method)
            impact_results = openLCA.get_impacts(openLCA, result, impact_dict)

            results[process.name] = process_results | impact_results
            
            result.dispose()

            openLCA.delete(product_system_ref)

        return results


if __name__ == '__main__':

    IMPACT_DICT = {'GWP (AR5)': {"@type":"ImpactCategory","@id":"866db1c8-b06b-304e-8664-65621476beea","name":"Greenhouse Gases","category":"ISO21930-LCIA-US","refUnit":"kg CO2 eq"},
                    'AP': {"@type":"ImpactCategory","@id":"420c955a-6f4f-39ae-ac4e-2276e141ef13","name":"Acidification potential","category":"ISO21930-LCIA-US","refUnit":"kg SO2 eq"},
                    'EP': {"@type":"ImpactCategory","@id":"d78c428f-907b-3d9d-967e-e87db83e987b","name":"Eutrophication potential","category":"ISO21930-LCIA-US","refUnit":"kg N eq"},
                    'ODP': {"@type":"ImpactCategory","@id":"39a1d262-bb86-3742-80b7-26c8e9a521ee","name":"Ozone depletion potential","category":"ISO21930-LCIA-US","refUnit":"kg CFC-11 eq"},
                    'POCP': {"@type":"ImpactCategory","@id":"a5cae9e0-23bc-3366-b8c8-a46aa6401ed2","name":"Photochemical oxidant creation potential","category":"ISO21930-LCIA-US","refUnit":"kg O3 eq"}, 
                    'CO2': {"@type":"ImpactCategory","@id":"32d7510b-8896-4fd5-926e-78923712b30d","name":"CO2","refUnit":"kg"}, 
                    'N2O': {"@type":"ImpactCategory","@id":"e7f1d432-5a78-4075-9fe4-610a45d80ad9","name":"N2O","refUnit":"kg"}, 
                    'CH4': {"@type":"ImpactCategory","@id":"a6182013-159b-4f60-bc96-09aa34c61a8f","name":"CH4","refUnit":"kg"} 
                    }
    
    # save_path = './data/US Elec Baseline_AR5_1_3_24.csv'
    # results = generate_impacts_dir(IMPACT_DICT)
    # write_results_to_csv(results, save_path) 

    # dict_A = csv_to_dict('./data/US Elec Baseline_AR5_1_3_24KIUN.csv')
    # dict_B = csv_to_dict('./data/USLCI_AR5_1_24_25.csv')
    # print(compare_dicts(dict_A, dict_B))

    dict_A = openLCA.csv_to_dict('./data/USLCI_tax_elec_1L_ISO21930_1_24_25.csv')

    openLCA_client = openLCA.set_connection()

    process_list = openLCA.get_process_list(openLCA_client)

    # impact_category_references = openLCA.set_impact_categoreis(openLCA_client, list(IMPACT_DICT.values()))
    # impact_method = openLCA.set_impact_method(openLCA_client, impact_category_references)
    impact_method = openLCA.get_impact_method(openLCA_client)

    results = {}
    for process in tqdm(process_list[1040:1042]):
        elec_results = {}

        process_results = {'Name': process.name, 'UUID': process.id}

        product_system_ref = openLCA.create_product_system(openLCA_client, process)
        process_results['Amount'], process_results['Unit'] = openLCA.get_product_amount(openLCA_client, product_system_ref)
        result = openLCA.compute_impacts(openLCA_client, product_system_ref, impact_method)

        impact_results = openLCA.get_impacts(openLCA_client, result, IMPACT_DICT)

        for impact_cat in IMPACT_DICT:

            impact_cat_ref = openLCA_client.get_descriptor(schema.ImpactCategory, IMPACT_DICT[impact_cat]['@id'])

            elec_impact = 0
            
            root = utree.of(result, impact_cat_ref)
            elec_impact, elec_required_sum = openLCA.get_electricity_in_process(root, 0, elec_impact=0, elec_required_sum=0, max_levels=1)

            impact_results['Elec ' + impact_cat] = elec_impact

        Elec_required = elec_required_sum
        # TODO: How elec requirement handled is not the most elegant way.

        impact_results['Total Elec [MJ]'] = Elec_required

        results[process.id] = process_results | impact_results

        # for item in results[process.id]:
        #     if item in ['Name', 'UUID', 'Unit']:
        #         if not results[process.id][item] == dict_A[process.id][item]:
        #             print('mismatch', item, results[process.id][item], dict_A[process.id][item])
        #     else:
        #         if not (float(results[process.id][item]) == 0 and float(dict_A[process.id].get(item)) == 0):
        #             if abs(float(results[process.id][item]) - float(dict_A[process.id][item]))/ abs(float(results[process.id][item]) + float(dict_A[process.id][item]))  > 0.005:
        #                 print('mismatch', item, process.name,  results[process.id][item], dict_A[process.id].get(item))

        result.dispose()
        
        openLCA_client.delete(product_system_ref)

    save_path = './data/USLCI_elec.csv'
    openLCA.write_results_to_csv(results, save_path) 

    
    
    # dict_B = openLCA.csv_to_dict('./data/USLCI_elec.csv')
    # print(openLCA.compare_dicts(dict_A, dict_B))