from lca_modules.building.building import Building
from lca_modules.building.components import BuildingComponent
from lca_modules.location.location import Location
from lca_modules.impacts.impacts_database import EOLImpactsDatabase
from utilities.units.common_units import KILOGRAM

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


# create building
my_land_plot = Location.from_str("98126, Seattle")

my_building = Building.build(name='My Shopping Mall', type='Commercial', location=my_land_plot, built_year=2025, geometry=None) # Dealing with geometry is not within the scope of EOL

eol_impact_database = EOLImpactsDatabase.new("EOL database")
eol_impact_database.set_primary_key('Material')
eol_impact_database.set_qty_key('Amount')
eol_impact_database.set_process_key('Process')
eol_impact_database.set_data(r'data/eol_impact_data_dummy.csv', impact_headers=['GWP-total (AR5) [kg CO2 eq]', 'AP [kg SO2 eq]','EP [kg N eq]', 'ODP [kg CFC-11 eq]','POCP [kg O3 eq]'], 
                                                                additional_headers=['LCA Stage'])

my_building.set_eol_database(eol_impact_database)

# add a window to the building
my_timber_window = BuildingComponent.create(name='Window', materials=[None]) # Making a building component from materials not within the scope of EOL
my_building.add_component(my_timber_window)

# deconstruct window
deconstruction_map = {
                        'Wood':{'qty': 4.2, 'unit': KILOGRAM},
                        'Inert/ND': {'qty': 0.5, 'unit': KILOGRAM}
                     }
my_timber_window.deconstruct(deconstruction_map) # TODO: code and test this

# TODO: code and test transportation links
# TODO: print outputs
# TODO: test example

# print eol impacts
