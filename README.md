# POD-LCA

Python Library developed as part of the Parametric Open Data for Life Cycle Assessment (POD|LCA) Project, by the University of Washington


## Installation Instructions

The Python Library requires Python 3.11 or above.

The Python package can be installed using pip command.

```shell
pip install pod_lca
```

The package also comes with two extras; search mode, openLCA linking. The search mode allows searching the databases and require additional dependencies for natural language processing. OpenLCA provides a pipeline to connect to the OpenLCA API for pre-processing of LCI data.

```shell
pip install pod_lca[search]
```

or

```shell
pip install pod_lca[olca]
```

or

```shell
pip install pod_lca[search, olca]
```

### Quick Start

First the project is built, setting the project location, year, and the impact databases.

```python
from pod_lca.location import Location
from pod_lca.materials_screening import Project

project = Project()

factory = Location.from_str("Seattle, Washington")
project.set_location(factory)
project.set_year(2025)
project.set_databases()
```

Then, a model is created under the project and the ingredient materials are added.

```python
from pod_lca.units import CUBIC_METER
from pod_lca.units import KILOGRAM

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(
    name="Lumber",
    stage="A1",
    qty=1.21,
    unit=CUBIC_METER,
    impacts_from="Sawn lumber; softwood; planed; kiln dried; packaged; at planer; PNW",
    sctg_code=26,
)
meth_diphenyl_d = CLT_model.add_product(
    name="Methylene diphenyl diisocyanate resin",
    stage="A1",
    qty=3.22,
    unit=KILOGRAM,
    impacts_from="Methylene diphenyl diisocyanate, MDI, at plant, US PNW",
    sctg_code=28,
)
prop_glycol = CLT_model.add_product(
    name="Propylene glycol",
    stage="A1",
    qty=2.77,
    unit=KILOGRAM,
    impacts_from="Ethylene glycol, materials production, organic compound, at plant, kg",
    sctg_code=28,
)
```

This would automatically consider the corresponding transportation of the material as well. The user can access and change the transportation settings for individual materials.

```python
lumber_transportation = CLT_model.get_transportation_manager().get_transportation_leg(lumber)
```

The electricity usage can also be added.

```python
from pod_lca.units import KILO
from pod_lca.units import WATT_HOUR

electricity = CLT_model.add_electricity(name="Electricity", 
                                        stage="A3", 
                                        qty=128.75, 
                                        unit=KILO * WATT_HOUR)
```

Now the model is built, analysis can be carried out on the model.

```python
from pod_lca.uncertainty import HotSpotAnalysis

hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category= "GWP")
print(hotspot_analysis)
```

The \examples folder provide a series of examples to explore the PoD|LCA Python package.

### Documentation

The project documentation are, including technical details on the underlying Life Cycle Analysis methods and the API reference, are available [here](https://podlca.uw.edu/pQElzwrpzCzy3tSQ2oG3) 

### Community and Contributing

LCA and Python community are welcome to make contribution to the project. See the developer guidelines [here](https://podlca.uw.edu/pQElzwrpzCzy3tSQ2oG3/python-library/developer) 

### Licensing

