
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import arange
from numpy import concatenate
from numpy import int16
from numpy import where
from numpy import zeros

from . import DynamicRadiativeForcing
from ..impacts import Emissions
from ...visualizer import LinePlot
from ...visualizer import MatplotlibPlotter
from ...utilities import log


class DynamicRadiativeForcingRecord:
    """ This record keeps a timeseries record of the dynamic radiative forcing from emissions.
    
    Attributes
    ----------
    start_year : int
        Start year of the emissions record.
    time_horizon : int
        Time horizon in years.
    emissions_lst : list of Emissions Obj.
        List of emissions considered in the record.
    data_years : numpy.array of int
        Years in the record.
    data_rf : list of float
        Radiative forcing values at the time steps.
    """

    def __init__(self):
        self.time_horizon = None
        self.start_year = None
        self.emissions_lst = []
        self.data_years = None
        self.data_rf = None
        self.data_concentrations = None
    
    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_emissions(cls, emissions, start_year=2025, time_horizon=100):

        record = cls()

        record.set_start_year(start_year)
        record.set_time_horizon(time_horizon)
        record.add_emission_records(emissions)

        return record
    
    @classmethod
    def from_products():
        pass 

    # ========================
    # Setters
    # ========================
    def set_start_year(self, year):
        """ Set the start year of the dynamic radiative forcing record.
        
        Parameters
        ----------
        start_year : int
            Start year of the emissions record.        
        """
        self.start_year = year

        return self
    
    def set_time_horizon(self, years):
        """ Set the time horizon (in years) of the dynamic radiative forcing record.
        
        Parameters
        ----------
        time_horizon : int
            Time horizon in years.        
        """
        self.time_horizon = years

        return self
    
    def set_data(self):
        """ Set dynamic radiative forcing data.
        
        Returns
        -------
        list of int
            Time steps in the record.
        list of float
            Radiative forcing values at the time steps.        
        """
        time_step = 1.0
        record_start_year = self.get_start_year()
        record_time_horizon = self.get_time_horizon()

        if record_start_year is None or record_time_horizon is None:
            raise ValueError("Record start time and/or record time horizon not set.")

        # create data records
        self.data_years = arange(record_start_year, record_time_horizon + 1, 1, dtype=int16)
        self.data_concentrations = {}
        self.data_rf = {}
        for greenhouse_gas in Emissions.record_attr_dict:
            self.data_concentrations[greenhouse_gas] = zeros(self.get_time_horizon())
            self.data_rf[greenhouse_gas] = zeros(self.get_time_horizon())
                    
        # set data
        for emission in self.get_emissions_list():
            if emission.get_function() == 'pulse':
                emission_year = emission.get_year()
                time_horizon = record_start_year + self.get_time_horizon() - emission_year
                for greenhouse_gas in emission.record_attr_dict:
                    if greenhouse_gas in ['CH4fossil', 'CH4_fossil']:
                        alpha = emission.methane_bio_oxidation
                        years, concentrations, rf = DynamicRadiativeForcing.get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=False, CH4_oxidation=True, alpha=alpha)
                    else:
                        years, concentrations, rf = DynamicRadiativeForcing.get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=False)
                    years = emission_year + years

                    if emission_year < record_start_year:
                        id = where(years == record_start_year)[0]
                        year_matched_concentrations = concentrations[id,:]
                        year_matched_rf = rf[id,:]
                    else:
                        zero_years = record_start_year - emission_year
                        year_matched_concentrations = concatenate((zeros(zero_years), concentrations))
                        year_matched_rf = concatenate((zeros(zero_years), rf))

                    self.data_concentrations[greenhouse_gas] += year_matched_concentrations
                    self.data_rf[greenhouse_gas] += year_matched_rf
            else:
                pass
                #TODO: ame for other emission distributions
    # ========================
    # Getters
    # ========================    
    def get_start_year(self):
        """ Get the start year of the dynamic radiative forcing record.
        
        Returns
        -------
        int
            Start year of the emissions record.        
        """
        return self.start_yea
    
    def get_time_horizon(self):
        """ Get the time horizon (in years) of the dynamic radiative forcing record.
        
        Returns
        -------
        int
            Time horizon in years.        
        """
        return self.time_horizon
    
    def get_emissions_list(self):
        """ Get the list of emissions assigned to the dynamic radiative forcing record.
        
        Retruns
        -------
        list of Emission Obj.
            List of emissions considered in the record.
        """
        return self.emissions_lst
    
    def get_data(self):
        """ Get the dynamic radiative forcing data.

        Retruns
        -------
        list of int
            Time steps in the record.
        list of float
            Radiative forcing values at the time steps.
        """
        if self.data_years is None:
            self.set_data()

        return self.data_years, self.data_rf
    
    # ========================
    # Methods
    # ========================    
    def add_emission_records(self, emissions):
        """ Assign an emission to the dynamic radiative forcing record.
        
        Parameters
        ----------
        emissions : list or Emissions Obj.        
            Emission(s) to be assigned to the record
        """
        if isinstance(emissions, list):
            self.emissions_lst.extend(emissions)
        elif isinstance(emissions, Emissions):
            self.emissions_lst.append(emissions)

        return self
    
    def update_data_records(self):




    
    # ========================
    # Plot
    # ========================
    def plot(self, to_plot='radiative forcing', cumulative=False):
        """ Plot the dynamic radiative forcing record.

        Parameters
        ----------
        to_plot : str
            Parameter to be ploted: 'atmospheric concentration', 'emission', 'radiative forcing'.        
        """
        graph = LinePlot.from_plotter(MatplotlibPlotter)

        if to_plot == 'atmospheric concentration':
            pass # TODO add
        elif to_plot == 'emission':
            pass # TODO add
        if to_plot == 'radiative forcing':
            graph.draw([self.get_data()], f"Dynamic Radiative Forcing Record", "Year", "dynamic radiative forcing (Wm-2)")
        else:
            raise ValueError("Parameter to be plotted is not recognized. Should be 'atmospheric concentration', 'emission', or 'radiative forcing' ")

        graph.show()

        #TODO add options for cumulative

if __name__ == '__main__':
    pass
