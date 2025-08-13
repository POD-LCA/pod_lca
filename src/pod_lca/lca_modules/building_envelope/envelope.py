
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

class Envelope:

    def __init__(self):
        self.name = None
        self.origin = None
        self.height = None
        self.floors = None


if __name__ == '__main__':

    for i in range(50): print('')

    import pod_lca
    from pod_lca.lca_modules.building import Building
    from pod_lca.lca_modules.operational.read_write.write import write_idf_from_building

    for i in range(50): print('')

    b = Building()
    write_idf_from_building(b)
    