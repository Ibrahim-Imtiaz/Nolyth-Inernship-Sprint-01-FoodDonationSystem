import streamlit as st
import requests

st.title("Food Donation System")
st.header("Login")
email = st.text_input("Email")
password = st.text_input("Password",type="password")
if st.button("Login"):
    st.write("Logging in...")