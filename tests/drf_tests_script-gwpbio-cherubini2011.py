
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.dynamic_radiative_forcing import UniformEmissionProfile
from pod_lca.dynamic_radiative_forcing import NormEmissionProfile
from pod_lca.impacts import Emissions
from pod_lca.utilities import DataImporter
from pod_lca.visualizer import LinePlot
from pod_lca.visualizer import MatplotlibPlotter

test_data = r'tests/drf_test_gwpbio-cherubini2011-test-values.csv'
output_file = r'tests/drf_test_gwpbio-cherubini2011-report.csv'

rotation_dict = DataImporter.csv_to_dict(test_data, 'rotation')

time_horizon_list = [20, 100, 500]

greenhouse_gas = 'CO2'
agwp_ref_dict = {}
for time_horizon in time_horizon_list:
    agwp_ref = DynamicRadiativeForcing().get_AGWP(greenhouse_gas, time_horizon)
    agwp_ref_dict[time_horizon] = agwp_ref

# print(agwp_ref_dict) # test if ref_agwp dictionary worked

output_dict = {}
plot_dict = {}
for rotation_period in tqdm(rotation_dict):
    output_dict[rotation_period] = {}

    for time_horizon in time_horizon_list:
        agwp_ref = agwp_ref_dict[time_horizon]
        

        # calculate agwp of 1 kg CO2 emitted w/ pulse profile, at year 0
        bioenergy_pulse = Emissions.from_dict(record_dict={'CO2': 1})
        pulse = UniformEmissionProfile.unit_pulse(at=0)
        bioenergy_pulse.set_temporal_emission_profile(pulse)
        
        # calculate agwp of 1 kg CO2 removal w/ normal profile, start at year 0, duration = rotation
        biomass_uptake = Emissions.from_dict(record_dict={'CO2': -1})
        # norm = NormEmissionProfile.from_cherubini_2011(float(rotation_period))
        norm = NormEmissionProfile.from_range(start=0, range=float(rotation_period))
        biomass_uptake.set_temporal_emission_profile(norm)

        drf_record = DynamicRadiativeForcingRecord.from_emissions([bioenergy_pulse, biomass_uptake], start_year=0, time_horizon=time_horizon, time_step=1/12)
        drf_record.set_data()

        #optionally display plot for selected time horizon and rotation period
        if time_horizon == 100 and int(rotation_period) == 50:
            drf_record.plot('emission intensity', 'lineplot') # 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing'
            drf_record.plot('atmospheric concentration', 'lineplot')

        agwp_data = drf_record.get_data(data_category='cumulative radiative forcing')
        agwp_dict = dict(agwp_data)
        # print(agwp_dict)
        bio_agwp_data = agwp_dict['CO2']
        bio_agwp_dict = dict(bio_agwp_data)
        agwp_bio = bio_agwp_dict[float(time_horizon)]
        # print(agwp_bio)

        gwpbio = agwp_bio / agwp_ref
        gwpbio = round(gwpbio,2)

        test_gwpbio = float(rotation_dict[rotation_period]['GWPbio'+str(time_horizon)])

        # Compare calculated and test values
        if (gwpbio and test_gwpbio) != 0:
            sym_diff_gwpbio = 2 * abs(gwpbio - test_gwpbio) / abs(gwpbio + test_gwpbio)
        else:
           sym_diff_gwpbio = "DNE" 

        if (sym_diff_gwpbio == "DNE" or sym_diff_gwpbio < 0.005) and test_gwpbio == gwpbio:
            test_status = 'PASS'
        else:
            test_status = 'FAIL'

        output_dict[rotation_period]['rotation [years]'] = rotation_period
        output_dict[rotation_period]['GWPbio' + str(time_horizon) + '(test value)'] = test_gwpbio
        output_dict[rotation_period]['GWPbio' + str(time_horizon) + '(computed)'] = gwpbio
        output_dict[rotation_period]['diff. GWPbio' + str(time_horizon) + '(%)'] = sym_diff_gwpbio
        output_dict[rotation_period]['test status' + str(time_horizon)] = test_status
    
        if time_horizon == time_horizon_list[-1]:
            if int(rotation_period) in [1,10,20,50,100]:
                plot_dict[rotation_period] = drf_record.get_data('atmospheric concentration')['CO2']

# print(agwp_ref_dict)

DataImporter.dict_to_csv(output_dict, output_file)

graph = LinePlot.from_plotter(MatplotlibPlotter)
graph.draw(plot_dict, "Atmospheric CO2 Record", "Time (years)", "CO2 gas in atmosphere (kg)")
graph.show()
