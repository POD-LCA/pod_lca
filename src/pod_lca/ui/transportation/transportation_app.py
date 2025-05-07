import streamlit as st
import pandas as pd
from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager
from lca_modules.transportation.logistics_link import Link
import matplotlib.pyplot as plt
import random  # Replace with your methods for real calculations

data_folder = r'data/transportation_dataset'
project = ProjectLogisticManager(name="Building A", location="Seattle", data_folder=data_folder)

# Streamlit App Title
st.image(r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\PODLCA logo - transparent.png", use_column_width=False, width=100)
#

import streamlit as st
import pandas as pd


# Page Title
st.title("Transportation Environmental Impact Calculator")

# Initialize Session State for Links and Impacts
if "transport_links" not in st.session_state:
    st.session_state["transport_links"] = []

if "impacts" not in st.session_state:
    st.session_state["impacts"] = []

# Sidebar for Adding and Editing Transportation Links
with st.sidebar:
    st.header("Manage Transportation Links")
    
    tab_selection = st.radio("Choose Action", ["Add Link", "Edit Link"])

    if tab_selection == "Add Link":
        st.subheader("Add Transportation Details")
        material = st.text_input("Material (e.g., Steel, Concrete):", "Steel")
        qty = st.number_input("Quantity (tonnes):", min_value=0.0, value=1000.0)
        travel_dist = st.number_input("Travel Distance (tkm):", min_value=0.0, value=200.0)
        return_trip_factor = st.number_input("Return Trip Factor:", min_value=1.0, value=2.0)
        dist_unit = st.selectbox("Distance Unit:", ["km", "Ml"])
        mode = st.selectbox("Transportation Mode:", ["Truck", "Rail", "Barge", "Air"])
        eff = st.slider("Efficiency Factor (1-3):", min_value=1, max_value=3, value=2)

        if st.button("Add Link"):
            new_link = {
                "Material": material,
                "Quantity (tonnes)": qty,
                "Travel Distance (tkm)": travel_dist,
                "Return Trip Factor": return_trip_factor,
                "Distance Unit": dist_unit,
                "Mode": mode,
                "Efficiency Factor": eff,
            }
            st.session_state["transport_links"].append(new_link)
            st.session_state["impacts"].append(
                {"GWP": 3.0, "AP": 2.0, "EP": 0.0, "ODP": 0.0, "SFP": 0.0}
            )
            st.success("Link added successfully!")

    elif tab_selection == "Edit Link":
        if not st.session_state["transport_links"]:
            st.write("No transportation links added yet. Please add a link first.")
        else:
            st.subheader("Edit Transportation Details")
            link_index = st.selectbox("Select a Link to Edit", range(len(st.session_state["transport_links"])),
                                      format_func=lambda x: f"Link {x+1}")
            selected_link = st.session_state["transport_links"][link_index]
            selected_link["Material"] = st.text_input("Material:", selected_link["Material"], key=f"material_{link_index}")
            selected_link["Quantity (tonnes)"] = st.number_input("Quantity (tonnes):", min_value=0.0, value=selected_link["Quantity (tonnes)"], key=f"qty_{link_index}")
            selected_link["Travel Distance (tkm)"] = st.number_input("Travel Distance (tkm):", min_value=0.0, value=selected_link["Travel Distance (tkm)"], key=f"dist_{link_index}")
            selected_link["Return Trip Factor"] = st.number_input("Return Trip Factor:", min_value=1.0, value=selected_link["Return Trip Factor"], key=f"return_trip_{link_index}")
            selected_link["Distance Unit"] = st.selectbox("Distance Unit:", ["km", "Ml"], index=["km", "Ml"].index(selected_link["Distance Unit"]), key=f"unit_{link_index}")
            selected_link["Mode"] = st.selectbox("Transportation Mode:", ["Truck", "Rail", "Barge", "Air"], index=["Truck", "Rail", "Barge", "Air"].index(selected_link["Mode"]), key=f"mode_{link_index}")
            selected_link["Efficiency Factor"] = st.slider("Efficiency Factor (1-3):", min_value=1, max_value=3, value=selected_link["Efficiency Factor"], key=f"eff_{link_index}")

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

# Tab 2: Results and Visualization
with tab2:
    if not st.session_state["transport_links"]:
        st.write("No transportation links added yet. Please add links first.")
    else:
        st.subheader("Impact Results by Category")

        # Mock impact calculations (replace with your real calculations)
        for i in range(len(st.session_state["impacts"])):
            st.session_state["impacts"][i] = {
                "GWP": random.uniform(0, 50),
                "AP": random.uniform(0, 10),
                "EP": random.uniform(0, 5),
                "ODP": random.uniform(0, 1),
                "SFP": random.uniform(0, 20),
            }

        # Prepare Data for Visualization
        impacts_df = pd.DataFrame(st.session_state["impacts"])
        impacts_df.index = [f"Link {i+1}" for i in range(len(st.session_state["impacts"]))]

        # Display Bar Charts for Each Impact Category
        for category in impacts_df.columns:
            st.write(f"### {category} Impact Comparison")
            st.bar_chart(impacts_df[category])




# streamlit run transportation_app.py