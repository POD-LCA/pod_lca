from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name= "truck_1", shipping_dest = "Pennsylvania", shipping_org = None )
truck_1.set_material (material= "Steel", qty=1, qty_unit= "tonne")
truck_1.set_travel_dist (travel_dist= 12, travel_dist_unit="km", return_trip_factor= None)
truck_1.set_mode_domestic (mode = "Truck", fuel_type= "Regular", efficiency= "Median")
truck_1.set_mode_foreign (mode = "Air", fuel_type= "Regular", efficiency= "Median")

truck_1.compute_impact()

print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())

















# project.create_link ( material="Steel", qty=1, travel_dist= "NA",
#                       return_trip_factor= None, dist_unit="km",
#                       mode_name= "Barge", fuel_type = "Regular" ,mode_dms_name = "Truck",
#                       efficiency= 1 , efficiency_dms= 1)



# print (project.get_links()[0].get_impact())
# print (project.get_links()[0].get_travel_dist())

# # print (project.get_links_impacts())

