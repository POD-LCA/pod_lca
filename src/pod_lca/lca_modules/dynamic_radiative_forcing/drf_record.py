
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

from numpy import arange as np_arange
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
        self.time_step = None
        self.data_years = None
        self.data_irf = None
        self.data_crf = None
        self.data_concentrations = None
    
    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_emissions(cls, emissions, start_year=2025, time_horizon=100, time_step=1/12):

        record = cls()

        record.set_start_year(start_year)
        record.set_time_horizon(time_horizon)
        record.set_time_step(time_step)
        record.add_emission_records(emissions)

        return record
    
    @classmethod
    def from_products():
        pass # TODO create

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
    
    def set_time_step(self, time_step):
        """ Set the time step for time series record.
        
        Parameters
        ----------
        time_step : float
            Time step of the record.
        """
        self.time_step = time_step

    def set_data(self):
        """ Set dynamic radiative forcing data.
        
        Returns
        -------
        list of int
            Time steps in the record.
        list of float
            Radiative forcing values at the time steps.        
        """
        time_step = self.get_time_step()
        record_start_year = self.get_start_year()
        record_time_horizon = self.get_time_horizon()

        if record_start_year is None or record_time_horizon is None:
            raise ValueError("Record start time and/or record time horizon not set.")

        # create data records
        self.data_years = np_arange(record_start_year, record_start_year + record_time_horizon + time_step, time_step)
        if self.data_years[-1] > record_time_horizon:
            self.data_years = self.data_years[:-1]

        self.data_concentrations = {}
        self.data_irf = {}
        self.data_crf = {}
        for greenhouse_gas in Emissions.record_attr_dict:
            self.data_concentrations[greenhouse_gas] = zeros(len(self.data_years))
            self.data_irf[greenhouse_gas] = zeros(len(self.data_years))
            self.data_crf[greenhouse_gas] = zeros(len(self.data_years))
                    
        # set data
        for emission in self.get_emissions_list():
            if emission.get_function() == 'pulse':
                emission_year = emission.get_year()
                time_horizon = record_start_year + self.get_time_horizon() - emission_year
                for greenhouse_gas in emission.record_attr_dict:
                    greenhouse_gas_emission_qty = getattr(emission, greenhouse_gas, 0.0)
                    if greenhouse_gas_emission_qty > 0:
                        # get unit emission records
                        if greenhouse_gas in ['CH4fossil', 'CH4_fossil', 'CH4 fossil']:
                            years, concentrations, irf = DynamicRadiativeForcing.get_radiative_forcing_time_series('CH4', time_horizon, time_step, cumulative=False, CH4_oxidation=True, alpha=emission.methane_bio_oxidation)
                            _, _, crf = DynamicRadiativeForcing.get_radiative_forcing_time_series('CH4', time_horizon, time_step, cumulative=True, CH4_oxidation=True, alpha=emission.methane_bio_oxidation)
                        else:
                            years, concentrations, irf = DynamicRadiativeForcing.get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=False)
                            _, _, crf = DynamicRadiativeForcing.get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=True)
                        
                        years = emission_year + years
                        if emission_year <= record_start_year:
                            id = where(years == record_start_year)[0][0]
                            year_matched_concentrations = concentrations[id:] * greenhouse_gas_emission_qty
                            year_matched_irf = irf[id:] * greenhouse_gas_emission_qty
                            year_matched_crf = crf[id:] * greenhouse_gas_emission_qty
                        else:
                            zero_time_steps = max(where(self.data_years < emission_year)[0])
                            year_matched_concentrations = concatenate((zeros(zero_time_steps), concentrations)) * greenhouse_gas_emission_qty
                            year_matched_irf = concatenate((zeros(zero_time_steps), irf)) * greenhouse_gas_emission_qty
                            year_matched_crf = concatenate((zeros(zero_time_steps), crf)) * greenhouse_gas_emission_qty

                        self.data_concentrations[greenhouse_gas] += year_matched_concentrations
                        self.data_irf[greenhouse_gas] += year_matched_irf
                        self.data_crf[greenhouse_gas] += year_matched_crf
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
        return self.start_year
    
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
    
    def get_time_step(self):
        """ Set the time step for time series record.
        
        Retruns
        -------
        float
            Time step of the record.
        """
        return self.time_step

    def get_data(self, data_category='radiative forcing'):
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

        if data_category == 'emission':
            pass # TODO: add plotting of the emission
        elif data_category == 'atmospheric concentration':
            data_y = self.data_concentrations
        elif data_category == 'instantaneous radiative forcing':
            data_y = self.data_irf
        elif data_category == 'cumulative radiative forcing':
            data_y = self.data_crf
        else:
            raise ValueError("Data category is not recognized.")

        output_dict = {}
        data_x = self.data_years
        for item in data_y:
            output_dict[item] = list(zip(data_x, data_y[item]))

        return output_dict
    
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
    
    # ========================
    # Plot
    # ========================
    def plot(self, to_plot='atmospheric concentration', plot_type='line'):
        """ Plot the dynamic radiative forcing record.

        Parameters
        ----------
        to_plot : str
            Parameter to be ploted: 'atmospheric concentration', 'emission', 'instantaneous radiative forcing', 'Cumulative Dynamic Radiative Forcing Record'.        
        
        """
        if plot_type == 'Line':
            graph = LinePlot.from_plotter(MatplotlibPlotter)
        elif plot_type == 'stacked':
            pass # TODO: add plot type
        else:
            raise ValueError("Plot type is not recognized.")

        if to_plot == 'emission':
            title = "Greenhouse Gas Emission Record"
            y_label = "greenhouse gas emitted (kg)"
        elif to_plot == 'atmospheric concentration':
            title = "Atmospheric Greenhouse Gas Record"
            y_label = "greenhouse gas in atmosphere (kg)"
        elif to_plot == 'instantaneous radiative forcing':
            title = "Instantaneous Dynamic Radiative Forcing Record"
            y_label = "dynamic radiative forcing (Wm-2)"
        elif to_plot == 'cumulative radiative forcing':
            title = "Cumulative Dynamic Radiative Forcing Record"
            y_label = "dynamic radiative forcing (Wm-2)"
        else:
            raise ValueError("Parameter to be plotted is not recognized.")

        graph.draw(self.get_data(to_plot), title, "Year", y_label)
        # TODO: limit x axis to the time horizon

        graph.show()

if __name__ == '__main__':
    pass
