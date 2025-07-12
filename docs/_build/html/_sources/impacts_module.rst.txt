**************
Impacts
**************

Impacts sub-package has the abstract classes of inventory records (:py:class:`~pod_lca.impacts.Records`) and databases (:py:class:`~pod_lca.impacts.ImpactsDatabase`). The inventory records of :py:class:`~pod_lca.impacts.Impacts`, :py:class:`~pod_lca.impacts.Emissions`, and :py:class:`~pod_lca.impacts.CarbonStorage` are containers for those LCA inventories. The databases of :py:class:`~pod_lca.impacts.ElectricityImpactsDatabase` and :py:class:`~pod_lca.impacts.EOLImpactsDatabase` speacialised classes to manage and retrieve inventory data for electricity and end-of-life pathways, respectively.

In addition, the :py:class:`~pod_lca.impacts.openLCA` class provides access to OpenLCA API to pre-process and retrieve data from USLCI and Ecoinvent databases.

--------

.. toctree::
   :maxdepth: 4

   impact_records
   impact_databases
   olca_pipeline
