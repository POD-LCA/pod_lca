__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"

from numpy import arange

from ...utilities import config
from ...utilities import MathFuncs
from ...visualizer import AbstractPlot


class BarChart(AbstractPlot):
    """Bar chart with data upto three levels: category, group, and component levels."""

    def __init__(self):
        super().__init__()

    # ================================
    # Methods
    # ================================
    def draw(self, data, title, x_label, y_label, graph_type='simple'):
        """Draw the bar chart.

        Parameters
        ----------
        data : dict
            Data to be plotted, given in one of the following dictionaries: \n
            - standard bar chart - {**category** (:class:`str`) : **value** (:class:`float`)};
            - grouped/stacked bar chart - {**category** (:class:`str`) : {group (:class:`str`) : value (:class:`float`)}};
            # - grouped bar chart with components - {category (:class:`str`) : {group (:class:`str`) : {component (:class:`str`) : value (:class:`float`)}}}. #TODO: to be implemented
        title : str
            Title of the barchart.
        x_label : str
            X-label of the barchart.
        y_label : str
            Y-label of the barchart.
        graph_type: {'simple', 'grouped', 'stacked'}
            The type of graph.
        """
        match graph_type:
            case 'simple':
                self.draw_simple_bar(data, title, x_label, y_label)
            case 'grouped':
                self.draw_grouped_bar(data, title, x_label, y_label)
            case 'stacked':
                self.draw_stacked_bar(data, title, x_label, y_label)
            case _:
                raise ValueError("graph type not recognzed.")

    def draw_simple_bar(self, data, title, x_label, y_label):

        self.get_plot().clear_plot()

        categories = list(data.keys())
        x = arange(len(categories))
        width = 0.8

        color_lst = BarChart.get_color_list()

        for i, (category, value) in enumerate(data.items()):

            height = MathFuncs.round_to_significant([value])[0]

            self.get_plot().draw_bar(
                x[i],
                height,
                width,
                label=category,
                color=color_lst[i],
                label_pos="center",
            )

        self.get_plot().set_xticks(range(len(categories)), categories)
        self.get_plot().set_legend(title=x_label)
        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()

    def draw_grouped_bar(self, data, title, x_label, y_label):

        self.get_plot().clear_plot()

        categories = list(data.keys())
        groups = list(next(iter(data.values())).keys())

        x = arange(len(groups))

        gap = 0.2
        width = (1.0 - gap) / len(categories)

        color_lst = BarChart.get_color_list()

        for i, (category, category_data) in enumerate(data.items()):

            for j, group in enumerate(groups):

                pos = (
                    x[j]
                    - ((len(categories) - 1) * width / 2)
                    + i * width
                )

                height = MathFuncs.round_to_significant(
                    [category_data[group]]
                )[0]

                self.get_plot().draw_bar(
                    pos,
                    height,
                    width,
                    color=color_lst[i],
                    label=None,
                    label_pos="center",
                )

        self.get_plot().set_xticks(range(len(groups)), groups)

        colors = [color_lst[i] for i in range(len(categories))]
        self.get_plot().set_legend(colors, categories)

        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()

    def draw_stacked_bar(self, data, title, x_label, y_label):
        # clean data
        data = {
            k: v if isinstance(v, dict) else {k: v}
            for k, v in data.items()
        }

        self.get_plot().clear_plot()

        COLOUR_PALETTES = config["Preferences"]["COLOUR_PALETTES"]
        COLOUR_ORDER_LIST = config["Preferences"]["COLOUR_ORDER_LIST"]

        categories = list(data.keys())

        x = arange(len(categories))
        width = 0.8

        colour_map = {}
        colour_counter = 0

        legend_components = set()

        for i, (category, components) in enumerate(data.items()):

            positive_bottom = 0
            negative_bottom = 0

            for component_name, value in components.items():

                # Assign a colour to this component if not already assigned
                if component_name not in colour_map:
                    palette = COLOUR_PALETTES[
                        COLOUR_ORDER_LIST[colour_counter % len(COLOUR_ORDER_LIST)]
                    ]

                    colour_map[component_name] = palette[
                        len(colour_map) % len(palette)
                    ]

                height = MathFuncs.round_to_significant([value])[0]

                if height >= 0:
                    bottom = positive_bottom
                    positive_bottom += height
                else:
                    bottom = negative_bottom
                    negative_bottom += height

                label = (
                    component_name
                    if component_name not in legend_components
                    else None
                )

                self.get_plot().draw_bar(
                    x[i],
                    height,
                    width,
                    bottom=bottom,
                    label=label,
                    color=colour_map[component_name],
                    label_pos="center",
                )

                legend_components.add(component_name)

        self.get_plot().set_xticks(range(len(categories)), categories)
        self.get_plot().set_legend(title=x_label)

        self.get_plot().set_title(title)
        self.get_plot().set_labels(x_label, y_label)
        self.get_plot().set_grid()

    @staticmethod
    def get_color_list():
        COLOUR_BASE = config["Preferences"]["COLOUR_BASE"]
        COLOUR_PALETTES = config["Preferences"]["COLOUR_PALETTES"]
        COLOUR_ORDER_LIST = config["Preferences"]["COLOUR_ORDER_LIST"]
    
        flat_list = []
        
        # First Pass: base colors
        for key in COLOUR_ORDER_LIST:
            flat_list.append(COLOUR_PALETTES[key][COLOUR_BASE])
        
        # Second Pass: all other colors
        for key in COLOUR_ORDER_LIST:
            current_group = COLOUR_PALETTES[key]
            for i, hex_code in enumerate(current_group):
                if i != COLOUR_BASE:
                    flat_list.append(hex_code)
                    
        return flat_list
    

if __name__ == "__main__":
    pass
