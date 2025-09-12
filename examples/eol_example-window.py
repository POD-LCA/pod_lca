
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import BuildingComponent
from pod_lca.building import BuildingMaterial
from pod_lca.impacts import Emissions
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.units import KILOGRAM

# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building()
my_building.set_eol_database('data/impacts_podlca_eol-impacts.csv')
my_building.set_transportation_impact_database('data/transportation_podlca_emission.csv')

# add a window to the building
# TODO try with the database
wood = BuildingMaterial()
wood.qty = 4.2
wood.unit = KILOGRAM
wood.eol_product = 'Wood'

glass = BuildingMaterial()
glass.qty = 0.5
glass.unit = KILOGRAM
glass.eol_product = 'Glass'

my_timber_window = BuildingComponent.create(name='Window',
                                            building=my_building,
                                            materials=[wood, glass])

# impacts by life cycle stage
impact_dict = {'C2':Impacts.from_parent(my_timber_window),
               'C3':Impacts.from_parent(my_timber_window), 
               'C4':Impacts.from_parent(my_timber_window)}
emission_dict = {'C2':Emissions.from_parent(my_timber_window),
                'C3':Emissions.from_parent(my_timber_window), 
                'C4':Emissions.from_parent(my_timber_window)}
for waste in my_timber_window.get_waste_products():
   for lc_stage, impacts_lst in waste.get_impacts().items():
      if impacts_lst:
         for impact in impacts_lst:
            impact_dict[lc_stage] += impact
   for lc_stage, emissions_lst in waste.get_emissions().items():
      if emissions_lst:
         for emission in emissions_lst:
            emission_dict[lc_stage] += emission

# tests
# my_timber_window.get_waste_products()[1].get_process_mix()
# my_timber_window.get_waste_products()[1].set_process_mix({'Compost':1.0})
# my_timber_window.get_waste_products()[1].get_impacts()


for lc_stage in impact_dict.keys():
   print(f"Life cycle stage: {lc_stage}")
   print(impact_dict[lc_stage])       
   print(emission_dict[lc_stage])

# TODO: code and test transportation links
# TODO: C1 impact dummies

# TODO: test example set
#        3 - material name outside list - what is the default value to go to (both mix and impact)
#        4 - setting a mix that is NA - Error or allow with warning
