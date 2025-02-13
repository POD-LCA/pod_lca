CFS_DATA_PATH = r"data\location_dataset\location_cfs.csv" 

FAF_DATA = {"Canada": 801, 
            "Mexico": 802, 
            "Rest of Americas": 803,
            "Europe": 804, 
            "Africa": 805, 
            "SW & Central Asia": 806,
            "Eastern Asia": 807, 
            "SE Asia & Oceania": 808}

#Clockwise order
FAF_BOUNDARIES = {
    "Canada": ([(69, -140), (68, -82), (53, -55), (44, -78), (49, -91), (49, -124), (69, -140)]), 
    "Mexico": ([(32, -116), (30, -105), (25, -97), (21, -86), (15, -91), (20, -105), (32, -116)]),
    "Europe": ([(65, -24), (71, 25), (40, 35), (40, 48), (65, -24)]),
    "Africa": ([(36, -17), (31, 31), (-31, 56), (-33, -11), (36, -17)]),
    "SW & Central Asia": ([(51, 47), (13, 44), (9, 90), (49, 88), (51, 47)]),
    "Eastern Asia": ([(50, 97), (49, 145), (25, 139), (19, 91), (50, 97)]),
    "SE Asia & Oceania": ([(9, 89), (20, 124), (-37, 177), (-45, 109), (9, 89)]),
}



FAF_DOMESTIC_REGION = r"data\location_dataset\faf_domestic_region.json"