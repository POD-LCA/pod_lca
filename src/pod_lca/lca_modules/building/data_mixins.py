
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pandas import DataFrame

from pod_lca.utilities import config


class DataMixins:

    def get_impacts_by_assembly_lcstage(self, impact_cat='GWP'):
        """Get impacts by assembly and life cycle stage.

        Parameters
        ----------
        impact_cat : str, optional
            Impact category to use, by default 'GWP'

        Returns
        -------
        dict
            Dictionary of impacts by assembly and life cycle stage. {**life cycle stage** (:class:`str`) : {**assembly** (:class:`str`): **impact** (:class:`float`)}}
        """
        results = {
            "A1-A3": {},
            "A4": {},
            "A5": {},
            "B4": {},
            "C1-C4": {}
        }
        for assembly in self.get_assemblies():
            results["A1-A3"][assembly.get_name()] = 0.0
            results["A4"][assembly.get_name()] = 0.0
            results["A5"][assembly.get_name()] = 0.0
            results["B4"][assembly.get_name()] = 0.0
            results["C1-C4"][assembly.get_name()] = 0.0
            for material in assembly.get_materials():
                results["A1-A3"][assembly.get_name()] += material.get_product_impacts().get_record(impact_cat)
                results["A4"][assembly.get_name()] += material.get_transportation_impacts().get_record(impact_cat)
                results["A5"][assembly.get_name()] += material.get_construction_impacts().get_record(impact_cat)
                results["B4"][assembly.get_name()] += material.get_replacement_impacts().get_record(impact_cat)
                results["C1-C4"][assembly.get_name()] += material.get_eol_impacts().get_record(impact_cat)
    
        return results
    
    def get_material_impacts_of_assembly_lcstage(self, assembly_name, impact_cat="GWP", lc_stage="A1-A3", as_df=True):
        """ Get material impact of a given assembly.
         
        Parameters
        ----------
        assembly_name : str
            Name of the assembly.
        impact_cat : str
            Impact category to use, by default 'GWP'.
        lc_stage : {"A1-A3", "A4", "A5", "B4", "C1-C4"}
            Life cycle stage.
        as_df : bool
            Return results as a dataframe, if True; otherwise, dictionary.
        """
        for assembly in self.get_assemblies():
            results = {}
            if assembly.get_name() == assembly_name:
                for material in assembly.get_materials():

                    match lc_stage:
                        case "A1-A3":
                            results[material.get_name()] = material.get_product_impacts().get_record(impact_cat)
                        case "A4":
                            results[material.get_name()] = material.get_transportation_impacts().get_record(impact_cat)
                        case "A5":
                            results[material.get_name()] = material.get_construction_impacts().get_record(impact_cat)
                        case "B4":
                            results[material.get_name()] = material.get_replacement_impacts().get_record(impact_cat)
                        case "C1-C4":
                            results[material.get_name()] = material.get_eol_impacts().get_record(impact_cat)
                        case _:
                            raise KeyError(f"life cycle stage not recognized.")

            if as_df:
                impact_unit = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"][impact_cat]
                return DataFrame(results.items(), columns=['Material', f"{impact_cat} ({impact_unit})"])
            else:                  
                return results
    
    def get_material_quantities_of_assembly(self, assembly_name, as_df=True):
        """ Get material quantities of a given assembly.
         
        Parameters
        ----------
        assembly_name : str
            Name of the assembly.
        as_df : bool
            Return results as a dataframe, if True; otherwise, dictionary.
        """
        for assembly in self.get_assemblies():
            results = {}
            if assembly.get_name() == assembly_name:
                for material in assembly.get_materials():
                    results[material.get_name()] = (material.get_qty(), material.get_unit().standard_notation)
                        
            if as_df:
                return DataFrame([
                    {"Material": key, "Amount": val[0], "Unit": val[1]} 
                    for key, val in results.items()
                ])
            else:                  
                return results

    # TODO: plot option for comparing scenarios

 
    

if __name__ == '__main__':
    pass
