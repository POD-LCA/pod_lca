__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "Modified BSD License"
__email__ = "tmendeze@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building import BuildingFloor
from pod_lca.lca_modules.building_structure import StatisticalStructure
from pod_lca.lca_modules.building_structure import Structure
from pod_lca.lca_modules.building_envelope import BuildingEnvelope
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Layer
from pod_lca.lca_modules.building_envelope import WoodFraming
from pod_lca.lca_modules.building_envelope import BrickLayer
from pod_lca.lca_modules.building_envelope import SheathingLayer
from pod_lca.lca_modules.building_envelope import FramedWall
from pod_lca.lca_modules.building_envelope import Floor
from pod_lca.lca_modules.building_envelope import Ceiling
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyMass
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyAirGap
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyNoMass
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialPropertyGlazing
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialPropertyGas
from pod_lca.lca_modules.location import Location
from pod_lca.units import INCH, METER, FEET
from pod_lca.units import Quantity as Q
from pod_lca.utilities import ArrayMethods
from pod_lca.utilities import DataExporter
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter


# =================================
# Building Geometry
# =================================
bname = 'PODLCA Reference Building'
btype = 'Commercial'
location = Location.from_str("98126, Seattle")
built_year =  2030
life_span = 60

x = Q(120, FEET)
y = Q(180, FEET)
zero = Q(0, FEET)
floor_to_floor = Q(12, FEET)
num_stories = 8

floor_plan = [[zero,zero,zero],
              [zero,y,zero],
              [x,y,zero],
              [x,zero,zero]]
flr = BuildingFloor.from_floor_plan(floor_plan, floor_to_floor, btype)

# =================================
# Set Structure
# =================================
stype = 'CLT' # 'Concrete', 'Steel', 'CLT', 'Light-Frame'
mui_type = 'mid' # 'mid', 'high'

s_floor = Structure.create(stype, flr)
s = StatisticalStructure.create(s_floor, num_stories)
s.build(mui_type)

# =================================
# Framed Wall
# =================================

## framed wall materials
m0 = EnvelopeMaterialPropertyMass.from_database(name='Clay brick', database_entry_name='Clay brick')
m1 = EnvelopeMaterialPropertyAirGap.from_database(name='Window Air Gap', database_entry_name='Air')
m2 = EnvelopeMaterialPropertyMass.from_database(name='EPS', database_entry_name='Expanded polystyrene (EPS) Type I',)
m3 = EnvelopeMaterialPropertyMass.from_database(name='Gypsum Wall Board', database_entry_name='Gypsum board, 5/8 in')
m4 = EnvelopeMaterialPropertyMass.from_database(name='Mineral wool blanket', database_entry_name='Heavy density mineral wool board')

## framed wall layers assembled
layers_ = {
    0:BrickLayer.from_property_and_thickness(m0.name, m0, Q(0.75, INCH)),
    1:Layer.from_property_and_thickness(m1.name, m1, Q(1.5,  INCH), 'air_gap'),
    2:Layer.from_property_and_thickness(m2.name, m2, Q(1.5,  INCH), 'exterior_insulation'),
    3:SheathingLayer.from_property_and_thickness(m3.name, m3, Q(0.5,  INCH)),
    4:Layer.from_property_and_thickness(m4.name, m4, Q(2.0,  INCH), 'framing_insulation'),
    5:Layer.from_property_and_thickness(m3.name, m3, Q(0.5,  INCH), 'interior_finish'),
}

layers_[0].set_structural(True)

## framed wall framing
framing_name                  = 'wooden_framing'
framing_material_property     = EnvelopeMaterialPropertyMass.from_database(name="Softwood Lumber", database_entry_name='Softwood Lumber')
framing_spacing               = Q(12, INCH)
framing_width                 = Q(1.5, INCH)
framing_length                = Q(3.5, INCH)
framing = WoodFraming.from_parameters(framing_name, framing_material_property, framing_spacing, framing_width, framing_length)

    
framed_wall = FramedWall.from_layers_framing('framed_wall_test', layers_, framing, 'encl_curtainwall')

# =================================
# Floor
# =================================
f = Floor.from_database('Generic Interior Floor')

# =================================
# Ceiling
# =================================
c = Ceiling.from_database('Generic Interior Ceiling')

# =================================
# Windows
# =================================
# set wwr to all walls in a floor
for i in range(len(floor_plan)):
    wall_key = f'wall_{i-1}'
    wwr = .4
    window = Window.from_database('Generic Double Pane')
    window.set_wwr(wwr)

    windows = {wall_key: window}

# =================================
# Set Envelope
# =================================
ename = 'tomas_envelope'
e = Envelope.from_components(ename, flr, wall=framed_wall, floor=f, ceiling=c, windows=windows)

be = BuildingEnvelope.from_envelope_and_stories(e, num_stories)

# =================================
# Set Building
# =================================
b = Building.from_assemblies(bname, location, built_year, life_span, s, be)

# overide defaults - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# =================================
# Set OPerational Analysis Inputs
# =================================
# b.set_eplus_path("temp/EnergyPlus-25-1-0/")
# b.set_weather_file_path("src/pod_lca/data/operational_weather_seattle.epw") # default based on climate zone
b.operational_energy_method = 'eplus' # {'eplus', 'EUIs'}, default is 'eplus'

# =================================
# Export BOM
# =================================
DataExporter.df_to_csv(b.get_bom(), "bill_of_materials.csv")

# =================================
# Get Operational Impacts
# =================================
print(b.get_operational_impacts()) # default is 'total'
print(b.get_operational_emissions()) 

# =================================
# Get Embodied Impacts
# =================================
print(b.get_impacts(scope='product')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
print(b.get_emissions(scope='product'))

emission_data = ArrayMethods.objects_to_dataframe(
    objects=b.get_emissions(scope='all', objs=True),
    attributes=['CO2', 
                'CH4', 
                'N2O', 
                'temporal_emission_profile.dist_name',
                'temporal_emission_profile.start',
                'parent.name',
                'parent.life_cycle_stage'])

DataExporter.df_to_csv(emission_data, "all_emissions.csv")

# =================================
# Plots
# =================================
drf_record = b.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(b.get_impact_totals(impact_cat='GWP',
                               lc_stages=["A1-A3", "A5", "C1-C4"], #"A1-A3", "A4", "A5", "B4", "C1-C4"
                               as_df=False), 
           "Environmental impacts of Building assemblies by life cycle stage.", 
           "Life cycle stage", 
           "GWP (in kg CO2eq)",
           graph_type='stacked')
graph.show()

