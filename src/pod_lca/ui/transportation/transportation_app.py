import streamlit as st
import pandas as pd
from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager
from lca_modules.transportation.logistics_link import Link
import matplotlib.pyplot as plt

# Initialize Session State for Links and Impacts
if "transport_links" not in st.session_state:
    st.session_state["transport_links"] = []

if "impacts" not in st.session_state:
    st.session_state["impacts"] = []

# Initialize the ProjectLogisticManager
data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"


# Streamlit App Title
st.image(
    r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\PODLCA logo - transparent.png", use_column_width=False, width=100
)
st.title("Transportation Environmental Impact Calculator")

# Sidebar for Adding and Editing Transportation Links
with st.sidebar:
    st.header("Manage Transportation Links")

    tab_selection = st.radio("Choose Action", ["Add Link", "Edit Link"])

    if tab_selection == "Add Link":
        st.subheader("Add Transportation Details")
        shipping_dest = st.text_input("Shipping Destination:", None)
        shipping_org = st.text_input("Shipping Origin:", None)
        material = st.text_input("Material (e.g., Steel, Concrete):", "Steel")
        qty = st.number_input("Quantity (tonnes):", min_value=0.0, value=1000.0)
        travel_dist = st.number_input("Travel Distance:", min_value=0.0, value=200.0)
        scenario = st.selectbox(
            "Transportation scenario:", [None, "Local", "Regional", "Regional_c", "National", "NA", "Global"]
        )
        return_trip_factor = st.number_input("Return Trip Factor:", min_value=1.0, value=2.0)
        dist_unit = st.selectbox("Distance Unit:", ["km", "Ml"])
        mode_name = st.selectbox("Transportation mode_name:", [None, "Truck", "Rail", "Water", "Air"])
        efficiency = st.slider("efficiencyiciency Factor (1-3):", min_value=1, max_value=3, value=2)
        st.subheader("Additional Details for NA and Global Scenarios")
        mode_dms_name = st.selectbox("Transportation mode_name for DMS:", [None, "Truck", "Rail", "Water", "Air"])
        efficiency_dms = st.slider("efficiencyiciency Factor for DMS (1-3):", min_value=1, max_value=3, value=2)

        if st.button("Add Link"):

            project = ProjectLogisticManager(
                name="Building A", shipping_dest=shipping_dest, data_folder=data_folder, shipping_org=shipping_org
            )
            # Get coordinates for shipping origin and destination

            if shipping_dest:
                try:
                    origin_coordinates = project.get_shipping_org().get_cordinates()
                    dest_coordinates = project.get_shipping_dest().get_cordinates()
                except AttributeError:
                    st.error("Unable to fetch coordinates. Please check your inputs.")
                    origin_coordinates, dest_coordinates = (None, None), (None, None)

                # Prepare location DataFrame
                location_data = []
                if origin_coordinates and dest_coordinates:
                    # Determine size based on the scenario
                    scenario_sizes = {
                        "Local": 10000,
                        "Regional": 2,
                        "Regional_c": 3,
                        "National": 4,
                        "NA": 5,
                        "Global": 6,
                    }
                    size_origin = scenario_sizes.get(scenario, 3 if scenario else 5)  # Default to 3 if scenario is None
                    size_dest = size_origin if not scenario else size_origin + 1

                    location_data.append(
                        {"latitude": origin_coordinates[0], "longitude": origin_coordinates[1], "size": size_origin}
                    )
                    location_data.append(
                        {"latitude": dest_coordinates[0], "longitude": dest_coordinates[1], "size": size_dest}
                    )

                location_df = pd.DataFrame(location_data)

            if scenario:
                travel_dist = scenario
            else:
                travel_dist = travel_dist
            project.create_link(
                material=material,
                qty=qty,
                travel_dist=travel_dist,
                return_trip_factor=return_trip_factor,
                dist_unit=dist_unit,
                mode_name=mode_name,
                mode_dms_name=mode_dms_name,
                efficiency=efficiency,
                efficiency_dms=efficiency_dms,
            )
            impact = project.get_impact()
            new_link = {
                "Shipping Destination": shipping_dest,
                "Shipping Origin": shipping_org,
                "Material": material,
                "Quantity (tonnes)": qty,
                "Travel Distance": travel_dist,
                "Scenario": scenario,
                "Return Trip Factor": return_trip_factor,
                "Distance Unit": dist_unit,
                "mode_name": mode_name,
                "efficiencyiciency Factor": efficiency,
                "mode_dms_name": mode_dms_name,
                "efficiency_dms": efficiency_dms,
            }
            st.session_state["transport_links"].append(new_link)
            st.session_state["impacts"].append(impact)
            st.success("Link added successfully!")

    elif tab_selection == "Edit Link":
        if not st.session_state["transport_links"]:
            st.write("No transportation links added yet. Please add a link first.")
        else:
            st.subheader("Edit Transportation Details")
            link_index = st.selectbox(
                "Select a Link to Edit",
                range(len(st.session_state["transport_links"])),
                format_func=lambda x: f"Link {x+1}",
            )
            selected_link = st.session_state["transport_links"][link_index]
            selected_link["Shipping Destination"] = st.text_input(
                "Shipping Destination:", selected_link["Shipping Destination"], key=f"dest_{link_index}"
            )
            selected_link["Shipping Origin"] = st.text_input(
                "Shipping Origin:", selected_link["Shipping Origin"], key=f"org_{link_index}"
            )
            selected_link["Material"] = st.text_input(
                "Material:", selected_link["Material"], key=f"material_{link_index}"
            )
            selected_link["Quantity (tonnes)"] = st.number_input(
                "Quantity (tonnes):", min_value=0.0, value=selected_link["Quantity (tonnes)"], key=f"qty_{link_index}"
            )
            selected_link["Travel Distance"] = st.number_input(
                "Travel Distance:", min_value=0.0, value=selected_link["Travel Distance"], key=f"dist_{link_index}"
            )
            selected_link["Scenario"] = st.selectbox(
                "Transportation scenario:",
                ["Local", "Regional", "Regional_c", "National", "NA", "Global"],
                index=["Local", "Regional", "Regional_c", "National", "NA", "Global"].index(selected_link["Scenario"]),
                key=f"scenario_{link_index}",
            )
            selected_link["Return Trip Factor"] = st.number_input(
                "Return Trip Factor:",
                min_value=1.0,
                value=selected_link["Return Trip Factor"],
                key=f"return_trip_{link_index}",
            )
            selected_link["Distance Unit"] = st.selectbox(
                "Distance Unit:",
                ["km", "Ml"],
                index=["km", "Ml"].index(selected_link["Distance Unit"]),
                key=f"unit_{link_index}",
            )
            selected_link["mode_name"] = st.selectbox(
                "Transportation mode_name:",
                ["Truck", "Rail", "Barge", "Air"],
                index=["Truck", "Rail", "Barge", "Air"].index(selected_link["mode_name"]),
                key=f"mode_name_{link_index}",
            )
            selected_link["efficiencyiciency Factor"] = st.slider(
                "efficiencyiciency Factor (1-3):",
                min_value=1,
                max_value=3,
                value=selected_link["efficiencyiciency Factor"],
                key=f"efficiency_{link_index}",
            )
            selected_link["mode_dms_name"] = st.selectbox(
                "Transportation mode_name for DMS:",
                ["Truck", "Rail", "Barge", "Air"],
                index=["Truck", "Rail", "Barge", "Air"].index(selected_link["mode_dms_name"]),
                key=f"mode_dms_{link_index}",
            )
            selected_link["efficiency_dms"] = st.slider(
                "efficiencyiciency Factor for DMS (1-3):",
                min_value=1,
                max_value=3,
                value=selected_link["efficiency_dms"],
                key=f"efficiency_dms_{link_index}",
            )

            if st.button("Update Link"):
                st.session_state["transport_links"][link_index] = selected_link
                st.success(f"Link {link_index + 1} updated successfully!")

# Tabs for Viewing Links and Results
tab1, tab2 = st.tabs(["Transportation Links", "Results"])

# Tab 1: Display Transportation Links
with tab1:
    if not st.session_state["transport_links"]:
        st.write("No transportation links added yet.")
    else:
        df = pd.DataFrame(st.session_state["transport_links"])
        st.dataframe(df, use_container_width=True)

        # if shipping_dest:
        #     st.map(
        #         data= location_df,
        #         latitude="latitude",
        #         longitude="longitude",
        #         size="size",
        #         use_container_width=True,
        #     )

# Tab 2: Results and Visualization
with tab2:
    if not st.session_state["transport_links"]:
        st.write("No transportation links added yet. Please add links first.")
    else:
        st.subheader("Impact Results by Category")

        # Prepare Data for Visualization
        impacts_df = pd.DataFrame(st.session_state["impacts"])
        impacts_df.index = [f"Link {i+1}" for i in range(len(st.session_state["impacts"]))]

        # Display Bar Charts for Each Impact Category
        for category in impacts_df.columns:
            st.write(f"### {category} Impact Comparison")
            st.bar_chart(impacts_df[category])


# streamlit run transportation_app.py
# C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\src\ui\transportation
