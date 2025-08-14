
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

class Envelope:

    def __init__(self):
        self.name = None
        self.height = None
        self.surfaces = {}
        self.constructions = {}


if __name__ == '__main__':

    for i in range(50): print('')

    import pod_lca
    from pod_lca.lca_modules.building import Building
    from pod_lca.lca_modules.operational.read_write.write import write_idf_from_building
    from pod_lca.units import METER

    for i in range(50): print('')

    x = 10
    y = 20

    b = Building()
    floor_plan = [[0,0,0], [x,0,0], [x,y,0], [0,y,0]]
    b.add_floor(floor_no=1, floor_plan=floor_plan, geometry_unit=METER, floor_height=3., below_grade=False, on_ground=True)

    write_idf_from_building(b)

    #TODO: Continue with zone surfaces, will have to start defining envelope stuff, layers etc. 