class Impacts:

    def __init__(self, parent):
        self.parent = parent
        self.GWP = 0.0
        self.acid_pot = 0.0
        self.eutro_pot = 0.0
        self.ozone_dep = 0.0
        self.smog = 0.0

    def updateImpactQty(self, GWP=0.0, acid_pot=0.0, eutro_pot=0.0, ozone_dep=0.0, smog=0.0):

        self.GWP = GWP
        self.acid_pot = acid_pot
        self.eutro_pot = eutro_pot
        self.ozone_dep = ozone_dep
        self.smog = smog
