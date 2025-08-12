
from ..building import BuildingComponent


class StructuralElement(BuildingComponent):

    def __init__(self):
        super().__init__()
        self.floor = None
        self.material = None
        self.geometry = None
        self.supports = None
        self.loading = None
        self.material_volume = None

    def get_capacity(self):
        pass

    def size_member(self):
        pass


class Foundation(StructuralElement):

    def __init__(self):
        super().__init__()

class LateralStabilitySystem(StructuralElement):

    def __init__(self):
        super().__init__()

class Beam(StructuralElement):

    def __init__(self):
        super().__init__()

class Column(StructuralElement):

    def __init__(self):
        super().__init__()

class Slab(StructuralElement):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pass
