__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import allclose
from numpy import arange
from numpy import array
from numpy import hstack
from numpy import vstack

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter

test_data = "tests\\drf_test_data-series-test-values.csv"
output_file = "tests\\drf_test_data-series-report.csv"
test_frame = DataImporter.csv_to_pandas(test_data)

time_horizon = 100
time_step = 1 / 120
greenhouse_gases = ["CO2", "N2O", "CH4", "CH4fossil"]

data = []
years = arange(0, time_horizon + time_step, time_step)
if years[-1] > time_horizon:
    years = years[:-1]

if not allclose(test_frame["t"], years, rtol=0.005):
    raise IndexError("Time series does not match. Update time horizon and time step.")

check = True
data = vstack((array(["year"]), years.reshape((-1, 1))))
for greenhouse_gas in greenhouse_gases:
    for cumulative in [True, False]:
        if greenhouse_gas == "CH4fossil":
            _, concentrations, y_data = DynamicRadiativeForcing().get_radiative_forcing_time_series(
                "CH4", time_horizon, time_step, cumulative, CH4_oxidation=True, alpha=1.0
            )
        else:
            _, concentrations, y_data = DynamicRadiativeForcing().get_radiative_forcing_time_series(
                greenhouse_gas, time_horizon, time_step, cumulative
            )

        if not cumulative:
            series_name = greenhouse_gas + "_concentration in atm"
            data_tmp = vstack((array([series_name]), concentrations.reshape((-1, 1))))
            data = hstack((data, data_tmp))

        series_name = greenhouse_gas + "_crf" if cumulative else greenhouse_gas + "_irf"
        data_tmp = vstack((array([series_name]), y_data.reshape((-1, 1))))
        data = hstack((data, data_tmp))

        check_1 = allclose(test_frame["Pulse" + greenhouse_gas + "qty in atm."], concentrations, rtol=0.005)
        if cumulative:
            check_2 = allclose(test_frame["Pulse" + greenhouse_gas + "CRF"], y_data, rtol=0.005)
        else:
            check_3 = allclose(test_frame["Pulse" + greenhouse_gas + "IRF"], y_data, rtol=0.005)

    if check_1 and check_2 and check_3:
        print(f"{greenhouse_gas} data passed")
    else:
        print(f"{greenhouse_gas} data failed")

DataExporter.list_to_csv(data, output_file)
