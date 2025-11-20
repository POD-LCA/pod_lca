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
from pod_lca.utilities import DataExporter


def test_gwp_guest():
    test_data = r"tests/drf_test_gwpbio-guest2012-100yr-test-values.csv"  # select for 100 yr or 500 yr time horizon
    output_file = r"tests/drf_test_gwpbio-guest2012-100yr-report.csv"
    # test_data = r'tests/drf_test_gwpbio-guest2012-500yr-test-values.csv'
    # output_file = r'tests/drf_test_gwpbio-guest2012-500yr-report.csv'

    rotation_dict = DataImporter.csv_to_dict(test_data, "rotation")

    time_horizon = 100  # set time horizon in years, 100 or 500

    greenhouse_gas = "CO2"
    agwp_ref = DynamicRadiativeForcing().get_AGWP(greenhouse_gas, time_horizon)

    storage_periods_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # storage periods in years

    # print(agwp_ref_dict) # test if ref_agwp dictionary worked
    tests_total = 0
    tests_passed = 0
    output_dict = {}
    for rotation_period in rotation_dict:
        output_dict[rotation_period] = {}

        # for loop through storage periods
        test_status = True
        for storage_period in storage_periods_list:

            # calculate agwp of 1 kg CO2 emitted w/ pulse profile, at end of storage period (service life)
            bioenergy_pulse = Emissions.from_dict(record_dict={"CO2": 1})
            pulse = UniformEmissionProfile.unit_pulse(at=storage_period)
            bioenergy_pulse.set_temporal_emission_profile(pulse)

            # calculate agwp of 1 kg CO2 removal w/ normal profile, start at year 0, duration = rotation
            biomass_uptake = Emissions.from_dict(record_dict={"CO2": -1})
            norm = NormEmissionProfile.from_range(start=0, range=float(rotation_period))
            biomass_uptake.set_temporal_emission_profile(norm)

            drf_record = DynamicRadiativeForcingRecord.from_emissions(
                [bioenergy_pulse, biomass_uptake], start_year=0, time_horizon=time_horizon, time_step=1 / 12
            )
            drf_record.set_data()

            # optionally display plot for selected  rotation period and storage period
            if rotation_period == 50 and storage_period == 50:
                drf_record.plot(
                    "emission intensity", "lineplot"
                )  # 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing'
                drf_record.plot("atmospheric concentration", "lineplot")

            agwp_data = drf_record.get_data(data_category="cumulative radiative forcing")
            agwp_dict = dict(agwp_data)
            bio_agwp_data = agwp_dict["CO2"]
            bio_agwp_dict = dict(bio_agwp_data)
            agwp_bio = bio_agwp_dict[float(time_horizon)]


            gwpbio = agwp_bio / agwp_ref
            if time_horizon == 100:
                gwpbio = round(gwpbio, 2)  # GWP-bio factors rounded to two decimal points for 100 yr TH
            else:
                gwpbio = round(gwpbio, 3)

            test_gwpbio = float(rotation_dict[rotation_period]["GWPbio" + str(storage_period)])

            if (gwpbio and test_gwpbio) != 0:
                sym_diff_gwpbio = 2 * abs(gwpbio - test_gwpbio) / abs(gwpbio + test_gwpbio)
            else:
                sym_diff_gwpbio = "DNE"

            if (not (sym_diff_gwpbio == "DNE") and sym_diff_gwpbio > 0.005) and test_gwpbio == gwpbio:
                test_status = False

            output_dict[rotation_period]["rotation [years]"] = rotation_period
            output_dict[rotation_period]["GWPbio" + str(storage_period) + "(test value)"] = test_gwpbio
            output_dict[rotation_period]["GWPbio" + str(storage_period) + "(computed)"] = gwpbio
            output_dict[rotation_period]["diff. GWPbio" + str(storage_period) + "(%)"] = sym_diff_gwpbio
            output_dict[rotation_period]["test status" + str(storage_period)] = "PASS" if test_status else "FAIL"

        tests_total += 1
        if test_status:
            tests_passed += 1

    DataExporter.dict_to_csv(output_dict, output_file)
    print(f"GWP Guest(2012) test passed: {tests_passed} of {tests_total}")

    assert tests_passed == tests_total


if __name__ == "__main__":
    pass
