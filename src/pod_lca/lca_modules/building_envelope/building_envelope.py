
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from copy import deepcopy

from . import Envelope

from pod_lca.utilities import geometric_key
from pod_lca.utilities import centroid


class BuildingEnvelope:
    def __init__(self):
        self.envelopes = {}
        self.building = None
        self.srf_gk_dict = {}
        self.network = {}

    @classmethod
    def from_envelopes(cls, envelopes):
        be = cls()
        for i, e in enumerate(envelopes):
            cls.set_envelope(e, i)
        return be
    
    @classmethod
    def from_envelope_and_stories(cls, envelope, num_stories):
        be = cls()
        for i in range(num_stories):
            data = deepcopy(envelope.to_data())
            h = i * envelope.height
            e = Envelope.from_data(data)
            e.name = '{}-{}'.format(data['name'], i)
            e.set_to_height(h)
            be.set_envelope(e, i)
        return be

    def set_envelope(self, envelope, floor_number):
        self.envelopes[floor_number] = envelope

    def set_building(self, parent):
        self.building = parent

        for ek in self.envelopes:
            for construction in self.envelopes[ek].get_constructions():
                construction.set_building()

    def get_building(self):
        """ Get the parent building of the envelope.
        
        Returns
        -------
        ~pod_lca.building.Building
            The building to which the envelope belong.
        """
        return self.building

    def make_envelope_connectivity_network(self):
        
        net = {}
        for ek in self.envelopes:
            env = self.envelopes[ek]
            for sk in env.surfaces:
                srf = env.surfaces[sk]
                cpt = centroid(srf.polygon)
                gk = geometric_key(cpt)
                node = {'environment': ek, 'surface': sk}
                if gk in net:
                    net[gk][len(net[gk])] = node
                else:
                    net[gk] = {0: node}

        for key in net:
            edge = net[key]                
            e1 = edge[0]['environment']
            s1 = edge[0]['surface']
            if len(edge) == 2:
                e2 = edge[1]['environment']
                s2 = edge[1]['surface']
            elif len(edge) == 1:
                e2 = 'outside'
                s2 = None
            self.network.setdefault(e1, {}).setdefault(e2, []).append(s1)
            self.network.setdefault(e2, {}).setdefault(e1, []).append(s2)

    def set_outside_boundary_conditions(self):
        pass
