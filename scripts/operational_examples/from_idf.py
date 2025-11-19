import os
import pod_lca
from pod_lca.lca_modules.operational.operational_building import OperationalBuilding
from pod_lca.lca_modules.operational.viewers import BuildingViewer
from pod_lca.lca_modules.operational.viewers import ResultsViewer

for i in range(50):
    print("")

file = "teresa_Example_apt.idf"
filepath = os.path.join(pod_lca.DATA, "operational_dataset", "idf_examples", file)
path = pod_lca.TEMP
wea = pod_lca.SEATTLE
b = OperationalBuilding.from_idf(filepath, path, wea)


b.write_idf()
b.analyze(exe="/Applications/EnergyPlus-25-1-0/energyplus")
b.load_results()


v = BuildingViewer(b)
v.show()

v = ResultsViewer(b)
v.show("total")
