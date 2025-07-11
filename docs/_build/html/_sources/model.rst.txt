**********
Model
**********

A material screening :py:class:`~pod_lca.materials_screening.Model` will maintain a list of :py:class:`~pod_lca.materials_screening.Product` and :py:class:`~pod_lca.materials_screening.Process` objects going into the material production. 

This also is a point to retrive the LCA output (e.g., :meth:`~pod_lca.materials_screening.Model.get_total_impact`)

-------

.. autoclass:: pod_lca.materials_screening.Model
    :members: