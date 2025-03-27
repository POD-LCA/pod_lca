from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"

project = ProjectLogisticManager(name="Building A", shipping_dest= "Pennsylvania",
                                 data_folder=data_folder, shipping_org= None)


project.create_link ( material="CeilingPanel", qty=1, travel_dist= "NA",
                      return_trip_factor=1, dist_unit="km",
                      mode_name= "Barge" , feul_type = "Regular" ,mode_dms_name = "Truck",
                      efficiency= 1 , efficiency_dms= 1)

print (project.get_impacts())

print (project.get_scenario_distance(0))
# project.get_scenario_distance_plot(0)

