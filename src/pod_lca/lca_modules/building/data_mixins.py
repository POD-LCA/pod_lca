
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pandas import DataFrame

from pod_lca.utilities import config
from pod_lca.utilities import ArrayMethods


class DataMixins:

    def get_impact_totals(self, assembly_names=None, material_names=None, lc_stages=None, impact_cat='GWP', as_df=True):
        """Get impacts by assembly and life cycle stage.

        Parameters
        ----------
        assembly_names : list of str, optional
            List of assembly names to filter by, by default None.
        material_names : list of str, optional
            List of material names to filter by, by default None.
        lc_stages : list of str, optional
            List of life cycle stages to filter by, by default None.
        impact_cat : str, optional
            Impact category to use, by default 'GWP'.

        Returns
        -------
        dict
            Dictionary of impacts by assembly and life cycle stage. {**life cycle stage** (:class:`str`) : {**assembly** (:class:`str`): **impact** (:class:`float`)}}
        """
        if assembly_names is None:
            assembly_names = set([assembly.get_name() for assembly in self.get_assemblies()])

        if lc_stages is None:
            lc_stages = ["A1-A3", "A4", "A5", "B4", "C1-C4"]
            
        results = {lc_stage: {} for lc_stage in lc_stages}

        for assembly_name in assembly_names:
            for lc_stage in lc_stages:
                results[lc_stage][assembly_name] = 0.0

            assemblies = self.find_assembly(assembly_name)
            if assemblies is None:
                continue

            for assembly in assemblies:
                for material in assembly.get_materials():
                    if  material_names is not None:
                        if material.get_name() not in material_names:
                            continue

                    if "A1-A3" in lc_stages:
                        results["A1-A3"][assembly_name] += material.get_product_impacts().get_record(impact_cat)
                    if "A4" in lc_stages:
                        results["A4"][assembly_name] += material.get_transportation_impacts().get_record(impact_cat)
                    if "A5" in lc_stages:
                        results["A5"][assembly_name] += material.get_construction_impacts().get_record(impact_cat)
                    if "B4" in lc_stages:
                        results["B4"][assembly_name] += material.get_replacement_impacts().get_record(impact_cat)
                    if "C1-C4" in lc_stages:
                        results["C1-C4"][assembly_name] += material.get_eol_impacts().get_record(impact_cat)


        if as_df:
            impact_unit = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"][impact_cat]
            return DataFrame(results.items(), columns=['Material', f"{impact_cat} ({impact_unit})"])
        else:                  
            return results

    def get_material_quantities(self, assembly_names=None, as_df=True):
        """ Get material quantities of a given assembly.
         
        Parameters
        ----------
        assembly_names : list of str, optional
            List of assembly names to filter by, by default None.
        as_df : bool
            Return results as a dataframe, if True; otherwise, dictionary.
        """
        assemblies_all = self.get_assemblies()
        if assembly_names is None:
            assembly_names = ArrayMethods.get_attribute_as_list(assemblies_all, 'name')    

        if not isinstance(assembly_names, list):
            assembly_names = [assembly_names]

        results = {}
        for assembly in assemblies_all:
            if assembly.get_name() in assembly_names:
                for material in assembly.get_materials():
                    if material.get_name() in results:
                        qty, unit =  results[material.get_name()]
                        results[material.get_name()] = (qty + material.get_qty() * material.get_unit().convert_to(unit), unit)
                    else:
                        results[material.get_name()] = (material.get_qty(), material.get_unit())
                        
        if as_df:
            return DataFrame([
                {"Material": key, "Amount": val[0], "Unit": val[1].standard_notation} 
                for key, val in results.items()
            ])
        else:                  
            return results
 
    

if __name__ == '__main__':
    pass
