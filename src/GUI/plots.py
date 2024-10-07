from material.visualizer.bar_chart import BarChart

class PlotsMixin:

    def create_plot(self, impact_cat, plot_type='Bar_chart'):
        
        model_lst = []
        for model in self.plot_models:
            if self.plot_models[model].get():
                model_lst.append(model)
        
        if plot_type == 'Bar_chart':
            plot = BarChart(self.project)
            plot.set_active_models(model_lst)
            plot.set_impact_category(impact_cat)
            plot.draw()

        return plot
    
    def update_plot(self):

        model_lst = []
        for model in self.plot_models:
            if self.plot_models[model].get():
                model_lst.append(model)

        self.plot.set_active_models(model_lst)
        self.plot.draw()
        self.canvas_plot.draw()

    def _update_plot_from_combo(self, event):
        
        self.plot.set_impact_category(event.widget.get())
        self.update_plot()
