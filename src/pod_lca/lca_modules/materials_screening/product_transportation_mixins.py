__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import isnan

from ..impacts import UniformEmissionProfile
from ...units import KILOMETER
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class ProductTransportationMixins:

    # ================================
    # Setters
    # ================================
    def set_transportation(
        self,
        travel_dist=None,
        dist_unit=None,
        shipping_org=None,
        transport_scenario=None,
        return_trip_factor=None,
        mode_name=None,
        mode_efficiency=None,
    ):
        """Set transport processes the product is subject to.

        Parameters
        ----------
        travel_dist : float
            Transportation distance for goods
        dist_unit : ~pod_lca.units.Unit Obj
            Unit of measurement of distances.
        transportation_scenario : str
            Transportation scenario considered.
        return_trip_factor : float
            Return trip factor.
        mode_name : str
            Name of the transportation mode..
        mode_efficiency : str
            Efficiency of the transportation mode.
        """
        if self.get_unit() is None:
            return self
        
        if (not self.get_unit().get_qty_measured() == "mass") and (self.get_density() is None):
            self.set_density()

        if travel_dist is None:
            transport_scenario = "Local" if transport_scenario is None else transport_scenario
            mode_efficiency = "Median" if mode_efficiency is None else mode_efficiency
            mode_name = "Truck" if mode_name is None else mode_name

        dist_unit = KILOMETER if dist_unit is None else dist_unit

        transportation_manager = self.get_transportation_manager()
        if transportation_manager.get_impact_database() is not None:
            transportation_manager.add_good(
                self,
                travel_dist=travel_dist,
                shipping_dest=self.get_project().get_location(),
                shipping_org=shipping_org,
                transport_scenario=transport_scenario,
                distance_unit=dist_unit,
                return_trip_factor=None,
                mode_name=mode_name,
                mode_efficiency=mode_efficiency,
            )

        if self.get_production_year() is not None:
            pulse = UniformEmissionProfile.unit_pulse(at=self.get_production_year())
            for leg in self.get_transportation():
                leg.get_emissions().set_temporal_emission_profile(pulse)

        return self

    def set_sctg_code(self, code=None):
        """Set the Standard Classification of Transported Goods (SCTG) code for the material.

        Parameters
        ----------
        code : str
            Standard Classification of Transported Goods (SCTG) code of the material
        """
        if code is None:
            data_material = DataImporter.csv_to_pandas(config["file_paths"]["transportation"]["BT_SCTG_CODE"])
            if self.get_name() in data_material["material"].values:
                sctg = data_material[data_material["material"] == self.get_name()].iloc[0, 1]
                self.sctg_code = str(sctg)
            else:
                log("Material not found in the dataset", "Warn")
        else:
            self.sctg_code = code

        return self

    # ================================
    # Getters
    # ================================
    def get_transportation_manager(self):
        """Get the transportation manager corresponding to the product.

        Returns
        -------
        ~pod_lca.transportation.TransportationManager
            Transportation manager
        """
        return self.get_model().get_transportation_manager()

    def get_transportation(self):
        """Retrieve transport processes the product is subject to, if any.

        Returns
        -------
        list of ~pod_lca.transportation.TransportationLeg
            Transportation legs the product is subject to.
        """
        transportation_manager = self.get_transportation_manager()

        if transportation_manager is None:
            return None
        else:
            return transportation_manager.get_transportation_leg(self)

    def get_sctg_code(self, digits=2):
        """Get the Standard Classification of Transported Goods (SCTG) code for the material.

        Parameters
        ----------
        digits : int
            Significant digits of the Standard Classification of Transported Goods (SCTG) code of the material

        Raises
        ------
        ValueError
            SCTG code length shorter that digits requested.
        """
        if self.sctg_code is not None:
            if digits <= len(str(self.sctg_code)):
                return int(str(self.sctg_code)[:digits])
            else:
                raise ValueError(
                    f"SCTG code length ({len(str(self.sctg_code))}) shorter than digits requested ({digits})."
                )
        else:
            return self.sctg_code

    # ================================
    # Methods
    # ================================
    def clear_transportation(self):
        """Clear transport processes the product is subject to, if any.

        Returns
        -------
        ~pod_lca.materials_screening.product.Product
            The product with cleared transportation legs.
        """
        transportation_manager = self.get_transportation_manager()
        transportation_manager.remove_good(self)

        return self
    
    def get_transportation_impacts(self):
        transportation_manager = self.get_transportation_manager()
        return transportation_manager.get_impacts(self)

    def get_default_sctg_code(self):
        """ Find a default Standard Classification of Transported Goods (SCTG) code for the product.
        
        Returns
        -------
        str
            Standard Classification of Transported Goods (SCTG) code for the material.
        """
        database_entry = self.get_impact_database_entry()

        if database_entry:
            mapping = DataImporter.csv_to_pandas(config['file_paths']['transportation']['NAICS_SCTG_MAP'])

            database = self.get_project().get_impact_database()
            data = database.get_data_entry(database_entry)
            if "NAICS Sub-category" in data:
                naics_sub_cat = data["NAICS Sub-category"]
                mapped = mapping[mapping["NAICS Sub-category"] == naics_sub_cat].iloc[0:1]

                if isnan(mapped["SCTG Category"].iloc[0]):
                    return config['setup']['transportation']['DEFAULT_SCTG_CODE']
                else:
                    return mapped["SCTG Category"].iloc[0][0:2]

            elif "NAICS Category" in data:
                naics_cat = data["NAICS Category"]
                mapped = mapping[mapping["NAICS Category"] == naics_cat].iloc[0:1]

                if isnan(mapped["SCTG Category"].iloc[0]):
                    return config['setup']['transportation']['DEFAULT_SCTG_CODE']
                else:
                    return mapped["SCTG Category"].iloc[0][0:2]
        
        return config['setup']['transportation']['DEFAULT_SCTG_CODE']


if __name__ == "__main__":
    pass
