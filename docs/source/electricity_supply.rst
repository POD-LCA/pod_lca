**********************
Electricity Supply
**********************

:py:class:`~pod_lca.electricity.ElectricitySupply` manages the  electricity usage (supply and distribution) aspects including mix of electricity generation technologies. The grid mixes are predicted for future using the data produced by `Cambium <https://www.nrel.gov/analysis/cambium>`_ which is managed via :py:class:`~pod_lca.electricity.CambiumData` class.

--------

.. autoclass:: pod_lca.electricity.ElectricitySupply
    :members:

.. autoclass:: pod_lca.electricity.CambiumData
    :members: