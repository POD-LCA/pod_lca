************************
Data Quality Assessment
************************

:py:class:`~pod_lca.uncertainty.PedigreeScore` objects are assigned to each :py:class:`~pod_lca.materials_screening.Product` object and can be accessed from :meth:`~pod_lca.materials_screening.Master.get_pedigree_score()`.

:py:class:`~pod_lca.uncertainty.DataQualityAnalysis` object carries out the data quality assesment for a model and would return data quality scores: :meth:`~pod_lca.uncertainty.DataQualityAnalysis.get_model_DQS()` and :meth:`~pod_lca.uncertainty.DataQualityAnalysis.get_normalised_DQS()`.

-----

.. autoclass:: pod_lca.uncertainty.PedigreeScore
    :members:

.. autoclass:: pod_lca.uncertainty.DataQualityAnalysis
    :members:
