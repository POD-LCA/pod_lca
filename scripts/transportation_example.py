from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"


project = ProjectLogisticManager(name="Building A", location= "2155 Bay St, San Francisco, CA 94123", data_folder=data_folder)
#project.create_link ( material="Carpet", qty=200.5, travel_dist= 23, return_trip_factor=1.5, dist_unit="km", mode_name="Truck",efficiency=1)
project.create_link ( material="Chillers", qty=200, travel_dist="Local", return_trip_factor=1.5, dist_unit="km", mode_name="Truck",efficiency=2)
#project.create_link ( material="Carpet", qty=200, travel_dist="Regional_c", return_trip_factor=1.5, dist_unit="km", mode= "Rail",eff=0.9)

print (project.get_impact())