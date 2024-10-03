from GUI.popup import Popup
from GUI.GUI_inputManager import GUIInputManager

import re
from tkinter import DISABLED, ACTIVE

class RelationshipsMixin:

    def set_relationship(self, item, slider):

        popup = Popup(self, "Set realtionship", "600x150")
        model_id = self.get_current_model()
        
        label = Popup._popup_label(popup, "Set relationship to other items on the canvas: \n e.g., {3} * 4.6 to set the qty to be always be 4.6 times that of item 3.", justify='left')
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))   
        
        txt_str = '{' + str(self.item_disp_num[model_id][item]) + '} = '
        default_str = self.relationships[model_id][item] if item in self.relationships[model_id] else ''
        relationship = Popup._popup_input_field(popup, txt_str, default_val=default_str)
        
        cmd =lambda : self.process_relationship(item, slider, relationship.get())          
        Popup.button_pack_OKCancelApply(popup, popup, cmd)

    def process_relationship(self, item, slider, relationship):
        """ Converts the relationship to an expression and assess.
            The relationship expressions are maintained in display numbers.
        """

        slider.config(state=DISABLED)
        model_name = self.get_current_model()

        masters = re.findall(r'\{ *(-?\d+(?:\.\d*)?) *\}', relationship)

        cyclicDependence = False
        if item in self.dependents[model_name]:
            for master_disp in masters:
                master_item = self.disp_num_item[model_name][int(master_disp)]
                if master_item in self.dependents[model_name][item]:
                    cyclicDependence = True
                    break
        
        if not cyclicDependence:
            self.relationships[model_name][item] = relationship
            for master_disp in masters:
                master_item_id = self.disp_num_item[model_name][int(master_disp)]
                if int(master_item_id) not in self.dependents[model_name]:
                    self.dependents[model_name][int(master_item_id)] = [item]
                else:
                    if not item in self.dependents[model_name][int(master_item_id)]:
                        self.dependents[model_name][int(master_item_id)].append(item)

                master_item = self.item_map[model_name][master_item_id]
                self.update_dependent_qtys(master_item, GUIInputManager.get_qty(master_item), is_param=False)


    def update_dependent_qtys(self, item, qty, is_param=False):

        model_id = self.get_current_model()
        item_id = item.get_id() if is_param else GUIInputManager.get_id(item)

        if item_id in self.dependents[model_id]:
            for dependent in self.dependents[model_id][item_id]:
                rel = self.relationships[model_id][dependent]
                rel_ss = re.sub(r'\s+', '', rel)
                masters = re.findall(r'\{ *(-?\d+(?:\.\d*)?) *\}', rel_ss)
                for master in masters:
                    master_item = self.item_map[model_id][item_id]
                    if GUIInputManager.is_transport(master_item):
                        qty = GUIInputManager.get_travel_distance(master_item)
                    else:
                        qty = item.get_qty() if is_param else GUIInputManager.get_qty(master_item)
 
                    tag_str = '{' + str(master) + '}'
                    rel_ss = rel_ss.replace(tag_str, str(qty))

                expression = re.sub(r'\{ *(-?\d+(?:\.\d*)?) *\}', r'\1', rel_ss)
                try:
                    calc_qty = eval(expression)
                except Exception as e:
                    f"Error evaluating expression: {e}"

                dependent_item = self.item_map[model_id][dependent]
                GUIInputManager.update_qty(self, dependent_item, calc_qty)
                slider = self.slider_map[model_id][dependent]
                slider.config(state=ACTIVE) 
                slider.set(calc_qty)
                slider.config(state=DISABLED)

    def clear_relationship(self, item):

        model_id = self.get_current_model()

        self.relationships[model_id].pop(item, None)
        for dependent in self.dependents[model_id]:
            if item in self.dependents[model_id][dependent]:
                self.dependents[model_id][dependent].remove(item)

        slider = self.slider_map[model_id][item]
        slider.config(state=ACTIVE) 


    def highlight_dependents(self, event):

        model_id = self.get_current_model()

        item = self.current_canvas.find_closest(event.x, event.y)[0]
        if item in self.dependents[model_id]:
            for dependent in self.dependents[model_id][item]:
                self.current_canvas.itemconfig(dependent, outline=self.highlight_color, width=self.highlight_width)
                self.current_canvas.current_highlight = dependent

    def remove_highight(self, event):

        if hasattr(self.current_canvas, 'current_highlight'):
            self.current_canvas.itemconfig(self.current_canvas.current_highlight, outline=self.outline_color, width=self.outline_width)

    def restore_relationships(self, item_id_history, old_dependents, old_relationships):

        new_dependents = {}
        for entry in old_dependents:
            new_dependents[item_id_history[entry]] = [item_id_history[id] for id in old_dependents[entry]]
        
        new_relationships = {}
        for entry in old_relationships:
            rel = old_relationships[entry]
            for id in old_dependents:
                old_str = '{' + str(id) + '}'
                new_str = '{' + str(item_id_history[id]) + '}'
                rel = rel.replace(old_str, new_str)
            new_relationships[item_id_history[entry]] = rel
        
        return new_dependents, new_relationships

