
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from math import isnan

from . import Ceiling
from . import EnvelopeMaterial
from . import Surface
from . import Wall
from . import Window
from pod_lca.utilities import area_polygon
from pod_lca.utilities import centroid

from pod_lca.utilities import config
from pod_lca.utilities import DataImporter
from ...units import UNITS_MAP
from ...utilities import log
from ...utilities import subtract_vectors
from ...utilities import dot_vectors


class Envelope:

    def __init__(self):
        self.name = None
        self.building = None
        self.floor_plan_obj = None
        self.surfaces = {}

        self.walls = {}
        self.windows = {}
        self.shadings = {}
        self.floors = {}
        self.ceiling = {}
        self.construction_map = {'Floor': self.floors,
                                 'Ceiling': self.ceiling,
                                 'Wall': self.walls,
                                 'Window': self.windows,
                                 'Shading': self.shadings}
        
        self.wall_surface_keys = []
        self.window_surface_keys = []
        self.origin = [0, 0, 0]

    @classmethod
    def from_data(cls, data):
        envelope = cls()
        envelope.name           = data['name']              
        envelope.building       = data['building']                        
        envelope.floor_plan_obj     = data['floor_plan_obj']                   

        envelope.walls          = data['walls']             
        envelope.windows        = data['windows']           
        envelope.shadings       = data['shadings']              
        envelope.floors         = data['floors']                
        envelope.ceiling        = data['ceiling']               

        for sk in data['surfaces']:
            srf = Surface.from_data(data['surfaces'][sk])
            envelope.surfaces[sk]= srf          
        

        for wk in data['windows']:
            win = Window.from_data(data['windows'][wk])
            envelope.windows[wk] = win

        envelope.construction_map = {
            'Floor': envelope.floors,
            'Ceiling': envelope.ceiling,
            'Wall': envelope.walls,
            'Window': envelope.windows,
            'Shading': envelope.shadings
        }

        return envelope

    def to_data(self):
        data = {}
        data['name']       = self.name      
        data['building']   = self.building       
        data['floor_plan_obj'] = self.floor_plan_obj   

        data['walls']      = self.walls     
        data['windows']    = self.windows   
        data['shadings']   = self.shadings  
        data['floors']     = self.floors    
        data['ceiling']    = self.ceiling   
        
        data['surfaces'] = {}
        for sk in self.surfaces:
            data['surfaces'][sk] = self.surfaces[sk].to_data()

        data['windows'] = {}
        for wk in self.windows:
            data['windows'][wk] = self.windows[wk].to_data()
        
        return data
    
    @property
    def height(self):
        return self.floor_plan_obj.height

    @property
    def floor_plan(self):
        return self.floor_plan_obj.floor_plan

    @classmethod
    def from_floor(cls, floor_plan):
        envelope = cls()
        envelope.floor = floor_plan
        envelope.update_envelope_surfaces()
        return envelope
    
    @classmethod
    def from_template(cls, building_type, envelope_opaque, envelope_translucent, roofing):
        """ Create a structure from a template model.
        
        Parameters
        ----------
        building_type : {'Commercial', 'Residential'}
            Type of building.
        envelope_opaque : {'Curtain wall: steel spandrel', 'Curtain wall: aluminum spandrel', 'MV - Brick', 'MV - Granite', 
                            'Insulated Metal Panel', 'EIFS (XPS)', 'Rainscreen, GFRC', 'Rainscreen, Thin Brick', 'Rainscreen, Wood', 
                            'Rainscreen, Formed Steel Panel', 'Brick, wood framing'}
            Template used for building opaque enclosure.
        envelope_translucent : {'Glazing, double pane IGU', 'Glazing, triple pane IGU', 'Operable window', 'Glazing, operable window'}
            Template used for building translucent enclosure.
        roofing : {'EPDM roofing', 'Asphalt shingle roofing'}
            Template used for building roofing.

        Returns
        -------
        ~pod_lca.building_structure.BuildingStructure
            Structure created.
        """
        envelope = cls()

        default_database_entry_map = DataImporter.csv_to_dict(config['file_paths']['building']['TEMPLATE_MATERIALS_DEFAULT_MAP'], 'template model material')
        
        bill_of_materials_walls_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_ENCLOSURE_OPAQUE'])
        bill_of_materials_walls = bill_of_materials_walls_all[(bill_of_materials_walls_all['building_type'].str.lower() == building_type.lower()) & 
                                                              (bill_of_materials_walls_all['assembly'].str.lower() == envelope_opaque.lower())].drop(['building_type'], axis=1).to_dict('index')
        if not bill_of_materials_walls:
            log("The opaque enclosure is empty.", 'warn')

        bill_of_materials_windows_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_ENCLOSURE_TRANSLUCENT'])
        bill_of_materials_windows = bill_of_materials_windows_all[(bill_of_materials_windows_all['building_type'].str.lower() == building_type.lower()) & 
                                                                  (bill_of_materials_windows_all['assembly'].str.lower() == envelope_translucent.lower())].drop(['building_type'], axis=1).to_dict('index')
        if not bill_of_materials_windows:
            log("The translucent enclosure is empty.", 'warn')

        bill_of_materials_roof_all = DataImporter.csv_to_pandas(config['file_paths']['building']['TEMPLATE_BOM_ROOFING'])
        bill_of_materials_roof = bill_of_materials_roof_all[(bill_of_materials_roof_all['building_type'].str.lower() == building_type.lower()) & 
                                                            (bill_of_materials_roof_all['assembly'].str.lower() == roofing.lower())].drop(['building_type'], axis=1).to_dict('index')
        if not bill_of_materials_roof:
            log("The roof is empty.", 'warn')

        boms = [bill_of_materials_walls, bill_of_materials_windows, bill_of_materials_roof]

        # FIXME: if the wwr to be calculated from these
        enclosure_walls = Wall.create('walls', None)
        enclosure_windows = Window.create('windows', None)
        enclosure_roof = Ceiling.create('roof', None)
        enclosures =  [enclosure_walls, enclosure_windows, enclosure_roof]
        
        for assembly, bom in zip(enclosures, boms):
            for item in bom.values():        
                building_assembly = item['assembly'].lower().replace(" ", "_").replace(",", "")
                if not (isnan(item['qty']) or (item['qty'] == '') or (isinstance(item['material'], (float, int)) and isnan(item['material'])) or (item['material'] == '')): # TODO: better check for qty
                    building_material = EnvelopeMaterial.new(
                        name=item['material'] + '_in_' + building_assembly,
                        qty=float(item['qty']),
                        unit=UNITS_MAP[item['unit']],
                        material_database_entry=default_database_entry_map[item['material']]['impact database entry'],
                        service_life_category=item['POD|LCA RSL Category']
                    )
                    assembly.add_material(building_material)
                else:
                    log("Quantity or material not specified for {} in {}. Skipping.".format(item['material'], building_assembly), level='Warn')
                
        for assembly in enclosures:
            if assembly.get_materials():
                envelope.add_construction(assembly)
        
        return envelope

    @classmethod
    def from_components(cls, name, floor_plan, floor=None, ceiling=None, wall=None, windows=None, shadings=None):
        envelope = cls()
        envelope.name = name
        envelope.floor_plan_obj = floor_plan
        envelope.create_envelope_surfaces()

        for sk in envelope.surfaces:
            s = envelope.surfaces[sk]
            if s.surface_type == 'Wall':
                if wall:
                    s.add_construction(wall)
                    envelope.walls[sk] = wall
            elif s.surface_type == 'Floor':
                if floor:
                    s.add_construction(floor)
                    envelope.floors[sk] = floor
            elif s.surface_type == 'Ceiling':
                if ceiling:
                    s.add_construction(ceiling)

        if windows:
            for wall_key in windows:
                win = windows[wall_key]
                envelope.add_window(win, wall_key)

        if shadings:
            pass

        envelope.set_materials_in_conmponents()

        return envelope

    # ================================
    # Setters
    # ================================
    def set_building(self, parent):
        """ Set the parent building of the envelope.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Building
            The building to which the envelope belong.
        """
        self.building = parent

        constructions = self.get_constructions()
        for construction in constructions:  
            construction.set_parent(self)
            log(f"{construction.name} added to the building", "Info")
        
        return self

    def set_cycle_directions(self):
        cpt = self.centroid
        for sk in self.surfaces:
            srf = self.surfaces[sk]
            sn = srf.normal
            sc = srf.centroid
            to_inside = subtract_vectors(cpt, sc)

            if dot_vectors(sn, to_inside) > 0:
                srf.reverse_normal()
        
        for wk in self.windows:
            win = self.windows[wk]
            sk = list(win.surfaces.keys())[0]
            srf = win.surfaces[sk]
            sn = srf.normal
            sc = srf.centroid
            to_inside = subtract_vectors(cpt, sc)

            if dot_vectors(sn, to_inside) > 0:
                srf.reverse_normal()

    def set_materials_in_conmponents(self):
        for construction in self.get_constructions():
            construction.set_materials()
    # ================================
    # Getters
    # ================================
    def get_building(self):
        """ Get the parent building of the envelope.
        
        Returns
        -------
        ~pod_lca.building.Building
            The building to which the envelope belong.
        """
        return self.building
        
    @property
    def area(self):
        return area_polygon(self.floor_plan)

    @property
    def volume(self):
        return self.height * self.area
    
    @property
    def centroid(self):
        return centroid(self.floor_plan)

    def create_envelope_surfaces(self):
        fp = self.floor_plan
        h = self.height
        cp = [[p[0], p[1], p[2]+h] for p in fp]
        self.surfaces['floor'] = Surface.from_polygon('floor', fp, surface_type ='Floor',)
        self.surfaces['ceiling'] = Surface.from_polygon('ceiling', cp, surface_type ='Ceiling')
        for i in range(len(fp)):
            a = fp[i]
            if i == len(fp)-1:
                b = fp[0]
            else:
                b = fp[i+1]
            wp = [a, b, [b[0], b[1], b[2]+h], [a[0], a[1], a[2]+h]]
            wk = 'wall_{}'.format(i)
            self.surfaces[wk] = Surface.from_polygon(wk, wp, surface_type = 'Wall')
            self.wall_surface_keys.append(wk)

    def update_envelope_surfaces_floorplan_height(self, floor_plan, height):
        self.floor_plan_obj.floor_plan = floor_plan
        f2f = self.height
        for sk in self.surfaces:
            srf = self.surfaces[sk]
            if 'wall' in sk:
                for i in range(len(floor_plan)):
                    a = floor_plan[i]
                    if i == len(floor_plan)-1:
                        b = floor_plan[0]
                    else:
                        b = floor_plan[i+1]
                    surface_polygon = [a, b, [b[0], b[1], b[2]+f2f], [a[0], a[1], a[2]+f2f]]
                    surface_key = 'wall_{}'.format(i)
                    self.wall_surface_keys.append(surface_key)
                    self.surfaces[surface_key] = Surface.from_polygon(surface_key, 
                                                                      surface_polygon, 
                                                                      surface_type = srf.surface_type,
                                                                      construction = srf.construction,
                                                                      outside_boundary_condition = srf.outside_boundary_condition,
                                                                      outside_boundary_condition_object = srf.outside_boundary_condition_object)
            else:
                if sk == 'floor':
                    surface_key = 'floor'
                    surface_polygon = floor_plan
                elif sk == 'ceiling':
                    surface_key = 'ceiling'
                    surface_polygon = [[p[0], p[1], p[2] + height] for p in floor_plan]

                self.surfaces[surface_key] = Surface.from_polygon(surface_key, 
                                                                  surface_polygon, 
                                                                  surface_type = srf.surface_type,
                                                                  construction = srf.construction,
                                                                  outside_boundary_condition = srf.outside_boundary_condition,
                                                                  outside_boundary_condition_object = srf.outside_boundary_condition_object)

    def get_constructions(self):
        """ Get a list of all enbvelope constructions of the building.
        
        Returns
        -------
        list of ~pod_lca.building_structure.Construction
            All the structural elements in the structure.
        """
        return [value for inner_dict in self.construction_map.values() for value in inner_dict.values()]

    def set_to_height(self, height):
        fp = []
        for xyz in self.floor_plan:
            fp.append([xyz[0], xyz[1], xyz[2] + height])
        self.update_envelope_surfaces_floorplan_height(fp, self.height)
        self.move_windows_up(height)

    def move_windows_up(self, height):
        for wk in self.windows:
            win = self.windows[wk]
            sk = list(win.surfaces.keys())[0]
            for i, pt in enumerate(win.surfaces[sk].polygon):
                win.surfaces[sk].polygon[i] = [pt[0], pt[1], pt[2] + height]

    # ================================
    # Add
    # ================================

    def add_constructions(self, constructions):
        """Add constructions to the building envelope.
        
        Parameters
        ----------
        constructions : list of ~pod_lca.buildings.Construction
            Constructio to be added to the building envelope.
        """
        for construction in constructions:
            self.add_assembly(construction)
            
        return self

    def add_construction(self, construction):
        """Add construction to the building envelope.
        
        Parameters
        ----------
        construction : ~pod_lca.buildings.Construction
            Constructio to be added to the building envelope.
        """
        con_dict = self.construction_map[construction.__type__]
        key = '{}_{}'.format(construction.__type__.lower(), len(con_dict))
        con_dict[key] = construction

        construction.set_parent(self)

    def add_window(self, window, wall_key):
        
        if not window.surfaces:
            window.create_window_surface_from_envelope_wall_key(self, wall_key)

        window.wall_key = wall_key
        key = 'Window_{}'.format(len(self.windows))
        self.windows[key] = window

    def add_shading(self, shading):
        self.shadings[len(self.shadings)] = shading

if __name__ == '__main__':

    pass