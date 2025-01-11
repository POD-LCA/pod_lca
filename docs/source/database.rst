**********
Database
**********

**Database** maintains the impacts data used in the current :class:`Project <material.projectManager.Project>`.

Impact data can be imported from a CSV file where the headings correspond to *name of the impact*, *unit*, *Global Warming potential* (in :math:`kg CO_{2} eq`), *acidification potential* (in :math:`kg SO_{2} eq`), *eutrophiction potential* (in :math:`kg N eq`), *ozone depletion* (in :math:`kg CFC^{-11} eq`), *smog* (in :math:`kg O_3 eq`). If the units are not compatible with above, a multiplier can be given for each column.

.. code-block:: python

    from material import HOME
    from material.projectManager.projectManager import Project

    file_path = HOME + '\databaseManager\impact_data_new.csv'
    project = Project()
    project.get_database().import_data_from_CSV(file_path)

Custom impact data entries can also be created.

.. code-block:: python

    from material.projectManager.projectManager import Project

    project = Project()
    project.get_database().set_custom_entry("Electricity", "kWh", 
                                            {"GWP":0.503, "acid_pot":0.0036, "eutro_pot":5.83e-05, "ozone":7.6e-11, "smog":3.37e-2})

--------

.. autoclass:: material.databaseManager.DatabaseManager
    :members:
