**********
Processes
**********

**Process** is some transformation done on a product. 

Similar to a product, process quantities, units, and impact can be set for a process

.. code-block:: python

    mixing = model_0.create_prcess("mixing", "A3")
    mixing.update_qty(1.0)
    sand.set_unit('m3')
    sand.set_impact_database_entry("mixer")

:class:`Transportation <model.process.transportationProcess>` is special type of a process. The units of a transportation process is of dimensions *mass* x *length*. The mass is from the :attr:`transported weight <model.process.transportationProcess.transported_weight>` and the distance is from :attr:`transported distance <model.process.transportationProcess.transported_distance>`. The former will be automatically updated if :attr:`transported products <model.process.transportationProcess.transported_products>` are set.

.. code-block:: python
    
    propane_by_truck = project.current_model.create_transportation_process("Propane Transportation", "A2")
    propane_by_truck.set_transported_product(propane)
    propane_by_truck.set_transported_distance(20.0)
    propane_by_truck.set_transported_distance_unit('km')
    propane_by_truck.set_impact_database_entry("Transportation by truck")

.. currentmodule:: model.process

.. autoclass:: Process
   :show-inheritance:
   :inherited-members:

.. autoclass:: transportationProcess
   :show-inheritance:
   :members: