**********
Model
**********

**Model** is where all the :class:`Products <model.product.Product>` and :class:`Processes <model.process.Process>` created. A :class:`Project <projectManager.projectManager.Project>` can have multiple projects enabling to use the same database for multiple scenarios and compare them. 

The current working model can be retrieved as following:

.. code-block:: python

    from material.projectManager.projectManager import Project

    project = Project()
    model_0 = project.get_current_model() 

An new model can be created as following:

.. code-block:: python

    model_1 = project.create_model("new Scenario")

:class:`Products <model.product.Product>` and :class:`Processes <model.process.Process>` can then be added to the current model. All products and processess must be asigned a life cycle stage.

.. code-block:: python

    sand = model_0.create_product("sand", "A1")
    mixing_process = model_0.create_process("mixing", "A3")
    trnasport_sand = model_0.create_transportation_process("transport_by_truck", "A2")
    electricity = model_0.create_energy("Electricity", "A3")
    CO_2 = model_0.create_emission("CO2", "A3")
    waste = model_0.create_waste("to_landfill", "A3")

**Model** will keep a full record of all :class:`Impacts <model.impacts.Impacts>` categorized by the life cycle stage. The following line of code will return a :class:`dict` where keys are the life cycle stages. 

.. code-block:: python

    impacts = model_0.get_impacts()


--------

.. autoclass:: model.model.Model
    :members: