# Logistics Leg

[`TransportationLeg`](#pod_lca.transportation.TransportationLeg) manages individual leg of transportation, including the travel distance. Domestic link and foreign link are abstracted classes

---

### *class* pod_lca.transportation.TransportationLeg

A generic transportation leg of transporting goods.

#### manager

Refers to the transportation manager.

* **Type:**
  [*TransportationManager*](project-logistics-manager.md#pod_lca.transportation.TransportationManager)

#### name

Name of the logistic leg.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### material

name of the material.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### travel_dist

transportation distance

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### dist_unit

Unit corresponding to the travel distance.

* **Type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### return_trip_factor

transportation return trip factor.

* **Type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### shipping_dest

shipping destination location.

* **Type:**
  [*Location*](location.md#pod_lca.location.Location)

#### shipping_org

shipping origin location.

* **Type:**
  [*Location*](location.md#pod_lca.location.Location)

#### mode

transportation mode.

* **Type:**
  [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)

#### impacts

Environmental impacts of the transportation leg.

* **Type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### emissions

Emissions of the transportation leg.

* **Type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### next

Next transportation leg for the goods transported.

* **Type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### previous

Previous transportation leg for the goods transported.

* **Type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### *classmethod* in_project(good, manager, name=None)

Create a new transportation leg in the project.

* **Parameters:**
  * **good** ([*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- Product being transported.
  * **manager** ([*TransportationManager*](project-logistics-manager.md#pod_lca.transportation.TransportationManager)) -- The project to which the transportation leg belongs.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the transportation leg (default is None).
* **Returns:**
  Transportation leg created in the project.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### set_manager(manager)

Set the project the transportation leg belongs to.

* **Parameters:**
  **project** ([*TransportationManager*](project-logistics-manager.md#pod_lca.transportation.TransportationManager)) -- The project to which the transportation leg belong.

#### set_name(name)

Set the name of the transportation leg.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the transportation leg.

#### set_material(material)

Set the material being transported.

* **Parameters:**
  **material** ([*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- Material being transported.

#### set_travel_dist(travel_dist, dist_unit=None, return_trip_factor=None)

Set the travel distance of the transportation leg.

* **Parameters:**
  * **travel_dist** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Travel distance of the transportation leg.
  * **dist_unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of the travel distance. Defualt is KILOMETER
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor of the transportation leg.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Travel distance is not a number.

#### set_shipping_destination(shipping_dest)

Set the shipping destination of the project.

* **Parameters:**
  **shipping_dest** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping destination location.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Shipping destination not recognized.

#### set_shipping_origin(shipping_org)

Set the shipping origin of the project.

* **Parameters:**
  **shipping_org** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping origin location.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Shipping origin not recognized.

#### set_mode(mode=None, efficiency=None)

Set the transportation mode of the transportation leg.

#### NOTE
1. Prefix 'E_' in the mode_name is used as the identifier of an electricity based transportation mode.
2. Electric vehicles takes electricity based on origin location.

* **Parameters:**
  * **mode** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)) -- transportation mode of the transportation leg.
  * **efficiency** ( *{'Low'* *,*  *'Median'* *,*  *'High'}*) -- Efficiency of the transportation mode.

#### set_next(next)

Set the next transportation leg for the material.

* **Returns:**
  The next transportation leg for the same material.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### set_pedigree_score(pedigree_score)

Set a pedigree score (data quality score) to the transportation leg.

* **Parameters:**
  **pedigree_score** (*PedigreeScore*) -- Data quality indicator for the transportation leg.

#### get_manager()

Retrieve the project of the transportation leg.

* **Returns:**
  The project of the transportation leg.
* **Return type:**
  [*TransportationManager*](project-logistics-manager.md#pod_lca.transportation.TransportationManager)

#### get_name()

Retrieve the name of the transportation leg.

* **Returns:**
  The name of the transportation leg.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_material()

Retrieve the material of the transportation leg.

* **Returns:**
  The material of the transportation leg.
* **Return type:**
  [*Product*](products-and-processes.md#pod_lca.materials_screening.Product)

#### get_travel_dist()

Retrieve the travel distance of the transportation leg.

* **Returns:**
  The travel distance of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float) or [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_dist_unit()

Retrieve the distance unit of the transportation leg.

* **Returns:**
  The distance unit of the transportation leg.
* **Return type:**
  [*Unit*](units-object.md#pod_lca.units.Unit)

#### get_return_trip_factor()

Retrieve the return trip factor of the transportation leg.

* **Returns:**
  The return trip factor of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_shipping_destination()

Retrieve the shipping destination of the project.

* **Returns:**
  Shipping destination location.
* **Return type:**
  [*Location*](location.md#pod_lca.location.Location)

#### get_shipping_origin()

Retrieve the shipping origin of the project.

* **Returns:**
  Shipping origin location.
* **Return type:**
  [*Location*](location.md#pod_lca.location.Location)

#### get_mode()

Retrieve the transportation mode of the transportation leg.

* **Returns:**
  The domestic transportation mode of the transportation leg.
* **Return type:**
  [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)

#### get_next()

Retrieve the next transportation leg for the material.

* **Returns:**
  The next transportation leg for the same material.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### get_previous()

Retrieve the previous transportation leg for the material.

* **Returns:**
  The previous transportation leg for the same material.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### get_impacts()

Retrieve the impact of the transportation leg.

* **Returns:**
  The impact of the transportation leg.
* **Return type:**
  [*Impacts*](inventory-records.md#pod_lca.impacts.Impacts)

#### get_emissions()

Retrieve the emissions of the transportation leg.

* **Returns:**
  The emissions of the transportation leg.
* **Return type:**
  [*Emissions*](inventory-records.md#pod_lca.impacts.Emissions)

#### get_impact_database()

Get the impact database.

* **Returns:**
  Impacts database
* **Return type:**
  [*ImpactsDatabase*](impacts-database.md#pod_lca.impacts.ImpactsDatabase)

#### get_pedigree_score()

Get pedigree score of the transportation leg.

* **Returns:**
  Data quality indicator for the transportation leg.
* **Return type:**
  *PedigreeScore*

#### update_inventory_records()

Compute and update all invetories.

* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) -- Incompatible units.

### *class* pod_lca.transportation.DomesticLeg

Bases: [`TransportationLeg`](#pod_lca.transportation.TransportationLeg)

A leg of domestic US transportation.

#### transport_scenario

A discriptor of the tranportation scenario. N/A when scenario not applicable (i.e., origin and destination both known).
'No Scenario' when insufficient data points to get scenarios.

* **Type:**
  {'Local', 'Regional', 'National', 'N/A', 'No Scenario'}

#### set_transport_scenario(transport_scenario: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the transport scenario of the transportation leg.

* **Parameters:**
  **transport_scenario** ( *{'Local'* *,*  *'Regional'* *,*  *'National'* *,*  *'N/A'* *,*  *'No Scenario'}*) -- Transport scenario of the transportation leg.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transportation scenario not recognized.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Transportation scenario is not None or a string.

#### set_material(material)

Set the material being transported.

* **Parameters:**
  **material** ([*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- Material being transported.

#### set_shipping_destination(shipping_dest)

Set the shipping destination of the project.

* **Parameters:**
  **shipping_dest** ([*Location*](location.md#pod_lca.location.Location)) -- Shipping destination location.

#### set_shipping_origin(shipping_org)

Set the shipping origin of the project.

* **Parameters:**
  **shipping_org** ([*Location*](location.md#pod_lca.location.Location)) -- Shipping origin location.

#### set_mode(mode=None, efficiency=None)

Set the transportation mode of the transportation leg.

#### NOTE
1. Prefix 'E_' in the mode_name is used as the identifier of an electricity based transportation mode.
2. Electric vehicles takes electricity based on origin location.

* **Parameters:**
  * **mode** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)) -- transportation mode of the transportation leg.
  * **efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- efficiency of the transportation mode.

#### set_travel_dist(travel_dist=None, dist_unit=None, return_trip_factor=None)

Set the travel distance of the transportation leg.

* **Parameters:**
  * **travel_dist** (*None*) -- For travel distance are autogenerated from CFS data.
  * **dist_unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of the travel distance.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor of the transportation leg.

#### get_transport_scenario()

Retrieve the transport scenario of the transportation leg.

* **Returns:**
  The transport scenario of the transportation leg.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_travel_dist()

Set the travel distance of the transportation leg.

* **Returns:**
  travel distance of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float) or [str](https://docs.python.org/3/library/stdtypes.html#str)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transport scenario not recognized.

#### get_return_trip_factor()

Retrieve the return trip factor of the transportation leg.

* **Returns:**
  The return trip factor of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_dataset()

Get the dataset.

#### get_distance_from_datset()

Get the average distance from the CFS dataset based on the scenario.

#### NOTE
CFS dataset gives distances in kilometres.

* **Parameters:**
  **scenario** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- The scenario to filter the distances by.
* **Returns:**
  The distance estimate for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

### *class* pod_lca.transportation.ForeignLeg

Bases: [`TransportationLeg`](#pod_lca.transportation.TransportationLeg)

A leg of Global transportation.

#### transport_scenario

A discriptor of the tranportation scenario.

* **Type:**
  {'Global'}

#### *classmethod* in_project(good, project, name=None)

Create a new transportation leg in the project. Also create a corresponding domestic transportation leg.

* **Parameters:**
  * **good** ([*Master*](products-and-processes.md#pod_lca.materials_screening.Master)) -- Product being transported.
  * **project** ([*Project*](project.md#pod_lca.materials_screening.Project)) -- The project to which the transportation leg belongs.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Name of the transportation leg (default is None).
* **Returns:**
  Transportation leg created in the project.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### set_transport_scenario(transport_scenario: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the transport scenario of the transportation leg.

* **Parameters:**
  **transport_scenario** ( *{'Global'}*) -- Transport scenario of the transportation leg.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transportation scenario not recognized.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Transportation scenario is not None or a string.

#### set_material(material)

Set the material being transported.

* **Parameters:**
  **material** ([*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- Material being transported.

#### set_shipping_destination(shipping_dest=None)

Set the shipping destination of the project.

* **Parameters:**
  **shipping_dest** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping destination location.

#### set_shipping_origin(shipping_org=None)

Set the shipping origin of the project.

* **Parameters:**
  **shipping_org** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping origin location.

#### set_mode(mode, efficiency)

Set the transportation mode of the transportation leg.

* **Parameters:**
  * **mode** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)) -- Transportation mode of the transportation leg.
  * **efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- Efficiency of the transportation mode.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transportation mode not recognized.

#### set_travel_dist(travel_dist=None, dist_unit=None, return_trip_factor=None)

Set the travel distance of the transportation leg.

* **Parameters:**
  * **travel_dist** (*None*) -- For ForeignLink objects travel distance are autogenerated using a dataset.
  * **dist_unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of the travel distance.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor of the transportation leg (default is None).

#### get_domestic_leg()

Get the corresponding domestic leg of transportation.

* **Returns:**
  Domestic transportation leg.
* **Return type:**
  [*TransportationLeg*](#pod_lca.transportation.TransportationLeg)

#### get_transport_scenario()

Retrieve the transport scenario of the transportation leg.

* **Returns:**
  The transport scenario of the transportation leg.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_travel_dist()

Get the travel distance of the transportation leg.

* **Returns:**
  travel distance of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_return_trip_factor()

Retrieve the return trip factor of the transportation leg.

* **Returns:**
  The return trip factor of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_dataset()

Get the dataset.

* **Returns:**
  Dataset used.
* **Return type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### get_distance_from_dataset(transport_scenario)

Get the average distance from the CFS dataset based on the scenario.

* **Parameters:**
  **scenario** ( *{'Global'}*) -- The tranportation scenario.
* **Returns:**
  The distance estimate for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- The transportation origin and transportation mode are inconsistant.

#### check_mode_origin_compatibility()

Check if the mode and origin combinations are realistic.

### *class* pod_lca.transportation.WasteTransportLeg

Bases: [`TransportationLeg`](#pod_lca.transportation.TransportationLeg)

A leg of waste transportation.

#### transport_scenario

A discriptor of the tranportation scenario.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### eol_pathway

End-of-life pathway:

- 'Landfill': transporting waste to a landfill.
- 'Recycle': transporting waste to a recycler.
- 'Compost': transporting to a composting facility.
- 'Incinerate': transporting to an incinerator.

* **Type:**
  {'Landfill', 'Recycle', 'Compost', 'Incinerate'}

#### distance_cut_off

cut-off length for the waste transportation leg.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### *classmethod* from_object(material, manager, eol_pathway, transport_scenario='High')

Create.

* **Parameters:**
  * **material** ([*WasteProcess*](waste-processing.md#pod_lca.eol.WasteProcess)) -- Material keeping quantity and unit record.
  * **manager** ([*Model*](model.md#pod_lca.materials_screening.Model) *or* *Building*) -- Manager keeping the end-of-life transport datasets.
  * **eol_pathway** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

    End-of-life pathway:
    - 'Landfill': transporting waste to a landfill.
    - 'Recycle': transporting waste to a recycler.
    - 'Compost': transporting to a composting facility.
    - 'Incinerate': transporting to an incinerator.
  * **transport_scenario** ( *{'Min'* *,*  *'Average'* *,*  *'High'}*) -- Transport scenario of the transportation leg. Default is 'High'.

#### set_transport_scenario(transport_scenario: [str](https://docs.python.org/3/library/stdtypes.html#str))

Set the transport scenario of the transportation leg.

* **Parameters:**
  **transport_scenario** ( *{'Min'* *,*  *'Average'* *,*  *'High'}*) -- Transport scenario of the transportation leg.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transportation scenario not recognized.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) -- Transportation scenario is not None or a string.

#### set_eol_pathway(eol_pathway)

Set the end-of-life pathway corresponding to the waste transportation leg.

* **Parameters:**
  **eol_pathway** ( *{'Landfill'* *,*  *'Recycle'* *,*  *'Compost'* *,*  *'Incinerate'}*) -- 

  End-of-life pathway:
  - 'Landfill': transporting waste to a landfill.
  - 'Recycle': transporting waste to a recycler.
  - 'Compost': transporting to a composting facility.
  - 'Incinerate': transporting to an incinerator.

#### set_material(material)

Set the material being transported.

* **Parameters:**
  **material** ([*Product*](products-and-processes.md#pod_lca.materials_screening.Product)) -- Material name of the transportation leg.

#### set_shipping_destination(shipping_dest)

Set the shipping destination of the project.

* **Parameters:**
  **shipping_dest** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping destination location.

#### set_shipping_origin(shipping_org)

Set the shipping origin of the project.

* **Parameters:**
  **shipping_org** ([*Location*](location.md#pod_lca.location.Location)) -- Name of the shipping origin location.

#### set_mode(mode=None, efficiency=None)

Set the transportation mode of the transportation leg.

#### NOTE
1. Prefix 'E_' in the mode_name is used as the identifier of an electricity based transportation mode.
2. Electric vehicles takes electricity based on origin location.

* **Parameters:**
  * **mode** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*TransportMode*](transport-mode.md#pod_lca.transportation.TransportMode)) -- transportation mode of the transportation leg.
  * **efficiency** ( *{'High'* *,*  *'Median'* *,*  *'Low'}*) -- efficiency of the transportation mode. Default is 'Median'.

#### set_cutoff_distance()

Set the cut-off length for the waste transportation leg.

#### set_travel_dist(travel_dist=None, dist_unit=None, return_trip_factor=None)

Set the travel distance of the transportation leg.

* **Parameters:**
  * **travel_dist** (*None*) -- For DomesticLink objects travel distance are autogenerated from CFS data.
  * **dist_unit** ([*Unit*](units-object.md#pod_lca.units.Unit)) -- Unit of the travel distance.
  * **return_trip_factor** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Return trip factor of the transportation leg (default is None).

#### get_transport_scenario()

Retrieve the transport scenario of the transportation leg.

* **Returns:**
  The transport scenario of the transportation leg.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_travel_dist()

Set the travel distance of the transportation leg.

* **Returns:**
  travel distance of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float) or [str](https://docs.python.org/3/library/stdtypes.html#str)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) -- Transport scenario not recognized.

#### get_return_trip_factor()

Retrieve the return trip factor of the transportation leg.

* **Returns:**
  The return trip factor of the transportation leg.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

#### get_eol_pathway()

Get the end-of-life pathway corresponding to the waste transportation leg.

* **Returns:**
  End-of-life pathway.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_cutoff_distance()

Retrieve the cut-off length for the waste transportation leg.

* **Returns:**
  Cut-off distance
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float) or [int](https://docs.python.org/3/library/functions.html#int)

#### get_dataset()

Get the dataset.

* **Returns:**
  Dataset
* **Return type:**
  [*TransportDataset*](transport_datasets.md#pod_lca.transportation.TransportDataset)

#### get_impact_database()

Get the impact database.

* **Returns:**
  Impacts database
* **Return type:**
  [*ImpactsDatabase*](impacts-database.md#pod_lca.impacts.ImpactsDatabase)

#### get_distance_from_dataset(transport_scenario)

Get the average distance from the CFS dataset based on the scenario.

* **Parameters:**
  **scenario** ( *{'Min'* *,*  *'Average'* *,*  *'High'}*) -- The scenario to filter the distances by.
* **Returns:**
  The distance estimate for the specified scenario.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)
