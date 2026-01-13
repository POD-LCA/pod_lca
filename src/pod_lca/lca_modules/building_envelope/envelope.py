
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from math import isnan

from . import Construction
from . import Surface
from . import EnvelopeMaterial
from pod_lca.utilities import area_polygon
from pod_lca.utilities import centroid
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter
from ...units import UNITS_MAP
from ...utilities import log


class Envelope:

    def __init__(self):
        self.name = None
        self.floor = None
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
    def from_floor(cls, floor):
        envelope = cls()
        envelope.floor = floor
        envelope.update_envelope_surfaces()
        envelope.name = 'Envelope_floor_{}'.format(floor.floor_no)
        return envelope
    
    @classmethod
    def from_template(cls, building, building_type, envelope_opaque, envelope_translucent, roofing):
        """ Create a structure from a template model.
        
        Parameters
        ----------
        building : ~pod_lca.building.Building
            Building for which the structure belong.
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
        envelope.set_parent(building)

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
        enclosure_walls = Construction.create('walls', building, None)
        enclosure_windows = Construction.create('windows', building, None)
        enclosure_roof = Construction.create('roof', building, None)
        enclosures =  [enclosure_walls, enclosure_windows, enclosure_roof]
        
        for assembly, bom in zip(enclosures, boms):
            for item in bom.values():
                    
                building_assembly = item['assembly'].lower().replace(" ", "_").replace(",", "")
                if not (isnan(item['qty']) or (item['qty'] == '') or (isinstance(item['material'], (float, int)) and isnan(item['material'])) or (item['material'] == '')): # TODO: better check for qty
                    building_material = EnvelopeMaterial.new(
                        parent=assembly,
                        name=item['material'] + '_in_' + building_assembly,
                        qty=float(item['qty']),
                        unit=UNITS_MAP[item['unit']],
                        material_database_entry=default_database_entry_map[item['material']]['impact database entry'],
                        product_year=building.get_built_year(),
                        service_life=item['POD|LCA RSL Category']
                    )
                    assembly.add_material(building_material)
                else:
                    log("Quantity or material not specified for {} in {}. Skipping.".format(item['material'], building_assembly), level='Warn')
                
                
            # TODO:update component servie life based on materials
        
        return envelope

    @classmethod
    def from_components(cls, geometry, floors= None, ceilings=None, wall=None, windows=None, shadings=None):
        pass

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """ Set the parent building of the envelope.
        
        Parameters
        ----------
        parent : ~pod_lca.building.Building
            The building to which the envelope belong.
        """
        self.parent = parent

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get the parent building of the envelope.
        
        Returns
        -------
        ~pod_lca.building.Building
            The building to which the envelope belong.
        """
        return self.parent
        
    @property
    def height(self):
        return self.floor.height
    
    @property
    def floor_plan(self):
        return self.floor.floor_plan
    
    @property
    def area(self):
        return area_polygon(self.floor_plan)

    @property
    def volume(self):
        return self.height * self.area
    
    @property
    def centroid(self):
        return centroid(self.floor_plan)


    def update_envelope_surfaces(self):
        fp = self.floor_plan
        h = self.height
        cp = [[p[0], p[1], p[2]+h] for p in fp]
        self.surfaces['floor'] = Surface.from_polygon('floor', fp)
        self.surfaces['ceiling'] = Surface.from_polygon('ceiling', cp)
        for i in range(len(fp)):
            a = fp[i]
            if i == len(fp)-1:
                b = fp[0]
            else:
                b = fp[i+1]
            wp = [a, b, [b[0], b[1], b[2]+h], [a[0], a[1], a[2]+h]]
            wk = 'wall_{}'.format(i)
            self.surfaces[wk] = Surface.from_polygon(wk, wp)
            self.wall_surface_keys.append(wk)

    def get_assemblies(self):
        # TODO implement method to return all envelop elements as a list
        return []

    def add_construction(self, construction):
        con_dict = self.construction_map[construction.__type__]
        key = '{}_{}'.format(construction.__type__.lower(), len(con_dict))
        con_dict[key] = construction

    def add_window(self, window, wall_key):
        window.wall_key = wall_key
        key = 'Window_{}'.format(len(self.windows))
        self.windows[key] = window

    # def add_shading(self, shading):
    #     self.shadings[len(self.shadings)] = shading

if __name__ == '__main__':

    pass