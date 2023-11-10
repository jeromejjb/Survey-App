import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Employee Engagement Dashboard")
st.markdown("Welcome to this month's Engagement Dashboard.")

conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
existing_data = conn.read(worksheet="DashboardData", usecols=list(range(5)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Display existing data as a table
st.subheader("Existing Dashboard Data")
st.dataframe(existing_data)

# Add a new element with a button
if st.button("Add New Element"):
    new_element = st.text_input("Enter New Element:")
    
    if new_element:
        updated_data = existing_data.append({"Element": new_element}, ignore_index=True)
        conn.update(worksheet="DashboardData", data=updated_data)
        st.success("New element added successfully!")

# You can add more visualizations and features as needed
