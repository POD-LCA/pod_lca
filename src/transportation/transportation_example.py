from transportation.Project_logistic_manager import ProjectLogisticManager


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\transportation_dataset"
project = ProjectLogisticManager(name="Building A", location="Seattle", data_folder=data_folder)


project.create_link ( material="Concrete", qty=500, travel_dist=150, return_trip_factor=1.5, dist_unit="km", mode="Truck",eff=0.9)
project.create_link ( material="Concrete", qty=200, travel_dist=10, return_trip_factor=1.5, dist_unit="km", mode="Rail",eff=0.9)


print (project.get_imapct())
print (project.get_links ())