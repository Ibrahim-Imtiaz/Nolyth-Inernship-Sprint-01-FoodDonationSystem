import streamlit as st
from datetime import datetime
from api import create_donation,get_my_donations,update_donation,delete_donation
def show():
    user = st.session_state["user"]
    token = st.session_state["token"]
    st.title("Donor Dashboard")
    st.write(f"Welcome, {user['organization_name']}")
    # Session State
    if "editing" not in st.session_state:
        st.session_state.editing = None
    # Create Donation
    st.divider()
    st.subheader("Create Donation")
    with st.form("create_donation"):
        food_name = st.text_input("Food Name")
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )
        expiry_date = st.date_input("Expiry Date")
        expiry_time = st.time_input("Expiry Time")
        pickup_address = st.text_area("Pickup Address")
        create = st.form_submit_button("Create Donation")
        if create:
            expiry_datetime = datetime.combine(
                expiry_date,
                expiry_time
            ).isoformat()
            response = create_donation(
                token,
                {
                    "food_name": food_name,
                    "quantity": quantity,
                    "expiry_time": expiry_datetime,
                    "pickup_address": pickup_address
                }
            )
            if response.status_code == 201:
                st.success("Donation created successfully.")
                st.rerun()
            else:
                try:
                    st.error(response.json()["detail"])
                except:
                    st.error("Unable to create donation.")
    # My Donations
    st.divider()
    st.subheader("My Donations")
    response = get_my_donations(token)
    if response.status_code != 200:
        st.error("Unable to load donations.")
        return
    donations = response.json()
    if len(donations) == 0:
        st.info("No donations found.")
        return
    editing_donation = None
    for donation in donations:
        with st.container(border=True):
            st.write(f"Food Name: {donation['food_name']}")
            st.write(f"Quantity: {donation['quantity']}")
            st.write(f"Status: {donation['status']}")
            st.write(f"Expiry: {donation['expiry_time']}")
            st.write(f"Pickup Address: {donation['pickup_address']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "Update",
                    key=f"update_{donation['id']}"
                ):
                    st.session_state.editing = donation["id"]
                    st.rerun()
            with col2:
                if st.button(
                    "Delete",
                    key=f"delete_{donation['id']}"
                ):
                    delete_response = delete_donation(
                        token,
                        donation["id"]
                    )
                    if delete_response.status_code == 200:
                        st.success("Donation deleted.")
                        st.rerun()
                    else:
                        st.error("Unable to delete donation.")
        if donation["id"] == st.session_state.editing:
            editing_donation = donation
    # Update Donation
    if editing_donation:
        st.divider()
        st.subheader("Update Donation")
        expiry = datetime.fromisoformat(
            editing_donation["expiry_time"]
        )
        with st.form("update_form"):
            food_name = st.text_input(
                "Food Name",
                value=editing_donation["food_name"]
            )
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=int(editing_donation["quantity"]),
                step=1
            )
            expiry_date = st.date_input(
                "Expiry Date",
                value=expiry.date()
            )
            expiry_time = st.time_input(
                "Expiry Time",
                value=expiry.time().replace(microsecond=0)
            )
            pickup_address = st.text_area(
                "Pickup Address",
                value=editing_donation["pickup_address"]
            )
            col1, col2 = st.columns(2)
            with col1:
                save = st.form_submit_button("Save Changes")
            with col2:
                cancel = st.form_submit_button("Cancel")
            if cancel:
                st.session_state.editing = None
                st.rerun()
            if save:
                expiry_datetime = datetime.combine(
                    expiry_date,
                    expiry_time
                ).isoformat()
                response = update_donation(
                    token,
                    editing_donation["id"],
                    {
                        "food_name": food_name,
                        "quantity": quantity,
                        "expiry_time": expiry_datetime,
                        "pickup_address": pickup_address
                    }
                )
                if response.status_code == 200:
                    st.success("Donation updated successfully.")
                    st.session_state.editing = None
                    st.rerun()
                else:
                    try:
                        st.error(response.json()["detail"])
                    except:
                        st.error("Unable to update donation.")