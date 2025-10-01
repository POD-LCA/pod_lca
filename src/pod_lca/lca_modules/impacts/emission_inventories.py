
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Records
from ..uncertainty import DataDistribution
from ...utilities import config

    
class Emissions(Records):
    """ Emissions object keep record of the emissions created by a product or a process.

    Attributes
    ----------
    parent : ~pod_lca.materials_screening.Master
        The product or process object to which this emissions record belong.
    <emission_name> : float
        Emission names are dynamically set based on the class variable 'record_attr_dict'.
        Currently, this is set to the EMISSION_INVENTORIES in the config file.
    temporal_emission_profile : ~pod_lca.uncertainty.DataDistribution
        Function describing the dynamic emission profile.
    methane_bio_oxidation : float
        Percentage of biogenic methane oxidating to CO2.
    """
    record_type = "Emissions"
    record_attr_dict = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

    def __init__(self):
        super().__init__()
        self.temporal_emission_profile = None
        self.methane_bio_oxidation = 0.5

    def __mul__(self, scalar):
        """ Multiplication of a record by a scalar.
        """
        new_record = super().__mul__(scalar)
        if self.get_temporal_emission_profile() is not None:
            new_record.set_temporal_emission_profile(self.get_temporal_emission_profile())

        return new_record
    
    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_parent(cls, parent):
        """ Create an record object from a parent object.
        
        Parameters
        ----------
        parent : ~pod_lca.materials_screening.Master
            The product or process object to which this record belong.
        
        Returns
        -------
        ~pod_lca.impacts.Emissions
            Record created.
        """
        record_obj = super().from_parent(parent)

        return record_obj
    
    @classmethod
    def from_dict(cls, record_dict):
        """ Create an record object from a dictionary.
        
        Parameters
        ----------
        record_dict : dict
            Dictionary of records {**record catergory** (:class:`str`): **record quantity** (:class:`float`)}
        
        Returns
        -------
        ~pod_lca.impacts.Record
            Records created.
        """
        record_obj = super().from_dict(record_dict)

        return record_obj

    # ========================
    # Setters
    # ========================    
    def set_temporal_emission_profile(self, time_profile):
        """ Set the dyanamic emissions function.
        
        Parameters
        ----------
        time_profile : ~pod_lca.uncertainty.DataDistribution
            Function describing the dynamic emission profile.

        Raises
        ------
        TypeError
            Data distribution type not recognized.
        """
        if isinstance(time_profile, DataDistribution):
            self.temporal_emission_profile = time_profile
        else:
            raise TypeError("Data distribution type not recognized.")

        return self

    # ========================
    # Getters
    # ========================    
    def get_temporal_emission_profile(self):
        """ Get the dyanamic emissions function.

        Returns
        -------
        ~pod_lca.uncertainty.DataDistribution
            Function describing the dynamic emission profile.
        """
        return self.temporal_emission_profile
    
    def get_start_year(self):
        """ Set year of the emission.
        
        Returns
        -------
        int
            Year of the emission occuring.
        """
        return self.get_temporal_emission_profile().get_start()
    
    def get_emission_duration(self):
        """ Get the duration of emissions.
        
        Returns
        -------
        float
            Duration of emission, in years.
        """
        return self.get_temporal_emission_profile().get_duration()


if __name__ == '__main__':
    pass
