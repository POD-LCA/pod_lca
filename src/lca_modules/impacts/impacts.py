from lca_modules.impacts.records import Records
from utilities.data_imports.data_importer import Data_Importer
from utilities.settings import config

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Impacts(Records):
    """
    Impacts object keep record of the impacts created by a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this impacts record belong.
    <impact_category> : float
        Impact categories are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the IMPACT_CATEGORIES in the config file.
    """
    record_type = "Impacts"
    record_attr_dict = config['setup']['impacts']['IMPACT_CATEGORIES']

    def __init__(self):
        super().__init__()

    # ========================
    # Impact Methods
    # ========================
    def get_weighted_impact(self, method='TRACI_EPA'):
        """ Get a weighted value for impacts.
            Ref: [1] The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. 
                     DOI: http://hdl.handle.net/1773/41885
        
        Parameters
        ----------
        method : str
            Which weightages to be used:
                'TRACI_EPA' - from Ref [1]
                'TRACI_NIST' - from Ref [1]
            
        Returns
        -------
        float
            The weighted impact.
        """

        if method == 'TRACI_EPA':
            weights = Data_Importer.json_to_dict(config["file_paths"]["IMPACT_WEIGHTING_FACTOR_EPA"])
        elif method == 'TRACI_NIST':
            weights = Data_Importer.json_to_dict(config["file_paths"]["IMPACT_WEIGHTING_FACTOR_NIST"])
        else:
            raise NotImplementedError
        
        for impact_cat in config['setup']['impacts']['IMPACT_CATEGORIES'].keys():
            if impact_cat not in weights:
                raise KeyError(f"Impact category '{impact_cat}' not found in weights.")
            
        # TODO: normalise the impacts begore applying weights
        weighted_impact = 0.0
        for (impact_cat, weight) in weights.items():
            impact = getattr(self, impact_cat, None)
            if impact is not None:
                weighted_impact += impact * weight
            else:
                return None
        
        return weighted_impact

if __name__ == '__main__':
    pass
