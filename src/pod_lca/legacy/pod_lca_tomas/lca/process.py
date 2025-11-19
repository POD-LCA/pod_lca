from __future__ import print_function


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


class Process(object):

    def __init__(self):
        self.uuid = None
        self.name = None
        self.amount = None
        self.scaling_factor = None
        self.level = None
        self.outputs = []
        self.inputs = {}
        self.parent = None
        self.unit = None

    def __repr__(self):
        return "pod_lca process - <{}>".format(self.name)


class Flow(object):

    def __init__(self):
        self.name = None
        self.flow_type = None
        self.amount = None
        self.scaling_factor = None
        self.uuid = None
        self.key = None
        self.parent = None
        self.unit = None


if __name__ == "__main__":
    for i in range(50):
        print("")

    p = Process()
    pname = "Example process"
    print(p)
