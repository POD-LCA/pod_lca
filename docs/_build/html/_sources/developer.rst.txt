***************
Developer Guide
***************

The program structure of the code base is as below. The program is structured in such a way that it is independent of the front-end and the background database.

.. image:: ../_images/Program_structure.png
  :width: 1000
  :alt: Add alternative text

The class structure if the code base is as below.

.. image:: ../_images/Class_diagram_overall.png
  :width: 1000
  :alt: Add alternative text

:class:`Product <model.product.Product>` and :class:`Processe <model.process.Process>`  objects inherit from the :class:`Master class <model.master.Master>`. 

.. image:: ../_images/Class_diagram_masterObject.png
  :width: 1000
  :alt: Add alternative text

:class:`Plotter <visualizer.plotter.Plotter>` provide an abstract class to create visualizations.

.. image:: ../_images/Class_diagram_plotters.png
  :width: 1000
  :alt: Add alternative text

:class:`Calculator <calculator.Calculator>` is the place to add new computation methods to reorganize (or work with) the impact data from the :class:`Models <model.model.Model>`.

`test_unittest` file includes a series of unit-tests to verify the new additions to the code base are compatible with the existing code implementations.

