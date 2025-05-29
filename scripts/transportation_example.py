from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name= "truck_1", shipping_dest = None, shipping_org = None )
truck_1.set_material (material= "Elevators", qty=1, qty_unit= "tonne")
truck_1.set_travel_dist (travel_dist= "None", travel_dist_unit="km", return_trip_factor= None)
# truck_1.set_mode_domestic (mode = None, fuel_type= "Regular", efficiency= "High")
# truck_1.set_mode_foreign (mode = "Barge", fuel_type= "Regular", efficiency= "Median")
truck_1.compute_impact()


print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())
print (truck_1.get_link_distances())
print (truck_1.get_return_trip_factor())



