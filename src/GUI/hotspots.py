from GUI.GUI_inputManager import GUIInputManager

class HotspotMixins:

    def clear_hotspots(self):

        if hasattr(self.current_canvas, 'current_hotspot'):
            for item_id in self.current_canvas.current_hotspot:
                self.current_canvas.itemconfig(item_id, outline=self.outline_color, width=self.outline_width)
                self.slider_map[self.get_current_model()][item_id]._never_show = True

        items_with_tag = self.current_canvas.find_withtag('impact_bubble')
        for item in items_with_tag:
            self.current_canvas.delete(item)

        self.current_canvas.current_hotspot = []    

    def show_hotspots(self):

        self.clear_hotspots()

        hot_spots =  self.project.get_calculator().hot_spot_analysis(model=self.get_current_model(), printout=False)

        if hot_spots is not None:

            max_GWP = 0.0
            for hotspot in hot_spots:
                max_GWP = max(round(GUIInputManager.get_impacts(hotspot).GWP),max_GWP) 

            for spot in hot_spots:
                item_id = spot.get_id()
                self.current_canvas.itemconfig(item_id, outline=self.hotspot_color, width=self.hotspot_width)
                self.slider_map[self.get_current_model()][item_id]._never_show = False
                self.show_impact_bubble(item_id, max_GWP)
                self.current_canvas.current_hotspot.append(item_id)


    def show_impact_bubble(self, item_id, max_GWP, k=0.5):

        model_id = self.get_current_model()
        product = self.item_map[model_id][item_id]
        impact_GWP = round(GUIInputManager.get_impacts(product).GWP)

        coords = self.current_canvas.coords(item_id)
        radius = self.impact_bubble_radius * self.scale[model_id] * (1 + impact_GWP / max_GWP) * k
        x0, y0 = coords[2] - radius, coords[1] + radius
        x1, y1 = coords[2] + radius, coords[1] - radius

        oval = self.current_canvas.create_oval(x0, y0, x1, y1, outline="black", fill="red", width=2, tag='impact_bubble')
        label = self.current_canvas.create_text(coords[2], coords[1], text=str(impact_GWP), anchor='center', tag='impact_bubble')
        
        group_tag = f"group_{item_id}"
        self.current_canvas.addtag_withtag(group_tag, oval)
        self.current_canvas.addtag_withtag(group_tag, label)
