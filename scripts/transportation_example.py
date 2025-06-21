from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name = "QC2", shipping_dest = "Montana" , shipping_org = None,
                            material = "FireSprinklers", qty = 1, qty_unit = "tonne", travel_dist = "Local",
                            travel_dist_unit = "km", return_trip_factor = None, mode_domestic = "Air",
                            mode_domestic_fuel_type = None, mode_domestic_efficiency= "Low",
                            mode_foreign= None, mode_foreign_fuel_type = None, mode_foreign_efficiency = None)


truck_1.compute_impact()
print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())
print (truck_1.get_link_distances())
print (truck_1.get_return_trip_factor())
print (truck_1.get_electricity_consumption())
print (truck_1.get_shipping_dest().get_state())
print (truck_1.get_shipping_org().get_state())
print (truck_1.get_mode_domestic().get_name())
#print (truck_1.get_mode_foreign().get_name())
print (truck_1.get_mode_domestic().get_impact())
#print (truck_1.get_mode_foreign().get_impact())