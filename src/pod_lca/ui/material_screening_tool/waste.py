from ui.materials_screening_tool.GUI_inputManager import GUIInputManager
from ui.materials_screening_tool.popup import Popup
from ui.materials_screening_tool.product import Product

from numpy import ceil, power, log10


class WasteProduct(Product):

    # =================================
    # Product Items
    # =================================

    def open_popup_waste(self):

        popup = Popup(self, "Create waste product", "300x225")

        name = Popup._popup_input_field(popup, "Waste name: ", default_val="Waste 01")
        lca_data = Popup._popup_input_combo(
            popup, "LCA data: ", [None] + GUIInputManager.get_database_data(self.project)["Flow"].tolist()
        )
        life_cycle_stage = Popup._popup_input_combo(popup, "Life cycle stage: ", ["A1", "A2", "A3"], default_entry=2)
        qty = Popup._popup_input_field(popup, "qty: ", validate_num=True, default_val=0.0)
        units = Popup._popup_input_combo(popup, "units: ", ["kg", "lb", "g"])

        cmd = lambda: self.create_waste_product(
            popup, name.get(), qty.get(), units.get(), life_cycle_stage.get(), lca_data.get()
        )
        Popup.button_pack_OKCancel(popup, popup, cmd)

        self.wait_window(popup)
        self.update_plot()

    def create_waste_product(self, popup, name, qty, unit, stage, lca_data):

        model_id = self.get_current_model()

        product = GUIInputManager.create_waste(self.project, model_id, name, unit, float(qty), stage, lca_data)

        if not product is None:
            slider_min = 0.0
            slider_max = power(10, ceil(log10(abs(float(qty))))) if float(qty) != 0 else 10.0
            resolution = (slider_max - slider_min) / 100

            item_id, text_item, text_id = WasteProduct.create_canvas_item(
                self, model_id, name, stage, qty, unit, self.color_waste, tags=["product", "waste"]
            )
            slider_cmd = lambda x: WasteProduct.update_qty(self, item_id, x)
            slider, slider_data = WasteProduct.create_slider(
                self, model_id, qty, unit, item_id, slider_cmd, slider_min, slider_max, resolution
            )
            WasteProduct.item_bind(self, item_id, text_item, text_id, slider, slider_data)

            GUIInputManager.set_id(product, item_id)
            self.item_map[model_id][item_id] = product

            self.update_plot()
            if self.hotspot_on_off.get():
                self.show_hotspots()

            if not popup is None:
                popup.destroy()

            return item_id

        else:
            return None
