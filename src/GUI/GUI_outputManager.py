

class GUIOutputManager():

    @staticmethod
    def get_output_data(project, impact_categories, model):

        data = {}
        for impact in impact_categories:
            data[impact] = project.get_calculator().get_data_by_LCstage(impact_category=impact, model_name=model)
        
        return data
    
    @staticmethod
    def show_hotspots(GUI):

        hot_spots =  GUI.project.get_calculator().hot_spot_analysis(model=GUI.get_current_model(), printout=False)

        if hot_spots is not None:

            if hasattr(GUI.current_canvas, 'current_hotspot'):
                for item_id in GUI.current_canvas.current_hotspot:
                    GUI.current_canvas.itemconfig(item_id, outline=GUI.outline_color, width=GUI.outline_width)
            GUI.current_canvas.current_hotspot = []      

            for spot in hot_spots:
                item_id = spot.get_id()
                GUI.current_canvas.itemconfig(item_id, outline=GUI.hotspot_color, width=GUI.hotspot_width)
                GUI.current_canvas.current_hotspot.append(item_id)
