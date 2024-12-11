**********
Impacts
**********

**Impacts** keep a record of the environmental impacts. They are created when a :class:`Product <model.product.Product>` or a :class:`Process <model.process.Process>` is created, and it belongs to them.

An impact corresponding to a product or a process can be looked up as below.

.. code-block:: python

    sand.get_impacts()

Similarly, from an impact object, its parent product or process can also be looked up

.. code-block:: python

    impact.get_parent()

All the impacts created in a :class:`model <model.model.Model>` are kept in :class:`dict` categorized by the life cycle stage. This can be 

Impact records impacts by impact categories (e.g., global warming potential, eutrophication potential). The names of categories can be set in the :class:`Database <databaseManager.databaseManager.DatabaseManager>` when the :class:`Project <projectManager.projectManager.Project>` is initialized (and before impact data imported). By default the following impact categories are set: GWP, acid_pot, eutro_pot, ozone_dep, smog.

.. autoclass:: material.impacts.Impacts
    :members: