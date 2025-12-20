# Plots

[`Plots`](#pod_lca.visualizer.AbstractPlot) is an abstract object for plots. The following concrete class of plotters are implemented: [`BarChart`](#pod_lca.visualizer.BarChart), [`BoxPlot`](#pod_lca.visualizer.BoxPlot), [`Histogram`](#pod_lca.visualizer.Histogram), [`LinePlot`](#pod_lca.visualizer.LinePlot), [`RadarChart`](#pod_lca.visualizer.RadarChart), [`Stackplot`](#pod_lca.visualizer.Stackplot), and [`ViolinPlot`](#pod_lca.visualizer.ViolinPlot).

---

### *class* pod_lca.visualizer.AbstractPlot

An abstract class for specific implementation of graphs and charts. A plot is a set of instructions for plotting the graph.

#### plot

Plot.

* **Type:**
  [*AbstractPlot*](#pod_lca.visualizer.AbstractPlot)

#### *classmethod* from_plotter(plotter)

Create a plot from a plotter.

* **Parameters:**
  **plotter** ([*AbstractPlotter*](plotters.md#pod_lca.visualizer.AbstractPlotter)) -- Plotter.
* **Returns:**
  Plot created.
* **Return type:**
  [*AbstractPlot*](#pod_lca.visualizer.AbstractPlot)

#### *classmethod* from_plot(plot)

Create a plot from an existing plot.

* **Parameters:**
  **plot** ([*AbstractPlot*](#pod_lca.visualizer.AbstractPlot)) -- Reference plot
* **Returns:**
  Plot created.
* **Return type:**
  [*AbstractPlot*](#pod_lca.visualizer.AbstractPlot)

#### set_plot(plotter)

Set the plot.

* **Parameters:**
  **plotter** ([*AbstractPlotter*](plotters.md#pod_lca.visualizer.AbstractPlotter)) -- Plotter.

#### get_plot()

Get the plot.

* **Returns:**
  Plotter.
* **Return type:**
  [*AbstractPlot*](#pod_lca.visualizer.AbstractPlot)

#### draw()

Draw the plot.

#### show()

Display the barchart.

### *class* pod_lca.visualizer.BarChart

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Bar chart with data upto three levels: category, group, and component levels.

#### draw(data, title, x_label, y_label)

Draw the bar chart.

* **Parameters:**
  * **data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- 

    Data to be plotted, given in one of the following dictionaries:
    - standard bar chart - {**category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **value** ([`float`](https://docs.python.org/3/library/functions.html#float))};
    - grouped bar chart - {**category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : {group ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : value ([`float`](https://docs.python.org/3/library/functions.html#float))}};
    - grouped bar chart with components - {category ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : {group ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : {component ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : value ([`float`](https://docs.python.org/3/library/functions.html#float))}}}.
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.

### *class* pod_lca.visualizer.BoxPlot

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Line chart with multiple lines.

#### draw(data, title, x_label, y_label)

Draw the bar chart.

* **Parameters:**
  * **data** (*array*) -- Data in a 1D or 2D array.
    If 1D, it will be plotted as a single boxplot.
    If 2D, each column will be plotted as a separate boxplot.
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.

### *class* pod_lca.visualizer.Histogram

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Bar chart with data upto three levels: category, group, and component levels.

#### draw(data, no_bins, title, x_label, y_label, label='', color=None, unitize=True)

Draw the histogram.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of all data points.
  * **no_bins** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Number of bins in the histogram
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.

#### draw_pdf(x_data, y_data, label, title=None, x_label=None, y_label=None)

Overlay the probability distribution function on a histogram.

* **Parameters:**
  * **x_data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of x values.
  * **y_data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- f(x) for all the y values.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- label for the function plotted
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.

### *class* pod_lca.visualizer.LinePlot

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Line chart with multiple lines.

#### draw(data, title, x_label, y_label, colors=None)

Draw the line plot.

* **Parameters:**
  * **data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- 

    Data to be plotted, given in one of the following dictionaries:
    - standard line plot, in pairs - [(**x_value** ([`float`](https://docs.python.org/3/library/functions.html#float)), **y_value** ([`float`](https://docs.python.org/3/library/functions.html#float)))];
    - standard line plot, in lists - [[**x_values** ([`float`](https://docs.python.org/3/library/functions.html#float))], [**y_values** ([`float`](https://docs.python.org/3/library/functions.html#float))]]
    - multiple line plot - {**category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : [(**x_value** ([`float`](https://docs.python.org/3/library/functions.html#float)), **y_value** ([`float`](https://docs.python.org/3/library/functions.html#float)))]};
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.
  * **colors** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Colors of the line plots.

### *class* pod_lca.visualizer.RadarChart

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Bar chart with data upto three levels: category, group, and component levels.

#### set_plot(plotter)

Set the plot.

* **Parameters:**
  **plotter** ([*AbstractPlotter*](plotters.md#pod_lca.visualizer.AbstractPlotter)) -- Plotter.

#### draw(data, title)

Draw the radar chart.

* **Parameters:**
  * **data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) -- 

    Data to be plotted, given in one of the following dictionaries:
    - single radar - {**category** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **value** ([`float`](https://docs.python.org/3/library/functions.html#float))};
    - multiple_radars - {**group** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : {category ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) : **value** ([`float`](https://docs.python.org/3/library/functions.html#float))}};
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the radar plot.

### *class* pod_lca.visualizer.Stackplot

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Stackplot.

#### draw(x_data, y_data, title, x_label, y_label, colors=None)

Draw the bar chart.

* **Parameters:**
  * **x_data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* *array*) -- X data.
  * **y_data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- 

    Data to be plotted, given in one of the following dictionaries. The length of each list should match the dimensions of **x_data** list.
    - list of lists - [[y1], [y2], ... , [yn]];
    - dict - {**data label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [y1], ... , **data label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)): [yn]}
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.
  * **colors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Colors of each stack.

### *class* pod_lca.visualizer.ViolinPlot

Bases: [`AbstractPlot`](#pod_lca.visualizer.AbstractPlot)

Line chart with multiple lines.

#### draw(data, title, x_label, y_label)

Draw the bar chart.

* **Parameters:**
  * **data** (*array*) -- Data in a 1D or 2D array.
    If 1D, it will be plotted as a single boxplot.
    If 2D, each column will be plotted as a separate boxplot.
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the barchart.
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-label of the barchart.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-label of the barchart.
