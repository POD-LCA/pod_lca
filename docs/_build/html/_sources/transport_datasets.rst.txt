*******************
Transport Datasets
*******************

:py:class:`~pod_lca.transportation.TransportDataset` class manages datasets which are used by :py:class:`~pod_lca.transportation.TransportationLeg` objects to estimate the traved distances. Transportation datasets and their corresponding transportation datasets are as in the table below.


+-------------------------------------------------------+--------------------------------------------------------+
| Transportation Leg                                    | Dataset                                                | 
+=======================================================+========================================================+
| :py:class:`~pod_lca.transportation.DomesticLeg`       | :py:class:`~pod_lca.transportation.CFSDataset`         | 
+-------------------------------------------------------+--------------------------------------------------------+
| :py:class:`~pod_lca.transportation.ForeignLeg`        | :py:class:`~pod_lca.transportation.USGlobalDataset`    |
+-------------------------------------------------------+--------------------------------------------------------+
| :py:class:`~pod_lca.transportation.WasteTransportLeg` | :py:class:`~pod_lca.transportation.EOLTransportDataset`| 
+-------------------------------------------------------+--------------------------------------------------------+

------

.. autoclass:: pod_lca.transportation.TransportDataset
    :members:

.. autoclass:: pod_lca.transportation.CFSDataset
    :members:

.. autoclass:: pod_lca.transportation.USGlobalDataset
    :members:

.. autoclass:: pod_lca.transportation.EOLTransportDataset
    :members:
