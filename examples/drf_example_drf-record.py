
from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.dynamic_radiative_forcing import ExponentDecayEmissionProfile
from pod_lca.dynamic_radiative_forcing import UniformEmissionProfile
from pod_lca.dynamic_radiative_forcing import NormEmissionProfile
from pod_lca.dynamic_radiative_forcing import LogNormEmissionProfile

# TODO: seperate example with products, directly reading their emissions
emission_01 = Emissions.from_dict(record_dict={'CO2': 1})
pulse = UniformEmissionProfile.unit_pulse(at=2035)
emission_01.set_temporal_emission_profile(pulse)

emission_02 = Emissions.from_dict(record_dict={'CH4': 0.01})
uniform = UniformEmissionProfile.from_params(start=2045, step=10)
emission_02.set_temporal_emission_profile(uniform)

emission_03 = Emissions.from_dict(record_dict={'CH4 fossil': 0.01})
norm = NormEmissionProfile.from_range(start=2060, range=10)
emission_03.set_temporal_emission_profile(norm)
emission_03.methane_bio_oxidation = 0.5

emission_04 = Emissions.from_dict(record_dict={'N2O': 0.005})
lognorm = LogNormEmissionProfile.from_range(start=2075, range=10)
emission_04.set_temporal_emission_profile(lognorm)

emission_05 = Emissions.from_dict(record_dict={'CH4': 0.01})
expon = ExponentDecayEmissionProfile.from_decay_rate(start=2085, decay_rate=10)
# expon = ExponentDecay.from_range(start=2085, range=10)
emission_05.set_temporal_emission_profile(expon)

drf_record = DynamicRadiativeForcingRecord.from_emissions([emission_02, emission_03, emission_04, emission_05], start_year=2025, time_horizon=100, time_step=1/12)

drf_record.set_data()

drf_record.plot('emission intensity', 'lineplot') # 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing'

output_file = "save_files\\drf_record_temp.csv"
drf_record.save(output_file)
