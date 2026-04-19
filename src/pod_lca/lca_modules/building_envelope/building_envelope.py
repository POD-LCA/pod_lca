
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from copy import deepcopy

from . import Envelope
from ...utilities import geometric_key
from ...utilities import centroid
from ...utilities import log


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

    def get_envelope(self, floor_number):
        return self.envelopes[floor_number]
    
    def get_envelopes(self):
        return list(self.envelopes.values())

    def set_building(self, parent):
        self.building = parent

        envelopes = self.get_envelopes()
        for envelope in envelopes:
            envelope.set_building(parent)
            log(f"{envelope.name} added to the building", "Info")

    def set_cycle_directions(self):
        for ek in self.envelopes:
            self.envelopes[ek].set_cycle_directions()


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
            # self.network.setdefault(e1, {}).setdefault(e2, []).append(s1)
            # self.network.setdefault(e2, {}).setdefault(e1, []).append(s2)
            self.network.setdefault(e1, {})[s1] = {'envelope':e2, 'surface': s2}
            self.network.setdefault(e2, {})[s2] = {'envelope':e1, 'surface': s1}

    def set_outside_boundary_conditions(self):
        if not self.network:
            self.make_envelope_connectivity_network()
        
        for ek in self.envelopes:
            for sk in self.envelopes[ek].surfaces:
                srf = self.envelopes[ek].surfaces[sk]
                connected_env = self.network[ek][sk]['envelope']
                # connected_srf = self.network[ek][sk]['surface']
                if connected_env == 'outside':
                    if sk == 'floor':
                        obc = 'Ground'
                    elif 'wall' in sk or sk == 'ceiling':
                        obc = 'Outdoors'
                    obco = None
                else:
                    obc = 'Surface'
                    obco = self.network[ek][sk]

                srf.outside_boundary_condition = obc
                srf.outside_boundary_condition_object = obco
