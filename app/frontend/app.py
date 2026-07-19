import streamlit as st

from api import login, register, get_me
from donor_dashboard import show as donor_dashboard
from ngo_dashboard import show as ngo_dashboard

st.set_page_config(
    page_title="Food Donation System",
    layout="wide"
)

st.title("Food Donation System")

# LOGOUT
if "token" in st.session_state:
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
# LOGIN/REGISTER
if "token" not in st.session_state:
    login_tab, register_tab = st.tabs(["Login", "Register"])
    #LOGIN
    with login_tab:
        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )
        if st.button("Login"):
            response = login(email, password)
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state["token"] = token
                user_response = get_me(token)
                if user_response.status_code == 200:
                    st.session_state["user"] = user_response.json()
                    st.rerun()
                else:
                    st.error("Unable to fetch user details.")
            else:
                st.error("Invalid email or password.")
    #REGISTER
    with register_tab:
        organization_name = st.text_input(
            "Organization Name"
        )
        contact_person = st.text_input(
            "Contact Person"
        )
        email = st.text_input(
            "Email",
            key="register_email"
        )
        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )
        contact_number = st.text_input(
            "Contact Number"
        )
        role = st.selectbox(
            "Role",
            ["Donor", "NGO"]
        )
        if st.button("Register"):
            response = register({
                "organization_name": organization_name,
                "contact_person": contact_person,
                "email": email,
                "password": password,
                "contact_number": contact_number,
                "role": role
            })
            if response.status_code == 201:
                st.success(
                    "Registration successful. Please login."
                )
            else:
                try:
                    st.error(response.json()["detail"])
                except:
                    st.error("Registration failed.")
# ROUTING
else:
    role = st.session_state["user"]["role"]
    if role == "Donor":
        donor_dashboard()
    elif role == "NGO":
        ngo_dashboard()
    else:
        st.error("Unknown role.")