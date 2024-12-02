import streamlit as st
import pandas as pd
from transportation.Project_logistic_manager import ProjectLogisticManager
from transportation.Logisticslink import Link


data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\transportation_dataset"
project = ProjectLogisticManager(name="Building A", location="Seattle", data_folder=data_folder)



# Streamlit App Title
st.title("Transportation Environmental Impact Calculator")

# Input Fields for Link Information
st.header("Add Transportation Details")

material = st.text_input("Material (e.g., Steel, Concrete):", "Steel")
qty = st.number_input("Quantity (tonnes):", min_value=0.0, value=1000.0)
travel_dist = st.number_input("Travel Distance (tkm):", min_value=0.0, value=200.0)
return_trip_factor = st.number_input("Return Trip Factor:", min_value=1.0, value=2.0)
dist_unit = st.selectbox("Distance Unit:", ["tkm"])
mode = st.selectbox("Transportation Mode:", ["Truck", "Rail", "Barge", "Air"])
eff = st.slider("Efficiency Factor (0-1):", min_value=0.0, max_value=1.0, value=0.8)





# Submit Button
if st.button("Calculate Impact"):
    try:
        # Create a Link instance with the input data
        link = Link(
            project=project,
            material=material,
            qty=qty,
            travel_dist=travel_dist,
            return_trip_factor=return_trip_factor,
            dist_unit=dist_unit,
            mode=mode,
            eff=eff
        )

        # Compute the impact
        impact = link.compute_impact()

        # Display the impact
        st.success("Environmental Impact Calculated Successfully!")
        st.subheader("Impact Details:")
        st.write(pd.DataFrame([impact]))
    except Exception as e:
        st.error(f"An error occurred: {e}")

