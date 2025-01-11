.. _section-Hotspot:

****************
Hotspot Analysis
****************

Hotspot analysis identifies the set of :class:`Products <model.product.Product>` and :class:`Processes <model.process.Process>` in the :class:`Model <model.model.Model>` which are;

* the top 20% contributors to a specified impact; and
* accounts for the top 80% of the total of the specified impact.

The analysis can by running the :py:func:`calculator.calculator.Calculator.hot_spot_analysis`.

.. code-block:: python

    hot_spots = project.get_calculator().hot_spot_analysis(model='Model_0', impact_category="GWP", printout=True)

The result for the Smoothie example would be as following:

.. code-block:: console

    **************************************************
    HOTSPOTS
    **************************************************
    Object(name=Electricity for Chemical Reaction, LC stage=A3) Impact (GWP): 90.0
    Object(name=Pickles, LC stage=A1) Impact (GWP): 24.0
    Object(name=Sprinkles, LC stage=A1) Impact (GWP): 20.0
    Object(name=NH3, LC stage=A3) Impact (GWP): 4.8999999999999995

