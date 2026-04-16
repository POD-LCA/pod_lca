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
    """Impacts object keep record of the impacts created by a product or a process.

    Attributes
    ----------
    parent : ~pod_lca.materials_screening.Master
        The product or process object to which this impacts record belong.
    <impact_category> : float
        Impact categories are dynamically set based on the class variable 'record_attr_dict'.
        This is set to the IMPACT_CATEGORIES in the config file.
    """

    record_type = "Impacts"
    record_attr_dict = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]

    def __init__(self):
        super().__init__()

    # ========================
    # Impact Methods
    # ========================
    def get_weighted_impact(self, method="TRACI_EPA"):
        """Get a normalized and weighted value for impacts.

        Note
        ----
        Reference: The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. DOI: http://hdl.handle.net/1773/41885

        Parameters
        ----------
        method : {'TRACI_EPA', 'TRACI_NIST'}
            Weightages to be used: \n
            - 'TRACI_EPA': From Ref [1].
            - 'TRACI_NIST': From Ref [1].
            Default is 'TRACI_EPA'.

        Returns
        -------
        float
            The weighted impact.

        Raises
        ------
        KeyError
            Weighing method not recognied.
        """
        if method == "TRACI_EPA":
            weights = DataImporter.json_to_dict(config["file_paths"]["impacts"]["IMPACT_WEIGHTING_FACTOR_EPA"])
        elif method == "TRACI_NIST":
            weights = DataImporter.json_to_dict(config["file_paths"]["impacts"]["IMPACT_WEIGHTING_FACTOR_NIST"])
        else:
            raise KeyError("Weighing method not recognized")

        normalisation_factors = DataImporter.json_to_dict(config["file_paths"]["impacts"]["IMPACT_NORMALIZATION_FACTORS"])

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
        """Get GWP values adjusted for biogenic and accelerated carbonation effects.

        Returns
        -------
        float
            Adjusted GWP value

        Raises
        ------
        KeyError
            Impact category not recognied.
        """
        key = config["setup"]["impacts"]["CARBONATION_EFFECTS_IMPACT_CATEGORY"]
        parent = self.get_parent()
        
        # Only adjust for products/processes with life cycle stage A1 or A3
        if not hasattr(parent, 'get_life_cycle_stage'):
            return self.get_record(key)
        
        stage = parent.get_life_cycle_stage()
        CO2_stored_qty = 0

        # check key
        if key in self.get_categories():
            if (
                not UNITS_MAP[self.get_categories(units=True)[1][key]].get_qty_measured()
                == KG_CARBON_DIOXIDE.get_qty_measured()
            ):
                raise KeyError(f"Impact category {key} incompatible to account for carbonation effects.")
        else:
            raise KeyError(f"{key} not in impact categories of config.")

        # adjust GWP
        if key in self.record_attr_dict:
            gwp_qty = self.get_record(key)
            unit_carbon_storage_record = self.get_parent().unit_carbon_storage
            product_qty = self.get_parent().get_qty()
            if unit_carbon_storage_record is not None: 
                for record, unit in unit_carbon_storage_record.record_attr_dict.items():
                    input_unit = UNITS_MAP[unit]
                    conversion_factor_1 = input_unit.convert_to(KG_CARBON_DIOXIDE) 
                    
                    conversion_factor_2 = parent.unit.convert_to(parent.inventories_declared_unit) 

                    unit_storage_qty = unit_carbon_storage_record.get_record(record)

                    CO2_stored_qty = unit_storage_qty * product_qty * conversion_factor_1 * conversion_factor_2 

                    if "Mineral" in record:
                        gwp_qty -= CO2_stored_qty

                    if "Biogenic" in record and stage == "A1":
                        gwp_qty -= CO2_stored_qty

            self.update_qty({key: gwp_qty}) # FIXME: Do we want to update this record here

            return gwp_qty

    # FIXME Delete - this method does not affect A3
    def get_adjusted_a3_gwp_for_bioC_neutrality(self, bio_co2):
        """Get A3 GWP values adjusted for stored biogenic CO2 (-1/+1 bioCO2 accounting, A1-A3 scope).

        Returns
        -------
        float
            Adjusted A3 GWP value (all stored biogenic CO2 is counted as a CO2 emission when the product exits the product system in stage A3)
        """    
        self.update_qty({"GWP": bio_co2})

        return bio_co2

if __name__ == "__main__":
    pass
