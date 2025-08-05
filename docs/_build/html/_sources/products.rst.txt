*******************
Products/Processes
*******************

:py:class:`~pod_lca.materials_screening.Product` and :py:class:`~pod_lca.materials_screening.Process` objects keeps track of product/process quantities and their LCA data (e.g., :py:class:`~pod_lca.impacts.Impacts`, :py:class:`~pod_lca.impacts.Emissions`). They both inherit from the abstract class :py:class:`~pod_lca.materials_screening.Master`.

Furthermore, they keep track of advanced analysis options such as :attr:`~pod_lca.materials_screening.Master.is_hotspot`, :attr:`~pod_lca.materials_screening.Master.data_distribution` and :attr:`~pod_lca.materials_screening.Master.pedigree_score`.

:py:class:`~pod_lca.materials_screening.Product` object keep track of its electricity usage (if the database provides data disagregated for electricity consumption), allowing swapping out of electricity based on project location (:meth:`~pod_lca.materials_screening.Product.set_electricity_source`).

-------

.. autoclass:: pod_lca.materials_screening.Master
   :show-inheritance:
   :members:
   :inherited-members:

.. autoclass:: pod_lca.materials_screening.Product
   :show-inheritance:
   :members:
   
.. autoclass:: pod_lca.materials_screening.Electricity
   :show-inheritance:
   :members:

.. autoclass:: pod_lca.materials_screening.Fuel
   :show-inheritance:
   :members:

.. autoclass:: pod_lca.materials_screening.Process
   :show-inheritance:
   :members:
   