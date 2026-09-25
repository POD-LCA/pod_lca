from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.location import Location
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

# =================================================
# INPUT DATA
# =================================================
# 1. BOM CSV file
#       The CSV file should have the following columns:
#       - assembly: name of the building assembly (e.g. wall, floor, roof, etc.)
#       - material: name of the material (e.g. concrete, steel, wood, etc.)
#       - qty: quantity of the material (a numerical value)
#       - unit: unit of the quantity (e.g. kg, m3, etc.)
#       - impact_database_entry: name of the entry in the material impact database to use for the material.
#                                see pod_lca/data/impacts_podlca_building-materials.csv to find a database entry for a material, 
#                                or add an entry to the database if not already present. 
#                                The entry name in the database should match the name in the csv file.
#       - POD|LCA RSL Category: category of the material to assign a service life for the assmbly.
#                               see pod_lca/data/building_rics_service_life.csv and pod_lca/data/buildings_ashrae_service_life.csv 
#                               to see the POD|LCA RSL categories and their mapping to RICS and ASHRAE standards.
#  
# 2. model data file (or dictionary)
#       The model data can be a JSON file or a Python dictionary.
#       It should contain the following keys (default values, when not provided are also noted):
#       - building_type: type of the building ('residential', 'commercial')
#       - floor_plan: list of (x, y) coordinates defining the floor plan of the building
#       - floor_area: total floor area of the building. If floor_plan is not provided, a square floor plan will be created based on the provided floor_area.
#       - no_floors: number of floors in the building. If not provided, assumed 1.  
#       - f2f_height: floor to floor height of the building. If not provided, assumed 3 meters (or 10 ft).
#       - geometry_units: units for the floor plan and floor to floor height. If not provided, assumed meters.
#       - construction_energy_use: construction energy use for the building. If not provided, assumed 0.0.
#       - construction_energy_use_unit: unit for construction energy use. If not provided, assumed MWh.
#       - building_standard : standard used for service lives and waste rates ('RICS', 'ASHRAE'). If not provided, assumed 'ASHRAE'.
#       - logistic_type: logistic type for building material transportation ('Local', 'Global'). If not provided, assumed 'Local'. 

bom_csv_file = 'c:/Users/kiun/pod_lca/examples/building_example_bom.csv'
model_data = {
    "building_type":"commercial",
    "floor_area": 10000,
    "no_floors": 2,
    "geometry_units": "ft",
    "construction_energy_use":80,
    "construction_energy_use_unit":"MWh"
}

# Build model
my_building = Building.from_csv(
    name='buildings_podlca',
    location=Location.from_str("98126, Seattle"),
    built_year=2025,
    life_span=60,
    csv_path=bom_csv_file,
    **model_data)

# Results
print(my_building.get_impacts(scope='product',)) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(my_building.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()