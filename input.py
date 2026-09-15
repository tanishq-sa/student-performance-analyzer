import streamlit as st
from datetime import datetime


st.title("Student Registration System", text_alignment='center')
name = st.text_input("Enter Student Name")
age = st.number_input("Enter Age")
course = st.text_input("Enter Course")
year = st.datetime_input(
    "Enter Year",value='now', min_value=datetime(2020, 1, 1), max_value='now')
email = st.text_input("Enter Email")
gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
skills = st.text_area("Enter Skills")
confirmation = st.checkbox("Read all the tos and privacy policy")
st.chat_input("Enter Student Name")
button = st.button("Submit")
if confirmation and button:
    if name != '' and age != '' and course != '' and email != '' and gender != '' and skills != '':
        st.info(f"Student Name: {name}")
        st.info(f"Student Age: {age}")
        st.info(f"Student Course: {course}")
        st.info(f"Student Email: {email}")
        st.info(f"Student Gender: {gender}")
        st.info(f"Student Skills: {skills}")
    else:
        st.error("Please enter a valid input")
