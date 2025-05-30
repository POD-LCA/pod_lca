from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name = "Truck_1", shipping_dest = "Arizona", shipping_org = "Hawaii",
                            material = "Tiling", qty = 1, qty_unit = "tonne", travel_dist = "Known_us",
                            travel_dist_unit = "km", return_trip_factor = None, mode_domestic = "Truck",
                            mode_domestic_fuel_type = None, mode_domestic_efficiency= None,
                            mode_foreign= None, mode_foreign_fuel_type = None, mode_foreign_efficiency = None)



truck_1.compute_impact()


print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())
print (truck_1.get_link_distances())
print (truck_1.get_return_trip_factor())



