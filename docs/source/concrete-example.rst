*****************
Concrete Example
*****************


The following process is to be modelled and impacts visualised.

.. image:: ../_images/Smoothie_example.png
  :width: 1000
  :alt: A flow chart indicating the process of making a smoothie. On the left, under A1, are 1kg of sand, 2kg of sprinkles, 1MJ of propane, and 4kg of pickles. Each of those are transported by trucks 40km, 30km, 20km, and 17km, respectively. They are then subjected to three processes taking up energy (13kWh electricit and 1MJ of propane) and produce a smoothie. 0.5kg of CO2, 0.6kg of CH4, and 0.7 kg of NH3 is emitted along with 1kg of waste to landfill.

First the project is built, setting the project location and the impact databases.

.. code-block:: python

    from pod_lca.location import Location
    from pod_lca.materials_screening import Project

    project = Project()

    concrete_yard = Location.from_str("Seattle, Washington")
    project.set_location(concrete_yard)

    project.set_impact_database(r'data/impacts_podlca_material-data.csv')
    project.set_transportation_mode_impact_database(r'data/transportation_podlca_emission.csv')

Then, a model is created under the project and the ingredient materials are added. 

.. code-block:: python

    from pod_lca.units import KILO
    from pod_lca.units import KILOGRAM

    concrete_model = project.add_model("concrete_01")
    
    portland_cement = concrete_model.add_product(name="Portland cement", 
                                                stage="A1", 
                                                qty=367.410, unit=KILOGRAM, 
                                                impacts_from="Portland Cement", 
                                                sctg_code=32)
    fly_ash = concrete_model.add_product(name="Fly ash", 
                                        stage="A1", 
                                        qty=367.410, unit=KILOGRAM, 
                                        impacts_from="Fly Ash", 
                                        sctg_code=19)
    slag_cement = concrete_model.add_product(name="Slag cement", 
                                            stage="A1",     
                                            qty=11.340, unit=KILOGRAM, 
                                            impacts_from="Slag cement", 
                                            sctg_code=32)
    water_mixing = concrete_model.add_product(name="Water for mixing", 
                                            stage="A1", 
                                            qty=185.519, unit=KILOGRAM, 
                                            impacts_from="Tap water_ROW_[ecoinvent]", 
                                            sctg_code=20)
    water_process = concrete_model.add_product(name="Water for processing", 
                                            stage="A1", 
                                            qty=239.681, unit=KILOGRAM, 
                                            impacts_from="Tap water_ROW_[ecoinvent]", 
                                            sctg_code=20)
    crushed_coarse_aggregate = concrete_model.add_product(name="Crushed coarse aggregate", 
                                                        stage="A1", 
                                                        qty=71.668, unit=KILOGRAM, 
                                                        impacts_from="Gravel_crushed_ROW_[ecoinvent]", 
                                                        sctg_code=31)
    natural_coarse_aggregate = concrete_model.add_product(name="Natural coarse aggregate", 
                                                        stage="A1", 
                                                        qty=900.381, unit=KILOGRAM, 
                                                        impacts_from="Gravel_round_ROW_[ecoinvent]", 
                                                        sctg_code=31)
    crushed_fine_aggregate = concrete_model.add_product(name="Crushed fine aggregate", 
                                                        stage="A1", 
                                                        qty=42.184, unit=KILOGRAM, 
                                                        impacts_from="Gravel_crushed_ROW_[ecoinvent]", 
                                                        sctg_code=31)
    natural_fine_aggregate = concrete_model.add_product(name="Natural fine aggregate", 
                                                        stage="A1", 
                                                        qty=712.140, unit=KILOGRAM, 
                                                        impacts_from="Gravel_round_ROW_[ecoinvent]", 
                                                        sctg_code=31)
    air_entraining_admixture = concrete_model.add_product(name="Air entraining admixtures", 
                                                        stage="A1", 
                                                        qty=0.037, unit=KILOGRAM, 
                                                        impacts_from="Air entrainers_[EFCA]", 
                                                        sctg_code=28)
    plasticizers_superplasticizers = concrete_model.add_product(name="Plasticizers and superplasticizers", 
                                                                stage="A1", 
                                                                qty=0.255, unit=KILOGRAM, 
                                                                impacts_from="Plasticizer and Superplasticizers_[EFCA]", 
                                                                sctg_code=28)
    set_accelerators = concrete_model.add_product(name="Set accelerators", 
                                                stage="A1", 
                                                qty=0.369, unit=KILOGRAM, 
                                                impacts_from="Set accelerators_[EFCA]", 
                                                sctg_code=28)

This would automatically consider the corresponding transportation of the material as well. The user can access and change the transportation settings for individual materials.

.. code-block:: python

    cement_transportation = concrete_model.get_transportation_manager().get_transportation_leg(portland_cement)

The electricity usage can also be added.

.. code-block:: python

    from pod_lca.units import WATT_HOUR

    electricity = concrete_model.add_electricity(name="Electricity", 
                                                stage="A3", 
                                                qty=4.72, unit=KILO * WATT_HOUR)

Now the model is built, analysis can be carried out on the model.

.. code-block:: python

    from pod_lca.uncertainty import HotSpotAnalysis

    hotspot_analysis = HotSpotAnalysis.from_model(concrete_model)
    hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
    print(hotspot_analysis)

