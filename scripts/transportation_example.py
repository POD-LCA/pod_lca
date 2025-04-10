from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"

project = ProjectLogisticManager(name="Building A", shipping_dest= "Arizona",
                                 data_folder=data_folder, shipping_org= "Hawaii")


project.create_link ( material="Tiling", qty=1, travel_dist= "None",
                      return_trip_factor= None, dist_unit="km",
                      mode_name= "Truck", feul_type = "Regular" ,mode_dms_name = None,
                      efficiency= 1 , efficiency_dms= 1)

print (project.get_impacts())
print (project.get_scenario_distance(0))
print (project.get_links()[0].get_return_trip_factor())


