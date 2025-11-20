from __future__ import print_function

import os
import json
import legacy.pod_lca_tomas

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

all = []


def read_traci_categories(filepath):
    with open(filepath, "r") as fp:
        traci = json.load(fp)

    ics = traci["impactCategories"]
    category_dict = {}
    for ic in ics:
        name = ic["name"]
        id = ic["@id"]
        unit = ic["refUnit"]
        category_dict[name] = {"id": id, "unit": unit}

    return category_dict


def read_traci_impacts(cpath, category_dict):
    traci = {}
    for ck in category_dict:
        file = "{}.json".format(category_dict[ck]["id"])
        filepath = os.path.join(cpath, file)
        with open(filepath, "r") as fp:
            traci_impact = json.load(fp)
        traci_dict = {}
        # print(traci_impact['impactFactors'][0].keys())
        for impf in traci_impact["impactFactors"]:
            iid = impf["flow"]["@id"]
            traci_dict[iid] = impf
        traci[ck] = traci_dict
    return traci


if __name__ == "__main__":

    # TODO: How does TRACI relate to Ecoinvent? Does it?

    for i in range(50):
        print("")
    path = os.path.join(legacy.pod_lca_tomas.TEMP, "TRACI_2.1_json_v1.0.0")
    category_dict = read_traci_categories(path)
    print(category_dict.keys())

    # category = 'Global warming'
    # # category = 'Smog formation'
    # lookup_impact(category, id, category_dict)

    # print(category_dict[category])
