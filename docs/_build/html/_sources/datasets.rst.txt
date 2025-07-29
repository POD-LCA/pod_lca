***************************
Data Distributions
***************************

:py:class:`~pod_lca.uncertainty.DataDistribution` objects holds underlying :attr:`~pod_lca.uncertainty.DataDistribution.data` or :attr:`~pod_lca.uncertainty.DataDistribution.distribution` corresponding to an :attr:`~pod_lca.uncertainty.DataDistribution.attribute` of another :attr:`object <pod_lca.uncertainty.DataDistribution.parent>` (e.g., :py:class:`~pod_lca.materials_screening.Master`)

A selected set of distributions of known distribution parameters are available for use: :py:class:`~pod_lca.uncertainty.Uniform`, :py:class:`Normal <pod_lca.uncertainty.Norm>`, :py:class:`Log Normal <pod_lca.uncertainty.LogNorm>`, and :py:class:`Exponential Decay <pod_lca.uncertainty.ExponentDecay>`.


-----


.. autoclass:: pod_lca.uncertainty.DataDistribution
    :members:

.. autoclass:: pod_lca.uncertainty.Uniform
    :members:

.. autoclass:: pod_lca.uncertainty.Norm
    :members:

.. autoclass:: pod_lca.uncertainty.LogNorm
    :members:

.. autoclass:: pod_lca.uncertainty.ExponentDecay
    :members:
