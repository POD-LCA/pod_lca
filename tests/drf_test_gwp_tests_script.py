
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcing
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter

test_data = r'tests/drf_test_gwp-test-values.csv'
output_file = r'tests/drf_test_gwp-report.csv'

test_dict = DataImporter.csv_to_dict(test_data, 'test_name')

output_dict = {}
for test_name in tqdm(test_dict):
    output_dict[test_name] = {}

    greenhouse_gas = test_dict[test_name]['greenhouse gas']
    time_horizon = int(test_dict[test_name]['time horizon'])

    test_agwp = float(test_dict[test_name]['AGWP'])
    test_gwp = int(test_dict[test_name]['GWP'])

    agwp = DynamicRadiativeForcing().get_AGWP(greenhouse_gas, time_horizon)
    gwp = round(DynamicRadiativeForcing().get_GWP(greenhouse_gas, time_horizon))

    sym_diff_agwp = 2 * abs(agwp - test_agwp) / abs(agwp + test_agwp)

    if sym_diff_agwp < 0.005 and test_gwp == gwp:
        test_status = 'PASS'
    else:
        test_status = 'FAIL'

    output_dict[test_name]['greenhouse gas'] = greenhouse_gas
    output_dict[test_name]['time horizon'] = time_horizon
    output_dict[test_name]['AGWP (test value)'] = test_agwp
    output_dict[test_name]['AGWP (computed)'] = agwp
    output_dict[test_name]['diff. AGWP (%)'] = sym_diff_agwp
    output_dict[test_name]['GWP (test value)'] = test_gwp
    output_dict[test_name]['GWP (computed)'] = gwp
    output_dict[test_name]['test status'] = test_status

DataExporter.dict_to_csv(output_dict, output_file)
