from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name = "Truck_1", shipping_dest = None, shipping_org = None,
                            material = "Aggregates", qty = 1, qty_unit = "tonne", travel_dist = "Regional_c",
                            travel_dist_unit = "km", return_trip_factor = None, mode_domestic = "Rail",
                            mode_domestic_fuel_type = "Regular", mode_domestic_efficiency= "High",
                            mode_foreign= None, mode_foreign_fuel_type = None, mode_foreign_efficiency = None)





truck_1.compute_impact()


print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())
print (truck_1.get_link_distances())
print (truck_1.get_return_trip_factor())



