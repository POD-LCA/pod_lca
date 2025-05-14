

class DynamicRadiativeForcing:

    def __init__(self):
        self.start_year = None
        self.emissions = []

    @staticmethod
    def get_radiative_efficiency(greenhouse_gas, reference, ref_unit):
        """ Get the radiative efficiency of given greenhouse_gas.
         
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g.,'CO2', 'CH4'. 'N2O'
        reference: str
            Reference used: e.g., 'AR5'
        ref_unit: str
            Output unit: 'Wm-2ppb-1', 'Wm-2kg-1'
        
        Returns
        -------
        float
            Radiative efficiency, in reference unit
        """
        pass
        # TODO: store values in a JSON in data

    @staticmethod
    def get_pertubation_lifetime(greenhouse_gas):
        """ Get the pertubation lifetime of the greenhouse_gas in question.

        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O'

        Returns
        -------
        float
            Pertubation lifetime in years.
        """
        pass
        # TODO: store values in a JSON in data
    
    def get_instantaneous_concentration(self, greenhouse_gas, year):
        """ Get the concentration of the greenhouse gas in the atmosphere at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg.       
        """
        pass
        # NOTE: takes start_year from self

    def get_instantaneous_radiative_forcing(greenhouse_gas, year):
        """ Get the radiative forcing of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            radiative forcing, in W/m2.       
        """
        pass

    def get_cumulative_radiative_forcing(self, greenhouse_gas, year):
        """ Get the cumalative radiative_forcing of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg.       
        """
        pass
        # NOTE: takes start_year from self
        # NOTE: integration methods in utilities.maths

    @staticmethod
    def get_GWP(greenhouse_gas, time_horizon):
        """ Get the Global Warming Potential of a greenhouse gas, for the given time_horizon.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.        
        """
        pass

    def get_radiative_forcing_time_series(self, time_horizon, time_step, cumulative=True):
        """ Get the daynamic radiative forcing values as a time-series.
            Considers all emissions, with their corresponding emission years.

        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.  
        time_step : float
            Time step in years.
        cumulative : bool
            Cumulative radiative forcing if true, else instantaneous values.       
        """
        pass
        # NOTE: this will take all the emissions from the emissions, and there corresponding emission years
        # NOTE: takes start_year from self
        # TODO: add emission year attribute to Emissions Records

if __name__ == '__main__':
    pass
