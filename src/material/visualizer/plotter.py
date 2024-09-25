import matplotlib.pyplot as plt

class Plotter:

    def __init__(self, project):
        self.calculator = project.get_calculator()
        plt.close('all')
        self.fig, self.ax = plt.subplots()

        self.impact_category = None
        self.model = 'Model_0'

        self.bar_colors = ['tab:red', 'tab:blue', 'tab:orange']

    def set_impact_category(self, impact_cat):

        self.impact_category = impact_cat

    def set_data(self):
        """ Calls calculator to generate the data and then sets them in the plot.
        """
        pass

    def set_labels(self):
        pass

    def plot(self):
        pass

    def show(self):
        
        self.set_data()
        self.set_labels()

        plt.show()

if __name__ == '__main__':
   pass
  