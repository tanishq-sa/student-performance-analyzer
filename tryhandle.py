import streamlit as st

st.title("Student Record Management System")

st.text_input("Enter Product name")
price = st.number_input("Enter Product Price", min_value=0)
if price >= 1000:
    st.success("Discount is there")
else:
    st.error("No Discount")
