from pod_lca.impacts import ImpactsDatabase

databse_path = "src/pod_lca/data/impacts_podlca_data.csv"

impact_database = ImpactsDatabase.new("impact database")
impact_database.set_data(databse_path, additional_headers=["Taxanomy", "Category", "Sub-category", "Description"])

# impact_database.find('cement')

# impact_database.find('cement',
#                      shortlist=True)

impact_database.find(
    "cement", additional_headers=["Taxanomy", "Category", "Sub-category", "Description"], shortlist=True
)

# concrete, glue, resin, wood, cement, timber, glass, truck tranport, steel, I-beam, insulation, mushroom, steel I-beam, chemical
