**********
Visualizer
**********

**Visualizer** is where plots are created. :class:`Plotter <visualizer.plotter.Plotter>` provide the basic structur of a plot and various other visualizations are created inheriting from it (e.g., :class:`Bar chart <visualizer.bar_chart.BarChart>`).

The code segment below will create a bar chart, categorized by the life cycle stage, and indicating the gloabel warming impact (*GWP*) from *model_0*. of the project.

.. code-block:: python

    graph = BarChart(project)
    graph.set_impact_category("GWP")
    graph.set_active_models(['Model_0'])
    graph.show()

--------

.. currentmodule:: visualizer

.. autoclass:: visualizer.plotter.Plotter
   :members:

.. autoclass:: visualizer.bar_chart.BarChart
   :show-inheritance:
    