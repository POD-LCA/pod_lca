**********************
Transportation
**********************

This sub-package handles transportation. :py:class:`~pod_lca.transportation.TransportationManager` class provides a means of managing a logistics operation (i.e., transportation of multiple :py:class:`~pod_lca.materials_screening.Product` objects). :py:class:`~pod_lca.transportation.TransportationLeg` manages individual leg of transportation, including the travel distance, and :py:class:`~pod_lca.transportation.TransportMode` class manages various aspects of transportation modes, including their :py:class:`~pod_lca.impacts.Impacts` and :py:class:`~pod_lca.impacts.Emissions`. 

-------

.. toctree::
   :maxdepth: 3

   project-logistics-manager
   logistics-leg
   transport-mode
   transport_datasets
