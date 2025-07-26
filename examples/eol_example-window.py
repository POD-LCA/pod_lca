
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import BuildingComponent
from pod_lca.impacts import Emissions
from pod_lca.impacts import EOLImpactsDatabase
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.transportation import EOLTransportDataset
from pod_lca.units import KILOGRAM

# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building.build(name='My Shopping Mall', type='Commercial', location=my_land_plot, built_year=2025, geometry=None) # Dealing with geometry is not within the scope of EOL

eol_impact_database = EOLImpactsDatabase.new("EOL database")
eol_impact_database.set_primary_key('Material')
eol_impact_database.set_process_key('Process')
eol_impact_database.set_life_cycle_stage_key('LCA Stage')
eol_impact_database.set_data(r'data/impacts_podlca_eol-impacts.csv')

my_building.set_eol_database(eol_impact_database)
my_building.set_eol_transport_dataset(EOLTransportDataset())
my_building.set_transportation_impact_database(r'data/transportation_podlca_emission.csv')

# add a window to the building
my_timber_window = BuildingComponent.create(name='Window', materials=[None]) # Making a building component from materials not within the scope of EOL
my_building.add_component(my_timber_window)

# deconstruct window
deconstruction_map = {
                        'Wood':{'qty': 4.2, 'unit': KILOGRAM},
                        # 'Glass': {'qty': 0.5, 'unit': KILOGRAM, 'bio_based': False}
                     }
my_timber_window.deconstruct(deconstruction_map)

# impacts by material and life cycle stage
# for waste in my_timber_window.get_waste_products():
#    print(waste)
#    for lc_stage, impacts_lst in waste.get_impacts().items():
#       if impacts_lst:
#          print(f"Life cycle stage: {lc_stage}")
#          for impact in impacts_lst:
#             print(impact) 

# impacts by life cycle stage
impact_dict = {'C2':Impacts.from_parent(my_timber_window),
               'C3':Impacts.from_parent(my_timber_window), 
               'C4':Impacts.from_parent(my_timber_window), 
               'D':Impacts.from_parent(my_timber_window)}
emission_dict = {'C2':Emissions.from_parent(my_timber_window),
                'C3':Emissions.from_parent(my_timber_window), 
                'C4':Emissions.from_parent(my_timber_window), 
                'D':Emissions.from_parent(my_timber_window)}
for waste in my_timber_window.get_waste_products():
   for lc_stage, impacts_lst in waste.get_impacts().items():
      if impacts_lst:
         for impact in impacts_lst:
            impact_dict[lc_stage] += impact
   for lc_stage, emissions_lst in waste.get_emissions().items():
      if emissions_lst:
         for emission in emissions_lst:
            emission_dict[lc_stage] += emission

for lc_stage in impact_dict.keys():
   print(f"Life cycle stage: {lc_stage}")
   print(impact_dict[lc_stage])       
   print(emission_dict[lc_stage])

# TODO: code and test transportation links
# TODO: C1 impact dummies

# TODO: test example set
#        3 - material name outside list - what is the default value to go to (both mix and impact)
#        4 - setting a mix that is NA - Error or allow with warning
