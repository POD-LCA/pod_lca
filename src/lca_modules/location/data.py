CFS_DATA_PATH = "data\\location_dataset\\location_cfs.csv" 

FAF_DOMESTIC_REGION = "data\\location_dataset\\faf_domestic_region.json"
FERC_ZIPCODE_MAP_PATH = "data\\FERC_zip_mapping.csv"
FERC_BA_ZIPCODE_MAP_PATH = "data\\FERC_BA_zip_mapping.csv"
GEA_ZIPCODE_MAP_PATH = "data\\GEA_zip_mapping.csv"
REEDS_BA_ZIPCODE_MAP_PATH = "data\\REEDS_BA_zip_mapping.csv"

FAF_DATA = {"Canada": 801, 
            "Mexico": 802, 
            "Rest of Americas": 803,
            "Europe": 804, 
            "Africa": 805, 
            "SW & Central Asia": 806,
            "Eastern Asia": 807, 
            "SE Asia & Oceania": 808}

FAF_city_representation = { 801: "Montreal",
                            802: "Veracruz",
                            803: "Santos",
                            804: "Antwerp",
                            805: "Durban",
                            806: "Mumbai",
                            807: "Shanghai",
                            808: "Saigon"}

#Clockwise order
FAF_BOUNDARIES = {
    "Canada": ([(69, -140), (68, -82), (53, -55), (44, -78), (49, -91), (49, -124), (69, -140)]), 
    "Mexico": ([(32, -116), (30, -105), (25, -97), (21, -86), (15, -91), (20, -105), (32, -116)]),
    "Europe": ([(65, -24), (71, 25), (40, 35), (30, -23), (65, -24)]),
    "Africa": ([(36, -17), (31, 31), (-31, 56), (-33, -11), (36, -17)]),
    "SW & Central Asia": ([(51, 47), (13, 44), (9, 90), (49, 88), (51, 47)]),
    "Eastern Asia": ([(50, 97), (49, 145), (25, 139), (19, 91), (50, 97)]),
    "SE Asia & Oceania": ([(9, 89), (20, 124), (-37, 177), (-45, 109), (9, 89)]),
}


MARINE_REGION = {
    "Canada": ([(69, -140), (68, -82), (53, -55), (44, -78), (49, -91), (49, -124), (69, -140)]),
    "Mexico": ([(32, -116), (30, -105), (25, -97), (21, -86), (15, -91), (20, -105), (32, -116)]),
    "Europe": ([(65, -24), (71, 25), (40, 35), (30, -23), (65, -24)]),
    "Eastern Asia": ([(50, 97), (49, 145), (25, 139), (19, 91), (50, 97)]),
    "Rest of America": ([(12, -91), (13, -32), (-25, -30), (-58, -67), (-43, -83), (12, -91)]),
    "Africa": ([(36, -17), (31, 31), (-31, 56), (-33, -11), (36, -17)]),
    "Southeastern Asia and Oceania": ([(9, 89), (20, 124), (-37, 177), (-45, 109), (9, 89)]),
    "Southern, Central, and Western Asia": ([(51, 47), (13, 44), (9, 90), (49, 88), (51, 47)]),
}


US_COAST = {
    "West Coast": ([(49, -124), (48, -104), (32, -116), (31, -106), (32, -124), (49, -124)]),
    "East Coast": ([(48, -103), (36, -101), (40, -48), (32, -79), (48, -62), (48, -103)]),
    "Gulf Coast": ([(36, -100), (32, -82), (21, -86), (24, -78), (25, -97), (28, -106), (36, -100)]),
}
