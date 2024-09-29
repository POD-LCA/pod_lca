**********
Project
**********

.. automodule:: projectManager.projectManager

**Project** class is used to create *Project* in two-dimensional space, 
.. with uniform thickness in the third dimension. *Block* :py:func:`~Builder2D.buildBlock` is the basic level of construction. This adds a *face* to the **Datastructure** (:py:attr:`Structure.continuum`) and a *part* to **Composite** (:py:attr:`Structure.assembly`).

.. In ths *structure* level, **Builder2D** class can build;

.. (i) a wall :py:func:`~Builder2D.buildWall`
.. (ii) a flat arch :py:func:`~Builder2D.buildFlatArch`
.. (iii) a cicrular arch :py:func:`~Builder2D.buildArch`
.. (iv) a multi ring arch :py:func:`~Builder2D.buildArchMultRing`

.. Combinations of above can be used to build complex **Structures**.

.. .. code-block:: python

..     Fascade = Structure()

..     Fascade, _ = Builder2D.buildWall(Fascade, layers=3, bricks=3, brick_length=0.225, brick_height=0.075, origin=(-0.9, -0.075), startLayer=0)
..     Fascade, _ = Builder2D.buildWall(Fascade, layers=3, bricks=3, brick_length=0.225, brick_height=0.075, origin=(0.9, -0.075), startLayer=0)
..     Fascade, _ = Builder2D.buildWall(Fascade, layers=8, bricks=4, brick_length=0.225, brick_height=0.075, origin=(0.675, -0.675), startLayer=0)
..     Fascade, _ = Builder2D.buildWall(Fascade, layers=8, bricks=4, brick_length=0.225, brick_height=0.075, origin=(-0.9, -0.675), startLayer=0)
..     Fascade, _ = Builder2D.buildWall(Fascade, layers=5, bricks=11, brick_length=0.225, brick_height=0.075, origin=(-0.9, -1.050), startLayer=1)
..     Fascade, _ = Builder2D.buildWall(Fascade, layers=5, bricks=11, brick_length=0.225, brick_height=0.075, origin=(-0.9, 0.150), startLayer=1)
..     Fascade, span = Builder2D.buildFlatArch(Fascade, blocks=9, block_width=0.075, block_height=0.15, incline=1.3, baseW=0.225, baseH=0.075, origin=(0.3375, 0.))


.. In a level between the *block*  and the *structure*, **Builder2D** class have *brick* methods, which are helper classes in building structures. The two *brick* methods are;

.. (i) a brick given its *length* and *height* :py:func:`~Builder2D.buildBrick`
.. (ii) an arc brick :py:func:`~Builder2D.buildArcBrick`.

--------

.. autoclass:: Project
    :members:
