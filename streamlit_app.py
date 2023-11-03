import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

#Display Title and Description 
st.title("Welcome to this months Engagement Survey")
st.markdown("Fill out the survey below")

conn = st.connection("gsheets", type=GSheetsConnection)

#Fetch existing survey
existing_data = conn.read(worksheet="Surveys", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

#List of Survey types 
SURVEY_TYPES = [
    "Engagement Survey",
    "Employee Recognition",
    "Pulse Check",
    "Onboarding Survey",
]
ORGANIZATIONS = [
    "Information Technology",
    "Operations",
    "Human Resources",
    "Engineering",
    "Accounting",
]

#New Survey Form
with st.form(key="survey_form"):
    employee_role = st.text_input(label="Employee Role*")
    business_org = st.selectbox("Survey Type*", options=SURVEY_TYPES, index=None)
    manager_name = st.text_input(label="Manager Name")
    organizations = st.multiselect("Team", options=ORGANIZATIONS)
    engagement_level = st.slider("Engagement Level", 0,10,5)
    onboarding_date = st.date_input(label="onboarding_date")
    additional_info = st.text_area(label="Any addtional info you'd like to share")
    
    #Mark mandatory fields 
    st.markdown("**required**")
    
    submit_button = st.form_submit_button(label="Submit Your Engagement Survey")
    
    #if the submit button is pressd 
    if submit_button:
        if not employee_role or not business_org:
            st.warning("Please fill out mandatory fields")
            st.stop()
            
        # elif existing_data["EmployeeRole"].str.contains(employee_role).any():
        #     st.warning("An employee with this has already filled out this survey")
        #     st.stop()
        else:
            
            survey_data = pd.DataFrame(
                [
                    {
                        "EmployeeRole": employee_role,
                        "BusinessOrg": business_org,
                        "Organizations": ", ".join(organizations),
                        "ManagerName": manager_name,
                        "EngagementLevel": engagement_level,
                        "OnboardingDate": str(onboarding_date),
                        "AdditionalInfo": additional_info,
                    } 
                ]
            )
            
            updated_df = pd.concat([existing_data, survey_data], ignore_index=True)
            
            conn.update(worksheet="Surveys", data=updated_df)
            
            st.write("Your Survey Has Been Submitted!")