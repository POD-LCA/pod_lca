
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
    
    from pod_lca.utilities import config
    from pod_lca.utilities import DataImporter

    molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
    print(molecular_weight_dict)



    # for i in range(50): print('')

    # b = Building()
    # write_idf_from_building(b)
    