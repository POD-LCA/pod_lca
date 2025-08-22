****************
Impacts Database
****************

Impact databases manages importing (:meth:`~pod_lca.impacts.ImpactsDatabase.set_data`) and retrieval (:meth:`~pod_lca.impacts.ImpactsDatabase.get_data_entry`) of LCA data.

Specialized databases, :py:class:`~pod_lca.impacts.ElectricityImpactsDatabase`, :py:class:`~pod_lca.impacts.EOLImpactsDatabase`, and :py:class:`~pod_lca.impacts.TranportationModeImpactsDatabase`, are inherited from the base class :py:class:`~pod_lca.impacts.ImpactsDatabase` to account for additional classifiers present in those databases (e.g., `region` and `technology type` used in `ElectricityImpactsDatabase`). 

--------

.. autoclass:: pod_lca.impacts.ImpactsDatabase
    :members:

.. autoclass:: pod_lca.impacts.ElectricityImpactsDatabase
    :members:
    :show-inheritance:

.. autoclass:: pod_lca.impacts.EOLImpactsDatabase
    :members:
    :show-inheritance:

.. autoclass:: pod_lca.impacts.TranportationModeImpactsDatabase
    :members:
    :show-inheritance:
