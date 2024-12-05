**********
Example
**********

The following process is to be modelled and impacts visualised.

.. image:: /Images/Smoothie_example.png
  :width: 1000
  :alt: A flow chart indicating the process of making a smoothie. On the left, under A1, are 1kg of sand, 2kg of sprinkles, 1MJ of propane, and 4kg of pickles. Each of those are transported by trucks 40km, 30km, 20km, and 17km, respectively. They are then subjected to three processes taking up energy (13kWh electricit and 1MJ of propane) and produce a smoothie. 0.5kg of CO2, 0.6kg of CH4, and 0.7 kg of NH3 is emitted along with 1kg of waste to landfill.

First the project is built and database imported.

.. code-block:: python

    from material import HOME
    from material.projectManager.projectManager import Project
    from material.visualizer.bar_chart import BarChart

    project = Project()
    project.get_database().import_data_from_CSV(HOME + '\databaseManager\impact_data_new.csv')

Then, the supplied materials are modelled...

.. code-block:: python

    sprinkles = project.current_model.create_product("Sprinkles", "A1")
    sprinkles.update_qty(2.0)
    sprinkles.set_unit('kg')
    sprinkles.set_impact_database_entry("Sprinkles")

    sand = project.current_model.create_product("Sand", "A1")
    sand.update_qty(1.0)
    sand.set_unit('kg')
    sand.set_impact_database_entry("Sand")

    pickles = project.current_model.create_product("Pickles", "A1")
    pickles.update_qty(4.0)
    pickles.set_unit('kg')
    pickles.set_impact_database_entry("Pickles")

    propane = project.current_model.create_energy("Propane", "A1")
    propane.update_qty(1.0)
    propane.set_unit('MJ')
    propane.set_density(0.02)
    propane.set_weight_unit('kg')
    propane.set_impact_database_entry("Propane")

... followed by their transportation.

.. code-block:: python

    sprinkles_by_truck = project.current_model.create_transportation_process("Sprinkle Transportation", "A2")
    sprinkles_by_truck.set_transported_product(sprinkles)
    sprinkles_by_truck.set_transported_distance(30.0)
    sprinkles_by_truck.set_transported_distance_unit('km')
    sprinkles_by_truck.set_impact_database_entry("Transportation by truck")

    sand_by_truck = project.current_model.create_transportation_process("Sand Transportation", "A2")
    sand_by_truck.set_transported_product(sand)
    sand_by_truck.set_transported_distance(40.0)
    sand_by_truck.set_transported_distance_unit('km')
    sand_by_truck.set_impact_database_entry("Transportation by truck")

    pickles_by_truck = project.current_model.create_transportation_process("Pickles Transportation", "A2")
    pickles_by_truck.set_transported_product(pickles)
    pickles_by_truck.set_transported_distance(17.0)
    pickles_by_truck.set_transported_distance_unit('km')
    pickles_by_truck.set_impact_database_entry("Transportation by truck")

    propane_by_truck = project.current_model.create_transportation_process("Propane Transportation", "A2")
    propane_by_truck.set_transported_product(propane)
    propane_by_truck.set_transported_distance(20.0)
    propane_by_truck.set_transported_distance_unit('km')
    propane_by_truck.set_impact_database_entry("Transportation by truck")

Rest of the fuel, prodcuts, transportation processes, emissions, and waste in the manufacturing stage are modelled. Note that the custom processess (mixing, heating, and chemical reaction) are not modelled. This is as those processes in itself does not have impacts: The fuel, emisssions, and waste from those processes are modeled and will give the corresponding impacts.

.. code-block:: python

    electricity = project.current_model.create_energy("Electricity for Mixing", "A3")
    electricity.update_qty(3.0)
    electricity.set_unit('kWh')
    electricity.set_impact_database_entry("Electricity")

    propane_transported = project.current_model.create_energy("Propane for Mixing", "A3")
    propane_transported.update_qty(1.0)
    propane_transported.set_unit('MJ')
    propane_transported.set_impact_database_entry("Propane")

    product_1 = project.current_model.create_product("Product of mixing", "A3")
    product_1.update_qty(3.0)
    product_1.set_unit('kg')

    product_2 = project.current_model.create_product("Product of mixing", "A3")
    product_2.update_qty(4.0)
    product_2.set_unit('kg')

    product1_by_truck = project.current_model.create_transportation_process("Product 01 Transportation", "A2")
    product1_by_truck.set_transported_product(product_1)
    product1_by_truck.set_transported_distance(3.0)
    product1_by_truck.set_transported_distance_unit('km')
    product1_by_truck.set_impact_database_entry("Transportation by truck")

    product2_by_truck = project.current_model.create_transportation_process("Product 02 Transportation", "A2")
    product2_by_truck.set_transported_product(product_2)
    product2_by_truck.set_transported_distance(14.0)
    product2_by_truck.set_transported_distance_unit('km')
    product2_by_truck.set_impact_database_entry("Transportation by truck")

    electricity_2 = project.current_model.create_energy("Electricity for Chemical Reaction", "A3")
    electricity_2.update_qty(10.0)
    electricity_2.set_unit('kWh')
    electricity_2.set_impact_database_entry("Electricity")

    CO2 = project.current_model.create_emission("CO2", "A3")
    CO2.update_qty(0.5)
    CO2.set_unit('kg')
    CO2.set_impact_database_entry("CO2")

    CH4 = project.current_model.create_emission("CH4", "A3")
    CH4.update_qty(0.6)
    CH4.set_unit('kg')
    CH4.set_impact_database_entry("CH4")

    NH3 = project.current_model.create_emission("NH3", "A3")
    NH3.update_qty(0.7)
    NH3.set_unit('kg')
    NH3.set_impact_database_entry("NH3")

    waste = project.current_model.create_waste("Waste to landfill", "A3")
    waste.update_qty(1.0)
    waste.set_unit('kg')
    waste.set_impact_database_entry("Waste to landfill")

Finally, the global warming impact (GWP) of the process is plotted, categorized by the life cycle stage...

.. code-block:: python

    graph = BarChart(project)
    graph.set_impact_category("GWP")
    graph.set_active_models(['Model_0'])
    graph.show()

... giving the plot below.

.. image:: /Images/Bar_chart_Smoothie_example.png
  :width: 600
  :alt: A bar chart with x-axis named 'Life cyle stages' and y-axis named 'GWP impact'. Three bars in red: A1 with a value of 51; A2 with a value of 0.253; and A3 with a value of 109.609
