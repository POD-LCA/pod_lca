
from plotters.matplotlib_plotter import Plotter

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart(Plotter):
    """Bar chart to visualize impacts (of a given impact category) for multiple models by life cycle stage---i.e., a bar for life cycle stage of a given model, 
       and bars grouped by life cycle stage.
    
    """

    def set_data(self):
        """Generate bar chart data and plot it."""

        if isinstance(self.impact_category, list):
            self.impact_category = self.impact_category[0]
            print("A list of impact categories given. Graph plotted for the first category in the list.")

        gap = 0.2 # gap between two groups of bars
        stages, bar_data = self.calculator.get_barchart_data(self.impact_category, self.active_models)
        width = (1.0 - gap) / len(self.active_models)
        for model_idx, (model, stage_data) in enumerate(bar_data.items()):
            for stage_idx, (stage, value) in enumerate(stage_data.items()):
                height = self.round_to_significant([value])[0]
                color = self.plot_colors[model_idx % len(self.plot_colors)]

                rect = self.ax.bar(
                    stage_idx - (1.0 - gap - width)/2 + (model_idx * width), height, width, label=f'{stage} ({model})', color=color
                )
                self.ax.bar_label(rect, labels=self.format_labels([height]), padding=3)
        self.ax.set_xticks(range(len(stages)), stages)

    def set_labels(self):
        """Set axis labels and title."""
        unit = self.IMPACT_UNITS.get(self.impact_category, '')
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(f'{self.impact_category} Impact ({unit})')
        self.ax.set_title("Life Cycle Stages")

    def set_legend(self):
        """Set legend for the bar chart."""
        self.ax.legend(title="Models", loc="upper left", ncols=3)
