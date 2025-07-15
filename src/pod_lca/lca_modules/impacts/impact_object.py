
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import isnan

from . import Records
from ...units import KG_CARBON_DIOXIDE
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter


class Impacts(Records):
    """ Impacts object keep record of the impacts created by a product or a process.

    Attributes
    ----------
    parent : ~pod_lca.materials_screening.Master
        The product or process object to which this impacts record belong.
    <impact_category> : float
        Impact categories are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the IMPACT_CATEGORIES in the config file.
    """
    record_type = "Impacts"
    record_attr_dict = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']

    def __init__(self):
        super().__init__()

    # ========================
    # Impact Methods
    # ========================
    def get_weighted_impact(self, method='TRACI_EPA'):
        """ Get a normalized and weighted value for impacts.
            
        Note
        ----    
        Reference: The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. DOI: http://hdl.handle.net/1773/41885
        
        Parameters
        ----------
        method : {'TRACI_EPA', 'TRACI_NIST'}
            Weightages to be used:
            - **'TRACI_EPA'**: From Ref [1].
            - **'TRACI_NIST'**: From Ref [1].
            Default is 'TRACI_EPA'.
            
        Returns
        -------
        float
            The weighted impact.

        Raises
        ------
        ValueError
            Weightage method not recognized, or incomplete.
        """
        if method == 'TRACI_EPA':
            weights = DataImporter.json_to_dict(config["file_paths"]["IMPACT_WEIGHTING_FACTOR_EPA"])
        elif method == 'TRACI_NIST':
            weights = DataImporter.json_to_dict(config["file_paths"]["IMPACT_WEIGHTING_FACTOR_NIST"])
        else:
            raise NotImplementedError
        
        normalisation_factors = DataImporter.json_to_dict(config["file_paths"]["IMPACT_NORMALIZATION_FACTORS"])
        
        for impact_cat in self.record_attr_dict:
            if impact_cat not in weights:
                raise KeyError(f"Impact category '{impact_cat}' not found in weights.")
            if impact_cat not in normalisation_factors:
                raise KeyError(f"Impact category '{impact_cat}' not found in normalization factors.")
                        
        weighted_impact = 0.0
        for impact_cat in self.record_attr_dict:
            impact = getattr(self, impact_cat, None)
            weight = weights[impact_cat]
            norm_factor = normalisation_factors[impact_cat]
            if impact is not None:
                weighted_impact += (impact / norm_factor) * weight
            else:
                return None
        
        return weighted_impact
    
    def get_adjusted_GWP(self):
        """ Get GWP values adjusted for biogenic and accelerated carbonation effects.

        Returns
        -------
        float
            Adjusted GWP value
        """
        key = config['setup']['impacts']['CARBONATION_EFFECTS_IMPACT_CATEGORY']

        # check key
        if key in self.get_categories():
            if not UNITS_MAP[self.get_categories(units=True)[1][key]].get_qty_measured() == KG_CARBON_DIOXIDE.get_qty_measured():
                raise KeyError(f"Impact category {key} incompatible to account for carbonation effects.")
        else:
            raise KeyError(f"{key} not in impact categories of config.")

        # adjust GWP
        if key in self.record_attr_dict:
            gwp_qty = self.get_record(key)
            carbon_storage_record = self.get_parent().get_carbon_storage()
            if carbon_storage_record is not None:
                for record, unit in carbon_storage_record.record_attr_dict.items():
                    input_unit = UNITS_MAP[unit]
                    conversion_factor = input_unit.get_conversion_factor(KG_CARBON_DIOXIDE)

                    qty = carbon_storage_record.get_record(record)

                    if isinstance(qty, (float, int)):
                        if not isnan(qty):
                            gwp_qty  = gwp_qty - (qty * conversion_factor)

            return gwp_qty

        
if __name__ == '__main__':
    pass
