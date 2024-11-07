from GUI.GUI_inputManager import GUIInputManager
from GUI.GUI_outputManager import GUIOutputManager

from math import log10, floor


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
        
        # TODO: Changed with new impact category abbreviations (replace impact_cat with self.hotspot_impact_cat.get())
        impact_convert = {'GWP': 'GWP', 'EP': 'eutro_pot', 'SFP': 'smog', 'AP': 'acid_pot', 'ODP':'ozone'}
        impact_cat = impact_convert[self.hotspot_impact_cat.get()]

        hot_spots = GUIOutputManager.get_hotspots(self.project, self.get_current_model(), impact_category=impact_cat)
        if hot_spots is not None:
            max_impact = 0.0
            for hotspot in hot_spots:
                max_impact = max(GUIInputManager.get_impact_val(hotspot, impact_cat), max_impact) 

            for spot in hot_spots:
                item_id = spot.get_id()
                self.current_canvas.itemconfig(item_id, outline=self.hotspot_color, width=self.hotspot_width)
                self.slider_map[self.get_current_model()][item_id]._never_show = False
                self.show_impact_bubble(item_id, impact_cat, max_impact)
                self.current_canvas.current_hotspot.append(item_id)


    def show_impact_bubble(self, item_id, impact_category, max_impact, k=0.5):

        model_id = self.get_current_model()
        product = self.item_map[model_id][item_id]

        impact = GUIInputManager.get_impact_val(product, impact_category)
        if max_impact < 1.0:
            pwr10 = abs(floor(log10(abs(max_impact))))
            impact_str = str(round(impact * 10 ** pwr10))
        else:
            impact_str = str(round(impact))

        coords = self.current_canvas.coords(item_id)
        radius = self.impact_bubble_radius * self.scale[model_id] * (1 + impact / max_impact) * k
        x0, y0 = coords[2] - radius, coords[1] + radius
        x1, y1 = coords[2] + radius, coords[1] - radius

        oval = self.current_canvas.create_oval(x0, y0, x1, y1, outline="black", fill="red", width=2, tag='impact_bubble')
        label = self.current_canvas.create_text(coords[2], coords[1], text=impact_str, anchor='center', tag='impact_bubble')
        
        group_tag = f"group_{item_id}"
        self.current_canvas.addtag_withtag(group_tag, oval)
        self.current_canvas.addtag_withtag(group_tag, label)
