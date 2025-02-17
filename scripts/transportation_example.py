from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"


project = ProjectLogisticManager(name="Building A", shipping_dest= "Seattle",
                                 data_folder=data_folder, shipping_org= None )


project.create_link ( material="Steel", qty=2, travel_dist="NA",
                      return_trip_factor=1.5, dist_unit="km",
                      mode_name= "Air",mode_dms_name = None,
                      efficiency=1, efficiency_dms= 1)

print (project.get_impact())