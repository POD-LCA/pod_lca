from material.visualizer.plotter import Plotter

import matplotlib.pyplot as plt

class BarChart(Plotter):
        
    def __init__(self, project):
        super().__init__(project)

    def set_data(self):
        
        bar_x, bar_height = self.calculator.get_barchart_data(self.impact_category, self.model)
        self.ax.bar(bar_x, bar_height, label=list(bar_x), color=self.bar_colors)

    def set_labels(self): 
        
        self.ax.set_ylabel(f'{self.impact_category} Impact')
        self.ax.set_title('Life cycle stages')
        self.ax.legend(title='Life cycle stage color')

if __name__ == '__main__':
    pass
