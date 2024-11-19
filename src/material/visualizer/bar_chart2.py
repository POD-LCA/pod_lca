from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt
import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class BarChart2(Plotter):
    """Stacked bar chart to visualize impacts for multiple models by life cycle stage."""

    def set_data(self):
        """Generate stacked bar chart data and plot it."""
        stages = ['A1', 'A2', 'A3']
        stage_indices = np.arange(len(stages))
        width = 0.4

        for model_idx, model in enumerate(self.active_models):
            bottom = np.zeros(len(stages))
            _, _, _, impacts = self.calculator.get_barchart2_data(self.impact_category, model)

            for stage, impact in impacts.items():
                heights = self.round_to_significant(impact)
                color = self.plot_colors[model_idx % len(self.plot_colors)]

                rect = self.ax.bar(
                    stage_indices + model_idx * width, heights, width, label=stage, bottom=bottom, color=color
                )
                bottom += heights
                self.ax.bar_label(rect, labels=self.format_labels(heights), label_type="center")

        self.ax.set_xticks(stage_indices, stages)

    def set_labels(self):
        """Set axis labels and title."""
        unit = self.IMPACT_UNITS.get(self.impact_category, '')
        self.ax.set_xlabel("Life Cycle Stage")
        self.ax.set_ylabel(f'{self.impact_category} Impact ({unit})')
        self.ax.set_title("Life Cycle Stages")

    def set_legend(self):
        """Set legend for the stacked bar chart."""
        self.ax.legend(title="Stages", loc="upper left", ncols=3)
