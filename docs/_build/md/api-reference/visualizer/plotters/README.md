# Plotters

[`Plotter`](#pod_lca.visualizer.AbstractPlotter) is an abstract object for plots. [`MatplotlibPlotter`](#pod_lca.visualizer.MatplotlibPlotter) is a concrete implementation of a Plotter.

---

### *class* pod_lca.visualizer.AbstractPlotter

A plotter provides a means of drawing and displaying plots (graphs, charts. etc.).

#### *classmethod* create_plot()

Creates a new plot.

#### clear_plot()

Clear the plot.

#### show()

Display the plot.

#### draw_bar(pos, height, width, bottom=0.0, label='', label_type='center')

draw a bar in a bar chart.

#### set_title(title)

Set title of the plot.

#### set_labels(x_label, y_label)

Set axis labels of the plot.

#### set_legend()

Set the legend of the plot.

#### set_xlim(min, max)

Set limits of the x-axis of the plot.

#### set_ylim(min, max)

Set limits of the y-axis of the plot.

#### set_xticks(tick, labels)

Set and label ticks along the x-axis of the plot.

#### set_yticks(tick, labels)

Set and label ticks along the y-axis of the plot.

#### set_grid()

Set grid lines of the plot.

### *class* pod_lca.visualizer.MatplotlibPlotter

Bases: [`AbstractPlotter`](#pod_lca.visualizer.AbstractPlotter)

A plotter implemented from Matplotlib package.

#### fig

Figure being plotted.

* **Type:**
  [matplotlib.figure.Figure](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure)

#### ax

Axes of the figure being plotted.

* **Type:**
  [matplotlib.axes.Axes](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes)

#### *classmethod* create_plot(polar=False)

Creates a new matplotlib plot.

* **Parameters:**
  **Polar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, create a plot with polar axis.

#### clear_plot()

Clear the plot

#### show()

Display the plot.

#### draw_bar(pos, height, width, bottom=0.0, color='blue', label=None, label_pos='center')

draw a bar in a bar chart.

* **Parameters:**
  * **pos** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Position (center) of the bar on the x-axis.
  * **height** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Height of the bar.
  * **width** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Width of the bar.
  * **bottom** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Position (bottom) of the bar on y-axis.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Labeling of the bar.
  * **label_pos** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Label position on the bar.

#### draw_radar(angles, values, label, color, alpha=0.5)

Draw radar lines in a polar plot.

* **Parameters:**
  * **angles** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of angles for the radar lines.
  * **values** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of values to be marked in each radar line.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Label for the radar created.
  * **color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Color of the radar plot as a named or hex string.
  * **alpha** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transparency of the radar (value between 0 and 1).

#### draw_histogram(data, no_bins, label, color, alpha, unitize)

Draw a histogram.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of all data points.
  * **no_bins** ([*int*](https://docs.python.org/3/library/functions.html#int)) -- Number of bins in the histogram
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Identifier of the histogram.
  * **color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Color of the radar plot as a named or hex string.
  * **alpha** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Transparency of the radar (value between 0 and 1).
  * **unitize** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) -- If true, the area under of the histogram is set to 1.

#### draw_line(x_data, y_data, label, color=None)

Draw a line plot through (x, y) data pairs.

* **Parameters:**
  * **x_data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of x values.
  * **y_data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- f(x) for all the y values.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- label for the function plotted
  * **color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Color of the radar plot as a named or hex string.

#### draw_stackplot(x_data, y_data, labels, colors=None)

Draw a stackplot.

* **Parameters:**
  * **x_data** (*array-like*) -- X data; shape (N,)
  * **y_data** (*array-like*) -- Y data; shape(M, N)
  * **labels** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Labels for y data series.
  * **colors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *of* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *tuples*) -- Colors of named, hex string, or RGB tuples.

#### draw_boxplot(data)

Draw a boxplot.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of all data points.
  * **color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Color of the radar plot as a named or hex string.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Identifier of the histogram.

#### draw_violinplot(data)

Draw a violinplot.

* **Parameters:**
  * **data** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of all data points.
  * **color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Color of the radar plot as a named or hex string.
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Identifier of the histogram.

#### set_title(title)

Set title of the plot.

* **Parameters:**
  **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the plot.

#### set_labels(x_label='', y_label='')

Set plot title and axis labels.

* **Parameters:**
  * **x_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- X-axis label.
  * **y_label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Y-axis label.

#### set_legend(colors=None, labels=None, title=None)

Set the legend of the plot. If colors and labels are given, override with patches.

* **Parameters:**
  * **colors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of colors, if patches are being used.
  * **labels** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- List of labels, if patches are being used.
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) -- Title of the legend.
* **Raises:**
  [**IndexError**](https://docs.python.org/3/library/exceptions.html#IndexError) -- Number of colors and labels does not match.

#### set_xticks(ticks, labels=None)

Set and label ticks along the x-axis of the plot.

* **Parameters:**
  * **ticks** (*1D array-like*) -- List of x values where ticks to be added.
  * **labels** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) -- List of labels for the ticks.

#### set_xlim(min, max)

Set limits of the x-axis of the plot.

* **Parameters:**
  * **min** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Minimum value on x-axis.
  * **max** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Maximum value on x-axis.

#### set_ylim(min, max)

Set limits of the y-axis of the plot.

* **Parameters:**
  * **min** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Minimum value on y-axis.
  * **max** ([*float*](https://docs.python.org/3/library/functions.html#float)) -- Maximum value on y-axis.

#### set_grid()

Set grid lines of the plot.
