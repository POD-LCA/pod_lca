
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import arange
from numpy import array
from numpy import hstack
from numpy import vstack

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.visualizer import LinePlot
from pod_lca.visualizer import MatplotlibPlotter
from pod_lca.utilities import DataImporter

time_horizon = 500
time_step = 1
greenhouse_gases = ["CO2", "N2O", "CH4", "CH4_fossil"]
plot = False
save_file = "save_files\\DRF_timeseries.csv"

data = []
years = arange(0, time_horizon + time_step, time_step)
data = vstack((array(['year']), years.reshape((-1, 1))))
for cumulative in [True, False]:
    for greenhouse_gas in greenhouse_gases:
        if greenhouse_gas == 'CH4_fossil':
            _, _, y_data = DynamicRadiativeForcing.get_radiative_forcing_time_series('CH4', time_horizon, time_step, cumulative, CH4_oxidation=True, alpha=0.5)
        else:
            _, _, y_data = DynamicRadiativeForcing.get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative)

        series_name = greenhouse_gas + '_cumulative' if cumulative else greenhouse_gas + '_instantaneous'
        data_tmp = vstack((array([series_name]), y_data.reshape((-1, 1))))
        data = hstack((data, data_tmp ))

        if plot:
            graph = LinePlot.from_plotter(MatplotlibPlotter)
            graph.draw([years, y_data], f"Instantaneous Dynamic Radiative Forcing ({greenhouse_gas})", "Year", "dynamic radiative forcing (Wm-2)")
            graph.show()

DataImporter.list_to_csv(data, save_file)
