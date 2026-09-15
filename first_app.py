import streamlit as st


st.title('Student Result Application', text_alignment='center')
st.header('Enter Details')
st.text("Enter Name and Marks")
name = st.text_input('Enter Name: ')
marks = st.number_input('Enter Marks: ', min_value=0, max_value=100)
button = st.button('Check Result', type='primary')
if button:
    if name == "":
        st.error("Enter Name and Marks")
    else:
        st.write("Student Name", name)
        if marks > 40:
            st.success(f'Your mark is {marks}, You Passed')
        else:
            st.error(f'Your mark is {marks}, You Failed')