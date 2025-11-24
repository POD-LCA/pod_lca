__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import Assembly
from pod_lca.building import BuildingMaterial
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.units import KILOGRAM

# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building()
my_building.set_eol_database('data/impacts_podlca_eol-impacts.csv')
my_building.set_transportation_impact_database('data/transportation_podlca_emission.csv')

# add a window to the building
concrete = BuildingMaterial()
concrete.qty = 4.100000
concrete.unit = KILOGRAM
concrete.eol_product = 'Concrete'

my_concrete_structure = Assembly.create(name='Structure', 
                                                 building=my_building, 
                                                 materials=[concrete]) 

# impacts by cycle stage
impact_dict = {
    "C2": Impacts.from_parent(my_concrete_structure),
    "C3": Impacts.from_parent(my_concrete_structure),
    "C4": Impacts.from_parent(my_concrete_structure),
    "D": Impacts.from_parent(my_concrete_structure),
}
for waste in my_concrete_structure.get_waste_products():
    for lc_stage, impacts_lst in waste.get_impacts().items():
        if impacts_lst:
            for impact in impacts_lst:
                impact_dict[lc_stage] += impact

for lc_stage, impact in impact_dict.items():
    print(f"Life cycle stage: {lc_stage}")
    print(impact)
