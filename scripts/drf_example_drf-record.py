
from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord

# TODO: seperate example with products, directly reading their emissions
emission_01 = Emissions.from_dict(record_dict={'CO2': 2.5})
emission_01.set_function('pulse')
emission_01.set_start_year(2025)

emission_02 = Emissions.from_dict(record_dict={'CO2': 1, 'CH4': 0.01})
emission_02.set_function('pulse')
emission_02.set_start_year(2030)
emission_02.methane_bio_oxidation = 0.5

drf_record = DynamicRadiativeForcingRecord.from_emissions([emission_01, emission_02], start_year=2025, time_horizon=100, time_step=1/12)

drf_record.set_data()
# TODO: linear emission from scipy/ linear emission with pulse emission
# TODO: plot emission

drf_record.plot('instantaneous radiative forcing') # 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing'
# TODO: add plot types
# TODO: limit plot extends to the time horizon

# TODO: write to file drf record
