__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import numpy as np
from bisect import bisect_left

from pod_lca.units import Quantity as Q
from pod_lca.units import KELVIN, WATT, METER, INCH


class Framing(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.member = None
        self.spacing = None
        self.L = None
        self.ds = None
        self.dII = None
        self.zf = None

    @classmethod
    def from_data(cls, data):
        framing = cls()
        framing.name        = data['name']
        framing.type        = data['type']
        framing.member      = data['member']
        framing.spacing     = data['spacing']
        framing.L           = data['L']
        framing.ds          = data['ds']
        framing.dII         = data['dII']
        return framing

    def get_zf(self, ratio):
        ratios = np.array([
            0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8,
            2.0, 2.2, 2.4, 2.6, 2.8, 3.0
        ])

        # zf values for stud depth: 3.5 in
        zf_35 = np.array([
            1.20, 1.30, 1.45, 1.55, 1.65, 1.70, 1.80, 1.85,
            1.90, 1.95, 2.00, 2.05, 2.10, 2.15
        ])

        # zf values for stud depth: 4.0 in
        zf_40 = np.array([
            1.30, 1.35, 1.60, 1.70, 1.80, 1.90, 1.95, 2.05,
            2.10, 2.15, 2.20, 2.25, 2.30, 2.35
        ])

        # zf values for stud depth: 6.0 in
        zf_60 = np.array([
            1.60, 1.80, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50,
            2.60, 2.65, 2.73, 2.80, 2.85, 2.92
        ])



        # Interpolate for each stud size
        z_35 = interp_along_ratio(ratios, zf_35, ratio)
        z_40 = interp_along_ratio(ratios, zf_40, ratio)
        z_60 = interp_along_ratio(ratios, zf_60, ratio)

        # Interpolate between stud depths
        if self.ds <= Q(3.5, INCH):
            self.zf = z_35
        elif self.ds >= Q(6.0, INCH):
            self.zf = z_60
        elif self.ds <= Q(4.0, INCH):
            self.zf = z_35 + (z_40 - z_35) * (self.ds - Q(3.5, INCH)) / Q(4.0 - 3.5, INCH)
        else:
            # Between 4.0 and 6.0:
            self.zf = z_40 + (z_60 - z_40) * (self.ds - Q(4.0, INCH)) / Q(6.0 - 4.0, INCH)

    def metal_bridge(self, ri, rins, di, Ra, Rb):

        debug = {}

        # -------------------------------
        # Metal resistivity constant
        # -------------------------------
        k_m = 26.0
        rmet = 1.0 / (k_m * 6.0)

        # TOMAS FIX, NEEDS TO BE DISCUSSED WITH TERESA
        rmet_unit = (METER * KELVIN) / WATT  
        rmet = Q(rmet, rmet_unit)
        
        
        debug["k_m"] = k_m
        debug["rmet"] = rmet

        # -------------------------------
        # Geometry
        # -------------------------------
        dI = self.ds - 2.0 * self.dII
        if dI < 0:
            raise ValueError("Metal stud too thick: dI < 0.")

        W = self.L + (self.zf * di)

        debug.update({
            "dI": dI,
            "W": W,
            "L": self.L,
            "di": di,
            "ds": self.ds,
            "dII": self.dII
        })

        # 3. Resistances

        dIxri = rins * dI
        dIIxri = rins * self.dII
        dIxrmet = rmet * dI
        dIIxrmet = rmet * self.dII

        # 4. Web & flange resistance

        # TODO: This is a hard coded unit, should be addressed with proper resistivity units
        RI = Q(dIxrmet.value * dIxri.value * W.value / (dI.value * (dIIxri.value - dIIxrmet.value) + W.value * dIxrmet.value), 
               (METER * METER * KELVIN) / WATT)
        # RI = dIxrmet * dIxri * W / (dI * (dIIxri - dIIxrmet) + W * dIxrmet)

        # TODO: This is a hard coded unit, should be addressed with proper resistivity units
        RII = Q(dIIxrmet.value * dIIxri.value * W.value / (self.L.value * (dIIxri.value - dIIxrmet.value) + W.value * dIIxrmet.value), 
        (METER * METER * KELVIN) / WATT)
        # RII = dIIxrmet * dIIxri * W / (self.L * (dIIxri - dIIxrmet) + W * dIIxrmet)

        # 5. Summations
        sum_Rcav = Ra + Rb + dIxri + 2.0 * dIIxri
        sum_RW = Ra + Rb + RI + 2.0 * RII


        # 6. Assembly R & U




        r = Q((sum_RW.value * sum_Rcav.value * self.spacing.value) / (W.value * (sum_Rcav.value - sum_RW.value) + self.spacing.value * sum_RW.value), 
                      (METER * METER * KELVIN) / WATT)
        u = r.invert()


        # -------------------------------
        # Return keys matching wall_model.py
        # -------------------------------
        return r, u

    def wood_bridge(self, width, k, Ra, Rb, rins):
        """
        Compute overall R-value of a wood stud wall using the parallel path method.
        """
        COND_TO_RIMP = 0.144
        # --------------------------
        # 1. Framing fraction
        # --------------------------
        # Fraction of wall area occupied by studs:
        f_stud = width / self.spacing
        f_stud = min(max(f_stud, 0.01), 0.30)   # keep reasonable bounds
        f_ins = 1 - f_stud

        # --------------------------
        # 2. Compute R-values
        # --------------------------

        # Cavity insulation:
        R_cavity = rins * self.ds

        # Wood stud resistance:
        # R = (1/k)*0.144 × thickness (in)
        R_wood_stud = (1 / k) * COND_TO_RIMP * self.ds

        # --------------------------
        # 3. Framing path
        # --------------------------
        R_stud_path = Ra + R_wood_stud + Rb

        # --------------------------
        # 4. Insulated path
        # --------------------------
        R_insulated_path = Ra + R_cavity + Rb

        # --------------------------
        # 5. Overall assembly by parallel method
        # --------------------------
        u = f_stud * (1 / R_stud_path) + f_ins * (1 / R_insulated_path)
        r = 1 / u

        return r, u



def interp_along_ratio(ratios, values, x):
    if x <= ratios[0]:
        return values[0]
    if x >= ratios[-1]:
        return values[-1]

    idx = bisect_left(ratios, x)
    x0, x1 = ratios[idx - 1], ratios[idx]
    y0, y1 = values[idx - 1], values[idx]

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)