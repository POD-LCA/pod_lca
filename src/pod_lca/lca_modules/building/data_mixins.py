
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


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
    

    # TODO: plot option for comparing scenarios

 
    

if __name__ == '__main__':
    pass
