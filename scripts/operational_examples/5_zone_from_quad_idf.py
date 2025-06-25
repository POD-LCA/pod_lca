import os
import pod_lca

from pod_lca.lca_modules.operational.viewers import BuildingViewer
from pod_lca.lca_modules.operational.viewers import ResultsViewer
from pod_lca.lca_modules.operational.read_write import get_idf_data

from pod_lca.lca_modules.operational.operational_building import OperationalBuilding
from pod_lca.lca_modules.operational.operational_building import Window
from pod_lca.lca_modules.operational.operational_building import EquipmentList
from pod_lca.lca_modules.operational.operational_building import EquipmentConnection
from pod_lca.lca_modules.operational.operational_building import NodeList
from pod_lca.lca_modules.operational.operational_building import IdealAirLoad


for i in range(50): print('')

file = 'doe_midrise_apt.idf'
filepath = os.path.join(pod_lca.DATA, 'operational_dataset', 'idf_examples', file)
path = pod_lca.TEMP
wea = pod_lca.SEATTLE

width = 20
depth = 10
height = 3

quad = [[0, 0, 0], [width, 0, 0],[width, depth, 0],[0, depth, 0]]


b = OperationalBuilding.from_quad_5zone(path, wea, quad, height=height, zone_depth=depth/4.)
data = get_idf_data(filepath)
b.add_data_from_idf(data)


zone = b.zones[0]
w = Window.from_wall_and_wwr(zone, 2, .6)
w.construction = 'Generic Double Pane'
b.add_window(w)

zone = b.zones[1]
w = Window.from_wall_and_wwr(zone, 2, .2)
w.construction = 'Generic Double Pane'
b.add_window(w)

rules = {'Wall': 'Typical Insulated Steel Framed Exterior Wall-R16',
         'Window': 'Generic Double Pane',
         'Floor': 'Generic Interior Floor',
         'Roof': 'Generic Roof'}

b.assign_constructions_from_rules(rules)
b.set_zone_systems()


v = BuildingViewer(b)
v.show()

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus-25-1-0/energyplus')
b.load_results()

v = ResultsViewer(b)
v.show('total')
