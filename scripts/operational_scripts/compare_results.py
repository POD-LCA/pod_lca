import os
import operational
from lca_modules.operational.read_write import read_results_file
from lca_modules.operational.building import Building
from lca_modules.operational.viewers import ResultsViewer
from lca_modules.operational.viewers import BuildingViewer

import os
import operational
from lca_modules.operational.read_write import read_results_file
from lca_modules.operational.building import Building

for i in range(50): print('')

path = operational.TEMP
wea = operational.SEATTLE
b1 = Building.from_idf(os.path.join(operational.DATA, 'idf_examples', 'teresa_example_apt.idf'), path, wea)
filepath = os.path.join(operational.DATA, 'results', 'teresa_apt.eso')
read_results_file(b1, filepath)

b2 = Building.from_idf(os.path.join(operational.DATA, 'idf_examples', 'teresa_example_apt.idf'), path, wea)
# b2 = Building.from_idf(os.path.join(operational.TEMP, 'Building.idf'), path, wea)
filepath = os.path.join(operational.TEMP, 'eplus_output', 'eplusout.eso')
read_results_file(b2, filepath)

v = ResultsViewer(b1, b2)
v.compare('cooling')

# v = BuildingViewer(b1)
# v.show()
