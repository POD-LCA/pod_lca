from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.impacts import ExponentDecayEmissionProfile
from pod_lca.impacts import UniformEmissionProfile
from pod_lca.impacts import NormEmissionProfile
from pod_lca.impacts import LogNormEmissionProfile
from pod_lca.impacts import LinearEmissionProfile
from pod_lca.impacts import SquareRootEmissionProfile

# ========== Example creating emissions object individually ===========
emission_01 = Emissions.from_dict(record_dict={"CO2": 1})
pulse = UniformEmissionProfile.unit_pulse(at=2035)
emission_01.set_temporal_emission_profile(pulse)

emission_02 = Emissions.from_dict(record_dict={"CH4": 1})
pulse = UniformEmissionProfile.unit_pulse(at=2025)
emission_02.set_temporal_emission_profile(pulse)

emission_03 = Emissions.from_dict(record_dict={"CH4": 1})
pulse = UniformEmissionProfile.unit_pulse(at=2025)
emission_03.set_temporal_emission_profile(pulse)
emission_03.methane_bio_oxidation = 0.0 # example: CH4 non-fossil accounting for zero CH4 oxidation

emission_04 = Emissions.from_dict(record_dict={"N2O": 0.005})
lognorm = LogNormEmissionProfile.from_range(start=2075, range=10)
emission_04.set_temporal_emission_profile(lognorm)

emission_05 = Emissions.from_dict(record_dict={"CH4": 0.01})
expon = ExponentDecayEmissionProfile.from_decay_rate(start=2085, decay_rate=10)
# expon = ExponentDecay.from_range(start=2085, range=10)
emission_05.set_temporal_emission_profile(expon)

emission_06 = Emissions.from_dict(record_dict={"CO2": 1})
linear = LinearEmissionProfile.from_params(start=2035, range=50, slope=-0.1)
# linear = LinearEmissionProfile.from_percent_decrease(start=2035, step=50, percent_decrease=50)
emission_06.set_temporal_emission_profile(linear)

emission_07 = Emissions.from_dict(record_dict={"CH4": 1})
sqrt = SquareRootEmissionProfile.from_range(start=2050, range=50)
emission_07.set_temporal_emission_profile(sqrt)

drf_record = DynamicRadiativeForcingRecord.from_emissions(
    [
     emission_01, 
     # emission_02, 
     # emission_03,
     # emission_04, 
     # emission_05,
     # emission_06,
     # emission_07
     ], 
     start_year=2025, 
     time_horizon=100, 
     time_step=1 / 12
)

# ====== Example of creating a DRF record from a list of emissions dictionaries =======
'''test_emissions_list_of_dicts = [
    {"greenhouse_gas": "CO2", "qty": 1, "emission_profile": {"profile_type": "pulse", "start": 10}},
    {"greenhouse_gas": "CH4", "qty": 0.01, "emission_profile": {"profile_type": "uniform", "start": 20, "range": 10}}
]

drf_record = DynamicRadiativeForcingRecord()
drf_record.set_start_year(0)
drf_record.set_time_horizon(100)
drf_record.set_time_step(1 / 12)
drf_record.add_emissions_from_list_of_dicts(test_emissions_list_of_dicts)
'''
# ====== Example of creating a DRF record from a CSV file of emissions dictionaries =========
'''drf_record = DynamicRadiativeForcingRecord()
drf_record.set_start_year(0)
drf_record.set_time_horizon(100)
drf_record.set_time_step(1 / 12)

# Set DLCI File path
test_DLCI_file_path = "examples/drf_example_dlci.csv"
drf_record.add_emissions_from_csv(test_DLCI_file_path)
'''
# ===========================================================================================

drf_record.set_data()

drf_record.plot(
    "atmospheric concentration", "lineplot"
)  
# plot options: 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP'
# plot types: 'lineplot', 'stackplot'

output_file = "src/pod_lca/data/drf_record_temp.csv"
drf_record.save(output_file)
