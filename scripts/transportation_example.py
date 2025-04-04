from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"

project = ProjectLogisticManager(name="Building A", shipping_dest= None,
                                 data_folder=data_folder, shipping_org= None)


project.create_link ( material="Timber", qty=1, travel_dist= "Global",
                      return_trip_factor=1, dist_unit="km",
                      mode_name= "Truck", feul_type = "Regular" ,mode_dms_name = None,
                      efficiency= 3 , efficiency_dms= 1)

print (project.get_impacts())

print (project.get_scenario_distance(0))


