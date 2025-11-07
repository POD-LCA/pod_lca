
import time
from pod_lca.impacts import ImpactsDatabase

databse_path = 'data/impacts_podlca_data.csv'

impact_database = ImpactsDatabase.new("impact database")
impact_database.set_data(databse_path)

start = time.time()
impact_database.find('cement')
end = time.time()
print('elapsed', end-start)
# concrete, glue, wood, cement, timber, glass, truck tranport, steel, I-beam, insulation, mushroom, steel I-beam
