__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

from numpy import arange as np_arange

from . import AR4Calculations
from . import AR5Calculations
from . import AR6Calculations
from ...utilities import config


class DynamicRadiativeForcing:
    """Computation methods related to dynamic radiative forcing methods.

    Attributes
    ----------
    calculator : ~pod_lca.drf.ARXCalculator
        Methods specified in IPCC Annual Reports.
    """

    def __init__(self, ipcc_ar=None):
        """Create Dynamic Radiative Forcing calculator.

        Parameters
        ----------
        ipcc_ar : {'AR4', 'AR5', 'AR6'}
            The IPCC report version
        """
        if ipcc_ar is None:
            ipcc_ar = config["setup"]["drf"]["IPCC_REPORT_VERSION"]

        if ipcc_ar == "AR4":
            self.calculator = AR4Calculations
        elif ipcc_ar == "AR5":
            self.calculator = AR5Calculations
        elif ipcc_ar == "AR6":
            self.calculator = AR6Calculations
        else:
            NotImplementedError("Only IPCC AR4, AR5, and AR6 methods implemented.")

    def get_radiative_efficiency(self, greenhouse_gas, ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True):
        """Get the radiative efficiency of given greenhouse_gas.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.
        ref_unit: {'Wm-2ppb-1', 'Wm-2kg-1'}
            Output unit.
        adjust_for_indirect_effects: bool
            Adjust radiative efficiency to account for indirect effects.

        Returns
        -------
        float
            Radiative efficiency, in the reference unit.

        Raises
        ------
        ValueError
            Reference unit not recognized.
        """
        return self.calculator.get_radiative_efficiency(greenhouse_gas, ref_unit, adjust_for_indirect_effects)

    def get_pertubation_lifetime(self, greenhouse_gas):
        """Get the pertubation lifetime of the greenhouse_gas in question.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.

        Returns
        -------
        float
            Pertubation lifetime in years.
        """
        return self.calculator.get_pertubation_lifetime(greenhouse_gas)

    def get_atmospheric_concentration(self, greenhouse_gas, at_year, cumulative=False):
        """Get the concentration of the greenhouse gas in the atmosphere at a given year, given that a 1kg of gas emitted on start of year 0.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.
        at_year : int or numpy.ndarray
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg (if not cumulative) or in kg-yrs (if cumulative).
        """
        return self.calculator.get_atmospheric_concentration(greenhouse_gas, at_year, cumulative)

    def get_radiative_forcing(
        self, greenhouse_gas, at_year, cumulative=False, CH4_oxidation=False, alpha=0.5, convolution_time_step=0.01
    ):
        """Get the radiative forcing (in W/m^2) of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.
        at_year : int or numpy.ndarray
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2.
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0.
        convolution_time_step : float
            Time step for CH4 oxidation.

        Returns
        -------
        float
            radiative forcing, in W/m2.
        """
        return self.calculator.get_radiative_forcing(
            self, greenhouse_gas, at_year, cumulative, CH4_oxidation, alpha, convolution_time_step
        )

    def get_dynamic_characterization_factor(self, greenhouse_gas, time_horizon, cumulative=False):
        pass

    def get_concentration_time_series(self, greenhouse_gas, time_horizon, time_step, cumulative=False):
        """Get the concentration of the greenhouse gas in the atmosphere as a time-series.

        Note
        ----
        Noting the behaviour of numpy.arange with floats, the end value of years is checked against time horizon.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.
        time_horizon : int
            Time horizon in years.
        time_step : float
            Time step in years.
        cumulative : bool
            Cumulative radiative forcing if true, else instantaneous values.

        Returns
        -------
        :class:`numpy.ndarray`
            years of the time series
        :class:`numpy.ndarray`
            concentration values at the end of the year.
        :class:`numpy.ndarray`
            concentration values at the end of the year #TODO: double check this
        """
        years = np_arange(0, time_horizon + time_step, time_step)
        if years[-1] > time_horizon:
            years = years[:-1]
        concentrations = self.get_atmospheric_concentration(
            greenhouse_gas, years, cumulative
        )  # TODO: check the at_years variable
        return years, concentrations

    def get_radiative_forcing_time_series(
        self, greenhouse_gas, time_horizon, time_step, cumulative=True, CH4_oxidation=False, alpha=0.5
    ):
        """Get the daynamic radiative forcing values (in W/m^2) as a time-series, given that a 1kg of gas emitted on start year.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the greenhouse gas.
        time_horizon : int
            Time horizon in years.
        time_step : float
            Time step in years.
        cumulative : bool
            Cumulative radiative forcing if true, else instantaneous values.
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0

        Returns
        -------
        :class:`numpy.ndarray`
            Years of the time series
        :class:`numpy.ndarray`
            Atmospheric concentration values at the end of the year
        :class:`numpy.ndarray`
            Radiative forcing values at the end of the year

        Raises
        ------
        ValueError
            Reference unit not recognized.
        """
        return self.calculator.get_radiative_forcing_time_series(
            greenhouse_gas, time_horizon, time_step, cumulative, CH4_oxidation, alpha
        )

    def get_AGWP(self, greenhouse_gas, time_horizon):
        """Get the Absolute Global Warming Potential (AGWP) of a greenhouse gas, for the given time_horizon.

        Note
        ----
        Convolution time step of 0.01 is used.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O', 'CH4 fossil'}
            Name of the greenhouse gas.
        time_horizon : int
            Time horizon in years.
        """
        return self.calculator.get_AGWP(greenhouse_gas, time_horizon)

    def get_GWP(self, greenhouse_gas, time_horizon):
        """Get the Global Warming Potential (GWP) of a greenhouse gas, for the given time_horizon.

        Note
        ----
        Convolution time step of 0.01 is used.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O', 'CH4 fossil'}
            Name of the greenhouse gas.
        time_horizon : int
            Time horizon in years.

        Returns
        -------
        float
            GWP value.
        """
        agwp_CO2 = self.get_AGWP("CO2", time_horizon)
        agwp_gas = self.get_AGWP(greenhouse_gas, time_horizon)

        return agwp_gas / agwp_CO2


if __name__ == "__main__":
    pass
