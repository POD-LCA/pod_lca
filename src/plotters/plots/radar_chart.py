from plotters.plots.abstract_plot import AbstractPlot
from plotters.plots.colour_palettes import COLOUR_PALETTES, COLOUR_ORDER_LIST

from numpy import linspace, pi


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu; kiun@uw.edu"
__version__ = "0.1.0"


class RadarChart(AbstractPlot):
    """Bar chart with data upto three levels: category, group, and component levels.
    """
    def __init__(self):
        super().__init__()

    # ================================
    # Setters and Getters
    # ================================  
    def set_plot_from_plotter(self, plotter):
        """ Set the plot.
        
            Parameters
            ----------
            plotter : AbstractPlotter Obj.
                Plotter.        
        """
        self.plot = plotter.create_plot(polar=True)

        return self

    # ================================
    # Methods
    # ================================ 
    def draw(self, data, title):
        """ Draw the radar chart.
        
            Parameters
            ----------
            data : dict
                Data to be plotted, given in one of the following dictionaries:
                single radar - {category (str) : value (float)};
                multiple_radars - {group (str) : {category (str) : value (float)}};
            title : str
                Title of the radar plot.
        """
        COLOUR_BASE = 2
        
        self.get_plot().clear_plot()

        counter = 0
        for key, group in data.items(): 
            if isinstance(group, float):
                num_spokes = len(data)
                angles = linspace(0, 2 * pi, num_spokes, endpoint=False).tolist()
                angles += angles[:1]

                values = [value for value in data.values()]
                values += values[:1] 

                self.get_plot().draw_radar(angles, values, key, color=COLOUR_PALETTES[COLOUR_ORDER_LIST[counter]][COLOUR_BASE], alpha=0.25)
                break
            elif isinstance(group, dict):
                num_spokes = len(data[list(data.keys())[0]])
                angles = linspace(0, 2 * pi, num_spokes, endpoint=False).tolist()
                angles += angles[:1]

                values = [group[item] for item in group.keys()]
                values += values[:1] 
            
                self.get_plot().draw_radar(angles, values, key, color=COLOUR_PALETTES[COLOUR_ORDER_LIST[counter]][COLOUR_BASE], alpha=0.25)
                counter += 1
            else:
                raise NotImplementedError

        self.get_plot().set_title(title)
        self.get_plot().set_grid()

        if isinstance(group, float):
            self.get_plot().set_xticks(angles[:-1], list(data.keys()))
        elif isinstance(group, dict):
            self.get_plot().set_xticks(angles[:-1], list(group.keys()))
            self.get_plot().set_legend()
        else:
            raise NotImplementedError

if __name__ == '__main__':
    pass