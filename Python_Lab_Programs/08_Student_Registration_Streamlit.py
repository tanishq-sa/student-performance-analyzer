import streamlit as st
from datetime import datetime

st.title("Student Registration Form")

name = st.text_input("Enter Student Name")
age = st.number_input("Enter Age", min_value=1, max_value=100)
course = st.text_input("Enter Course")
year = st.date_input(
    "Enter Year",
    value=datetime.now(),
    min_value=datetime(2020, 1, 1),
    max_value=datetime.now()
)
email = st.text_input("Enter Email")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
skills = st.text_area("Enter Skills")
confirmation = st.checkbox("I have read all the terms and privacy policy")

button = st.button("Submit")

if confirmation and button:
    if name != '' and course != '' and email != '' and skills != '':
        st.success("Registration Successful!")
        st.info(f"Student Name: {name}")
        st.info(f"Student Age: {age}")
        st.info(f"Student Course: {course}")
        st.info(f"Year: {year}")
        st.info(f"Student Email: {email}")
        st.info(f"Student Gender: {gender}")
        st.info(f"Student Skills: {skills}")
    else:
        st.error("Please fill in all the fields.")
elif button and not confirmation:
    st.warning("Please accept the terms and privacy policy.")
