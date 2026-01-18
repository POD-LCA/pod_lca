__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"




class Framing(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.member = None
        self.spacing = None

    @classmethod
    def from_data(cls, data):
        framing = cls()
        framing.name        = data['name']
        framing.type        = data['type']
        framing.member      = data['member']
        framing.spacing     = data['spacing']
        return framing