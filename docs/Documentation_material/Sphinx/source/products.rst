**********
Products
**********

**Product** is something used or created in the process. :class:`Fuel <model.product.Fuel>`, :class:`Emission <model.product.Emission>`, :class:`Waste <model.product.Waste>` are sub-types of products. They inherit attributes and methods from Product class.

In the follwing code segment, a quatity and the corresponding units are set to a product. 

.. code-block:: python

    sand = model_0.create_product("sand", "A1")
    sand.update_qty(1.0)
    sand.set_unit('kg')


Impact data can be set to the product by identifying the *name* of the corresponding entry in the database. Note that the unit of the product and the unit of the impact data should be of same dimesnions. For instance, if the product quantity is in *kg* the impact should be for any standard unit of mass (e.g., *lb*, *t*, *g*).

.. code-block:: python

    sand.set_impact_database_entry("Sand")

Density can also be set for products. Density here is defined as weight per unit of product. This is useful when the product is not typically measured in mass unit, but the transportation of the product requires knowledge of mass of the product.

.. code-block:: python

    propane = project.current_model.create_energy("Propane", "A1")
    propane.update_qty(1.0)
    propane.set_unit('MJ')
    propane.set_density(0.02)
    propane.set_weight_unit('kg')
    propane.set_impact_database_entry("Propane")

.. currentmodule:: model.product

.. autoclass:: Product
   :show-inheritance:
   :inherited-members:

.. autoclass:: Fuel
   :show-inheritance:
   :members:

.. autoclass:: Emission
   :show-inheritance:
   :members:

.. autoclass:: Waste
   :show-inheritance:
   :members: