from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager(name="Building A", shipping_dest= "Pennsylvania" ,shipping_org= None)

project.create_link ( material="CeilingPanel", qty=1, travel_dist= "NA",
                      return_trip_factor= None, dist_unit="km",
                      mode_name= "Barge", feul_type = "Regular" ,mode_dms_name = "Truck",
                      efficiency= 1 , efficiency_dms= 1)



print (project.get_links()[0].get_impact())
print (project.get_links()[0].get_travel_dist())

# print (project.get_links_impacts())

