__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.building import Building
from pod_lca.building import Assembly
from pod_lca.building import Material
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.units import KILOGRAM

# TODO: Change this to a template model

# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building()
my_building.set_eol_process_impact_database('src/pod_lca/data/impacts_podlca_eol-impacts.csv')
my_building.set_transportation_mode_impact_database('src/pod_lca/data/transportation_podlca_emission.csv')

# add a window to the building
bamboo = Material()
bamboo.qty = 538
bamboo.unit = KILOGRAM
bamboo.eol_product = 'Bamboo'

my_bamboo_roof = Assembly.create(name='Bamboo Roof', 
                                          building=my_building,
                                          materials=[bamboo]) # Making a building assembly from materials not within the scope of EOL

# impacts by cycle stage
impact_dict = {
    "C2": Impacts.from_parent(my_bamboo_roof),
    "C3": Impacts.from_parent(my_bamboo_roof),
    "C4": Impacts.from_parent(my_bamboo_roof),
}
for waste in my_bamboo_roof.get_waste_products():
    for lc_stage, impacts_lst in waste.get_impacts().items():
        if impacts_lst:
            for impact in impacts_lst:
                impact_dict[lc_stage] += impact

for lc_stage, impact in impact_dict.items():
    print(f"Life cycle stage: {lc_stage}")
    print(impact)
