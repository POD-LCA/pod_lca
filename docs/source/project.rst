**********
Project
**********

A material screening :py:class:`~pod_lca.materials_screening.Project` maintain the project metadata (e.g., year, :py:class:`~pod_lca.location.Location`), :py:class:`~pod_lca.impacts.ImpactsDatabase`, and the alternative :py:class:`~pod_lca.materials_screening.Model` objects. 

This also is a point to retrive the LCA output (e.g., :meth:`~pod_lca.materials_screening.Project.get_impacts_by_category_models`)

-------

.. autoclass:: pod_lca.materials_screening.Project
    :members:
