__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

from numpy import arange as np_arange
from numpy import convolve
from numpy import zeros

from . import DynamicRadiativeForcing
from ..impacts import Emissions
from ..impacts import UniformEmissionProfile
from ..impacts import NormEmissionProfile
from ..impacts import ExponentDecayEmissionProfile
from ..impacts import LogNormEmissionProfile
from ..impacts import LinearEmissionProfile
from ..impacts import SquareRootEmissionProfile
from ...units import KILOGRAM
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataExporter
from ...utilities import DataImporter
from ...visualizer import LinePlot
from ...visualizer import MatplotlibPlotter
from ...visualizer import Stackplot


class DynamicRadiativeForcingRecord:
    """This record keeps a timeseries record of the dynamic radiative forcing from emissions.

    Attributes
    ----------
    start_year : int
        Start year of the emissions record.
    time_horizon : int
        Time horizon in years.
    time_step : int or float
        Time step of the record. The same time step is used for both for integration and for reporting.
    emissions_list : list of ~pod_lca.impacts.Emissions
        List of emissions considered in the record.
    data_years : numpy.array of int or float
        Years in the record.
    data_emission_intensity : dict
        Emission intensity (in kg/yr); {**greenhous gas** (:class:`str`): [**emission intensity** (:class:`float`)]}.
    data_concentrations : dict
        Atmospheric concentration (in kg); {**greenhous gas** (:class:`str`): [**atmospheric concenration** (:class:`float`)]}.
    data_irf : dict
        Instantaneous radiative forcing values at the time steps (in W/m^2); {**greenhous gas** (:class:`str`): [**irf** (:class:`float`)]}.
    data_crf : dict
        Cumulative radiative forcing values at the time steps (in W-yr/m^2); {**greenhous gas** (:class:`str`): [**crf** (:class:`float`)]}.
    """

    def __init__(self):
        self.time_horizon = None
        self.start_year = None
        self.time_step = None
        self.emissions_list = []
        self.data_years = None
        self.data_emission_intensity = None
        self.data_concentrations = None
        self.data_irf = None
        self.data_crf = None
        self.data_crf_ref = None
        self.data_dGWP = None
        self.data_AGTP = None

    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_emissions(cls, emissions, start_year=2025, time_horizon=100, time_step=1 / 12):
        """Create a dynamic radiative forcing (DRF) record from emissions.

        Parameters
        ----------
        emissions : list of ~pod_lca.impacts.Emissions or str
            Emissions in the record.
        start_year : int
            Start year of the record.
        time_horizon : int or float
            Time horizon of the record, in years.
        time_step : int or float
            Time step of the record, in years.

        Returns
        -------
        ~pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord
            DRF record object.
        """
        record = cls()

        record.set_start_year(start_year)
        record.set_time_horizon(time_horizon)
        record.set_time_step(time_step)
        record.add_emission_records(emissions)

        return record

    @classmethod
    def from_products(cls, products, start_year=2025, time_horizon=100, time_step=1 / 12):
        """Create a dynamic radiative forcing (DRF) record from products, inheriting from Master Obj.

        Parameters
        ----------
        products : list of ~pod_lca.materials_screening.Product or str
            Products in the record.
        start_year : int
            Start year of the record.
        time_horizon : int or float
            Time horizon of the record, in years.
        time_step : int or float
            Time step of the record, in years.

        Returns
        -------
        ~pod_lca.dynamic_radiative_forcing.DynamicRadiativeForcingRecord
            DRF record object.
        """
        emissions_list = [item.get_emissions() for item in products]

        return cls.from_emissions(emissions_list, start_year, time_horizon, time_step)

    # ========================
    # Setters
    # ========================
    def set_start_year(self, year):
        """Set the start year of the dynamic radiative forcing record.

        Parameters
        ----------
        start_year : int
            Start year of the emissions record.
        """
        self.start_year = year

        return self

    def set_time_horizon(self, years):
        """Set the time horizon (in years) of the dynamic radiative forcing record.

        Parameters
        ----------
        time_horizon : int
            Time horizon in years.
        """
        self.time_horizon = years

        return self

    def set_time_step(self, time_step):
        """Set the time step for time series record.

        Parameters
        ----------
        time_step : float
            Time step of the record.
        """
        self.time_step = time_step

    def set_data(self):
        """Set dynamic radiative forcing data.

        Returns
        -------
        :class:`list` of :class:`int`
            Time steps in the record.
        :class:`list` of :class:`float`
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

        self.data_emission_intensity = {}
        self.data_concentrations = {}
        self.data_irf = {}
        self.data_crf = {}
        self.data_dGWP = {} # dynamic GWP
        self.data_AGTP = {} # Absolute Global Temperature Potential
        for greenhouse_gas in Emissions.record_attr_dict:
            self.data_emission_intensity[greenhouse_gas] = zeros(len(self.data_years))
            self.data_concentrations[greenhouse_gas] = zeros(len(self.data_years))
            self.data_irf[greenhouse_gas] = zeros(len(self.data_years))
            self.data_crf[greenhouse_gas] = zeros(len(self.data_years))
            self.data_dGWP[greenhouse_gas] = zeros(len(self.data_years))
            self.data_AGTP[greenhouse_gas] = zeros(len(self.data_years))

        # set data
        drf_calculator = DynamicRadiativeForcing(config["setup"]["drf"]["IPCC_REPORT_VERSION"])

        #get crf_ref for pulse CO2 ref
        self.data_crf_ref = {} # reference pulse 1 kg CO2 at start year
        self.data_crf_ref["CO2"] = zeros(len(self.data_years))
        _, _, crf_CO2_ref = drf_calculator.get_radiative_forcing_time_series("CO2", record_time_horizon, time_step, cumulative=True, CH4_oxidation=True, alpha=0.5)
        self.data_crf_ref["CO2"] += crf_CO2_ref
        
        for emission in self.get_emissions_list():
            # emission time profile
            time_profile = emission.get_temporal_emission_profile()
            if time_profile.get_dist_name() == "pulse":
                pulse = UniformEmissionProfile.from_params(start=emission.get_start_year(), range=time_step)
                pulse.dist_name = "pulse"
                emission.set_temporal_emission_profile(pulse)
                time_profile = emission.get_temporal_emission_profile()
            emission_start_year = emission.get_start_year()
            emission_time_horizon = record_start_year + record_time_horizon - emission_start_year
            _, unit_emission_profile = time_profile.discrete_from_continous(
                record_start_year, record_time_horizon, time_step, integrate_point="left"
            )

            for greenhouse_gas in emission.record_attr_dict:
                conversion_factor = UNITS_MAP[emission.record_attr_dict[greenhouse_gas]].convert_to(KILOGRAM)
                greenhouse_gas_emission_qty = getattr(emission, greenhouse_gas, 0.0) * conversion_factor
                if (
                    greenhouse_gas_emission_qty != 0
                ):   # get emission records for unit pulse
                    if greenhouse_gas in ["CH4fossil", "CH4_fossil", "CH4 fossil"]:
                        _, concentrations, irf = drf_calculator.get_radiative_forcing_time_series(
                            "CH4",
                            emission_time_horizon,
                            time_step,
                            cumulative=False,
                            CH4_oxidation=True,
                            alpha=emission.methane_bio_oxidation,
                        )
                        _, _, crf = drf_calculator.get_radiative_forcing_time_series(
                            "CH4",
                            emission_time_horizon,
                            time_step,
                            cumulative=True,
                            CH4_oxidation=True,
                            alpha=emission.methane_bio_oxidation,
                        )
                        _, agtp = drf_calculator.get_AGTP_time_series(
                            "CH4",
                            time_step,
                            emission_time_horizon,
                        )
                    else:
                        _, concentrations, irf = drf_calculator.get_radiative_forcing_time_series(
                            greenhouse_gas, emission_time_horizon, time_step, cumulative=False
                        )
                        _, _, crf = drf_calculator.get_radiative_forcing_time_series(
                            greenhouse_gas, emission_time_horizon, time_step, cumulative=True
                        )
                        _, agtp = drf_calculator.get_AGTP_time_series(
                            greenhouse_gas, time_step, emission_time_horizon
                        )

                    # convolve with emission temporal profile
                    emission_profile = unit_emission_profile * greenhouse_gas_emission_qty
                    concentrations = convolve(emission_profile, concentrations)[: len(self.data_years)]
                    irf = convolve(emission_profile, irf)[: len(self.data_years)]
                    crf = convolve(emission_profile, crf)[: len(self.data_years)]
                    agtp = convolve(emission_profile, agtp)[: len(self.data_years)]

                    # calculate dynamic GWP
                    dGWP = zeros(len(self.data_years))
                    dGWP[0] = 0 # avoid divide by zero at t=start when cumulative_rf_CO2 = 0
                    dGWP[1:] = crf[1:] / crf_CO2_ref[1:]
                    

                    # add to data record
                    self.data_emission_intensity[greenhouse_gas] += emission_profile / self.get_time_step()
                    self.data_concentrations[greenhouse_gas] += concentrations
                    self.data_irf[greenhouse_gas] += irf
                    self.data_crf[greenhouse_gas] += crf
                    self.data_dGWP[greenhouse_gas] += dGWP
                    self.data_AGTP[greenhouse_gas] += agtp
        return self

    # ========================
    # Getters
    # ========================
    def get_start_year(self):
        """Get the start year of the dynamic radiative forcing record.

        Returns
        -------
        int
            Start year of the emissions record.
        """
        return self.start_year

    def get_time_horizon(self):
        """Get the time horizon (in years) of the dynamic radiative forcing record.

        Returns
        -------
        int
            Time horizon in years.
        """
        return self.time_horizon

    def get_emissions_list(self):
        """Get the list of emissions assigned to the dynamic radiative forcing record.

        Returns
        -------
        list of ~pod_lca.impacts.Emissions
            List of emissions considered in the record.
        """
        return self.emissions_list

    def get_time_step(self):
        """Set the time step for time series record.

        Returns
        -------
        float
            Time step of the record.
        """
        return self.time_step

    def get_data(self, data_category="radiative forcing", xy_pairs=True):
        """Get the dynamic radiative forcing data.

        Parameters
        ----------
        data_category : {'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing'}
            Category of data to be reported. Default is 'radiative forcing'.
        xy_pairs : bool
            If true, provide data as xy pairs, else as sperate lists. Default is True.

        Raises
        ------
        ValueError
            Data category is not recognized.
        """
        if self.data_years is None:
            self.set_data()

        if data_category == "emission intensity":
            data_y = self.data_emission_intensity
        elif data_category == "atmospheric concentration":
            data_y = self.data_concentrations
        elif data_category == "instantaneous radiative forcing":
            data_y = self.data_irf
        elif data_category == "cumulative radiative forcing":
            data_y = self.data_crf
        elif data_category == "GWP-dynamic":
            data_y = self.data_dGWP
        elif data_category == "AGTP":
            data_y = self.data_AGTP
        else:
            raise ValueError("Data category is not recognized.")

        if xy_pairs:
            output_dict = {}
            data_x = self.data_years
            for item in data_y:
                output_dict[item] = list(zip(data_x, data_y[item]))

            return output_dict
        else:
            return self.data_years, data_y

    # ========================
    # Methods
    # ========================
    def add_emission_records(self, emissions):
        """Assign an emission to the dynamic radiative forcing record.

        Parameters
        ----------
        emissions : list or ~pod_lca.impacts.Emissions
            Emission(s) to be assigned to the record
        """
        if isinstance(emissions, list):
            self.emissions_list.extend(emissions)
        elif isinstance(emissions, Emissions):
            self.emissions_list.append(emissions)

        return self

    def add_emissions_from_list_of_dicts(self, emissions):
        """Assign a list of emissions to the dynamic radiative forcing record from a dictionary.

        Parameters
        ----------
        emissions : list of dicts
            List of dictionaries containing emission data: 
                  [{'greenhouse_gas': ('CO2', 'CH4', or 'N2O'), 
                    'qty': float [kg], 
                    'emission_profile': 
                        {'profile_type': ('pulse', 'uniform', 'normal', 'exp_decay', 'lognormal', 'linear', 'sqrt'),
                            'start': int [year], 
                            **'range': float [years],
                            **'decay_rate': float [1/years],
                            **'skew': float,
                            **'slope': float}
                            }, 
                    {...}, 
                    ...]

                    (Note: '**' indicates an optional parameters depending on the profile type.)
        """
        for emission_dict in emissions:
            greenhouse_gas = emission_dict.get("greenhouse_gas")
            emission_qty = emission_dict.get("qty")
            emission_profile = emission_dict.get("emission_profile")

            if emission_qty != 0:
                emission = Emissions.from_dict({greenhouse_gas: emission_qty})

                #Assign emission profile
                profile_type = emission_profile.get("profile_type", "pulse").lower()
                t_start = emission_profile.get("start")

                if profile_type == "pulse":
                    pulse = UniformEmissionProfile.unit_pulse(at=t_start)
                    emission.set_temporal_emission_profile(pulse)

                elif profile_type == "uniform":
                    t_range = emission_profile.get("range")
                    uniform = UniformEmissionProfile.from_params(start=t_start, range=t_range)
                    emission.set_temporal_emission_profile(uniform)

                elif profile_type == "normal":
                    t_range = emission_profile.get("range")
                    norm = NormEmissionProfile.from_range(start=t_start, range=t_range)
                    emission.set_temporal_emission_profile(norm)

                elif profile_type in ["exponential decay", "exponential_decay", "exp_decay"]:
                    decay_rate = emission_profile.get("decay_rate")
                    exp_decay = ExponentDecayEmissionProfile.from_decay_rate(start=t_start, decay_rate=decay_rate)
                    emission.set_temporal_emission_profile(exp_decay)

                elif profile_type == "lognormal":
                    t_range = emission_profile.get("range")
                    skew = emission_profile.get("skew", 0)
                    lognorm = LogNormEmissionProfile.from_range(start=t_start, range=t_range, skew=skew)
                    emission.set_temporal_emission_profile(lognorm)

                elif profile_type == "linear":
                    t_range = emission_profile.get("range")
                    slope = emission_profile.get("slope")
                    linear = LinearEmissionProfile.from_params(start=t_start, range=t_range, slope=slope)
                    emission.set_temporal_emission_profile(linear)

                elif profile_type in ["square root", "square_root", "sqrt"]:
                    t_range = emission_profile.get("range")
                    sqrt = SquareRootEmissionProfile.from_range(start=t_start, range=t_range)
                    emission.set_temporal_emission_profile(sqrt)

                else:
                    raise ValueError(f"Emission profile type {profile_type} is not recognized.")

                self.emissions_list.append(emission)

        return self

    def add_emissions_from_csv(self, file_path):
        """Assign a list of emissions to the dynamic radiative forcing record from a csv file.
        Note: CSV file should have headers: 
            "Greenhouse Gas Type" : 'CO2', 'CH4', or 'N2O', 
            "Quantity (kg)" : float, 
            "Temporal Emission Profile" : 'pulse', 'uniform', 'normal', 'exponential decay', 'lognormal', 'linear', or 'square root'
            "Start Time (year)" : float,
            **"Duration (years)" : float, (required for uniform, normal, lognormal, linear, or square root profiles)
            **"Decay Rate (1/years)", (required for exponential decay profile)
            **"Skew", (required for lognormal profile)
            **"Slope (1/years)" (required for linear profile)

        Parameters
        ----------
        file_path : str
            Location of the csv file containing emission data.
        """
        emissions_data = DataImporter.csv_to_dict(file_path)
        emissions_list_raw = list(emissions_data.values())
        emissions_list_formatted = []
        #convert temporal emission profile parameter to separate dict for each emission
        for emission_dict in emissions_list_raw:
            emission_profile = {}
            for key, value in emission_dict.items():
                if key == "Greenhouse Gas Type" and value != "":
                    greenhouse_gas = value
                elif key == "Quantity (kg)" and value != "":
                    qty = float(value)
                elif key == "Temporal Emission Profile" and value != "":
                    emission_profile["profile_type"] = value
                elif key == "Start Time (year)" and value != "":
                    emission_profile["start"] = float(value)
                elif key == "Duration (years)" and value != "":
                    emission_profile["range"] = float(value)
                elif key == "Decay Rate (1/years)" and value != "":
                    emission_profile["decay_rate"] = float(value)
                elif key == "Skew" and value != "":
                    emission_profile["skew"] = float(value)
                elif key == "Slope (1/years)" and value != "":
                    emission_profile["slope"] = float(value)
                elif value == "":
                    pass
                else:
                    raise ValueError(f"Emission profile parameter {key} is not recognized.")

            emission_dict_formatted = {'greenhouse_gas': greenhouse_gas, 'qty': qty, 'emission_profile': emission_profile}
            emissions_list_formatted.append(emission_dict_formatted)

        self.add_emissions_from_list_of_dicts(emissions_list_formatted)

        return self

    # ========================
    # Plot
    # ========================
    def plot(self, to_plot="atmospheric concentration", plot_type="lineplot", plot_time_step=10, colors=None):
        """Plot the dynamic radiative forcing record.

        Parameters
        ----------
        to_plot : {'atmospheric concentration', 'emission', 'instantaneous radiative forcing', 'Cumulative Dynamic Radiative Forcing Record', 'GWP-dynamic'}
            Parameter to be ploted.
        plot_type : {'lineplot', 'stackplot'}
            Type of the plot.
        plot_time_step : int or float
            Time step for ticks along x axis.
        colors : list of str
            Colors of each line or stack.

        Raises
        ------
        ValueError
            Parameter to be plotted is not recognized.
        ValueError
            Plot type is not recognized.
        """
        if to_plot == "emission intensity":
            title = "Greenhouse Gas Emission Record"
            y_label = "greenhouse gas emission intensity (kg/yr)"
        elif to_plot == "atmospheric concentration":
            title = "Atmospheric Greenhouse Gas Record"
            y_label = "greenhouse gas in atmosphere (kg)"
        elif to_plot == "instantaneous radiative forcing":
            title = "Instantaneous Dynamic Radiative Forcing Record"
            y_label = "dynamic radiative forcing (W/m^2)"
        elif to_plot == "cumulative radiative forcing":
            title = "Cumulative Dynamic Radiative Forcing Record"
            y_label = "dynamic radiative forcing (W-yr/m^2)"
        elif to_plot == 'GWP-dynamic':
            title = "GWP-dynamic Record (kgCO2e)"
            y_label = "GWP-dynamic (kgCO2e)"
        elif to_plot == 'AGTP':
            title = "AGTP Record (K)"
            y_label = "AGTP (K)"
        else:
            raise ValueError("Parameter to be plotted is not recognized.")

        if plot_type == "lineplot":
            graph = LinePlot.from_plotter(MatplotlibPlotter)
            graph.draw(self.get_data(to_plot), title, "Year", y_label, colors)
        elif plot_type == "stackplot":
            graph = Stackplot.from_plotter(MatplotlibPlotter)
            graph.draw(*self.get_data(to_plot, xy_pairs=False), title, "Year", y_label, colors)
        else:
            raise ValueError("Plot type is not recognized.")

        x_start = self.get_start_year()
        x_end = x_start + self.get_time_horizon()
        graph.get_plot().set_xlim(x_start, x_end)
        graph.get_plot().set_xticks(range(x_start, x_end, plot_time_step))
        graph.show()

    def save(self, file_path, emission_intensity=True, concentration=True, irf=True, crf=True, crf_ref=True, dGWP=True, AGTP=True):
        """Write the data to a file.

        Parameters
        ----------
        file_path : str
            Location of the save file.
        emission_intensity : bool
            If true, save emission intensity values of greenhouse gases.
        concentration : bool
            if true, save atmospheric concentration of greenhouse gases.
        irf : bool
            If true, save the Instantaneous Radiative Forcing (IRF) values of greenhouse gases.
        crf : bool
            If true, save the Cumulative Radiative Forcing (CRF) values of greenhouse gases.
        crf_ref : bool
            If true, save the reference Cumulative Radiative Forcing values (reference pulse 1 kg CO2 emission at start year).
        dGWP : bool
            If true, save the Dynamic Global Warming Potential (dGWP) values of greenhouse gases.
        """
        if self.data_years is None:
            self.set_data()

        lists_to_write = [self.data_years.tolist()]
        headers = ["year"]

        if emission_intensity:
            for greenhouse_gas, data_array in self.data_emission_intensity.items():
                headers.append(f"{greenhouse_gas} emission intensity (kg/yr)")
                lists_to_write.append(data_array.tolist())

        if concentration:
            for greenhouse_gas, data_array in self.data_concentrations.items():
                headers.append(f"atmospheric {greenhouse_gas} (in kg)")
                lists_to_write.append(data_array.tolist())

        if irf:
            for greenhouse_gas, data_array in self.data_irf.items():
                headers.append(f"{greenhouse_gas} irf (in W/m^2)")
                lists_to_write.append(data_array.tolist())

        if crf:
            for greenhouse_gas, data_array in self.data_crf.items():
                headers.append(f"{greenhouse_gas} crf (in W-yr/m^2)")
                lists_to_write.append(data_array.tolist())

        if crf_ref:
            for greenhouse_gas, data_array in self.data_crf_ref.items():
                headers.append(f"{greenhouse_gas} crf_ref (in W-yr/m^2)")
                lists_to_write.append(data_array.tolist())

        if dGWP:
            for greenhouse_gas, data_array in self.data_dGWP.items():
                headers.append(f"{greenhouse_gas} dGWP (in kgCO2e)")
                lists_to_write.append(data_array.tolist())

        if AGTP:
            for greenhouse_gas, data_array in self.data_AGTP.items():
                headers.append(f"{greenhouse_gas} AGTP (in K)")
                lists_to_write.append(data_array.tolist())

        return DataExporter.lists_to_csv(lists_to_write, file_path, as_columns=True, headers=headers)


if __name__ == "__main__":
    pass
