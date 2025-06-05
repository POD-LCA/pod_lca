from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager


project = ProjectLogisticManager.new("Building A")


# Example of creating a link with the project

truck_1 = project.add_link (link_name = "QC2", shipping_dest = "Pennsylvania", shipping_org = None,
                            material = "CeilingPanel", qty = 1, qty_unit = "tonne", travel_dist = "NA",
                            travel_dist_unit = "km", return_trip_factor = None, mode_domestic = "Truck",
                            mode_domestic_fuel_type = None, mode_domestic_efficiency= None,
                            mode_foreign= None, mode_foreign_fuel_type = None, mode_foreign_efficiency = "Low")


truck_1.compute_impact()
print (truck_1.get_impact_domestic())
print (truck_1.get_impact_foreign())
print (truck_1.get_link_distances())
print (truck_1.get_return_trip_factor())



