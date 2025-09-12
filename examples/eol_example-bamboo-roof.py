
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import BuildingComponent
from pod_lca.impacts import EOLImpactsDatabase
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.transportation import EOLTransportDataset
from pod_lca.units import KILOGRAM

# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building()

eol_impact_database = EOLImpactsDatabase.new("EOL database")
eol_impact_database.set_primary_key('Material')
eol_impact_database.set_process_key('Process')
eol_impact_database.set_life_cycle_stage_key('LCA Stage')
eol_impact_database.set_data(r'data/impacts_podlca_eol-impacts.csv')

my_building.set_eol_database(eol_impact_database)
my_building.set_eol_transport_dataset(EOLTransportDataset())
my_building.set_transportation_impact_database(r'data/transportation_podlca_emission.csv')

# add a window to the building
my_bamboo_roof = BuildingComponent.create(name='Bamboo Roof', 
                                          building=my_building,
                                          materials=[None]) # Making a building component from materials not within the scope of EOL

# deconstruct window
deconstruction_map = {'Bamboo':{'qty': 538, 'unit': KILOGRAM}}
my_bamboo_roof.deconstruct(deconstruction_map)

# impacts by cycle stage
impact_dict = {'C2':Impacts.from_parent(my_bamboo_roof),
               'C3':Impacts.from_parent(my_bamboo_roof), 
               'C4':Impacts.from_parent(my_bamboo_roof)}
for waste in my_bamboo_roof.get_waste_products():
   for lc_stage, impacts_lst in waste.get_impacts().items():
      if impacts_lst:
         for impact in impacts_lst:
            impact_dict[lc_stage] += impact

for lc_stage, impact in impact_dict.items():
   print(f"Life cycle stage: {lc_stage}")
   print(impact)  
