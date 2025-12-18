# Developer Guide

The program structure of the code base is as below. The program is structured in such a way that it is independent of the front-end and the background database.

Provide reference to utitlites settings to access config, and log methods

Procide reference to the combined class file

![Add alternative text](../_images/Program_structure.png)

The class structure if the code base is as below.

![Add alternative text](../_images/Class_diagram_overall.png)

`Product` and `Processe`  objects inherit from the `Master class`.

![Add alternative text](../_images/Class_diagram_masterObject.png)

`Plotter` provide an abstract class to create visualizations.

![Add alternative text](../_images/Class_diagram_plotters.png)

`Calculator` is the place to add new computation methods to reorganize (or work with) the impact data from the `Models`.

test_unittest file includes a series of unit-tests to verify the new additions to the code base are compatible with the existing code implementations.
