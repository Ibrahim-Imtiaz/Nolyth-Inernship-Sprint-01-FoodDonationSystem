import streamlit as st
from api import get_available_donations,claim_donation,get_my_claims

def show():
    user = st.session_state["user"]
    token = st.session_state["token"]
    st.title("NGO Dashboard")
    st.write(f"Welcome, {user['organization_name']}")
    
    #available donations
    st.divider()
    st.subheader("Available Donations")
    response = get_available_donations(token)
    if response.status_code == 200:
        donations = response.json()
        if len(donations) == 0:
            st.info("No donations are currently available.")
        else:
            for donation in donations:
                with st.container(border=True):
                    st.write(f"Food Name: {donation['food_name']}")
                    st.write(f"Quantity: {donation['quantity']}")
                    st.write(f"Expiry Time: {donation['expiry_time']}")
                    st.write(f"Pickup Address: {donation['pickup_address']}")
                    st.write(f"Status: {donation['status']}")
                    if st.button(
                        "Claim Donation",
                        key=f"claim_{donation['id']}"
                    ):
                        claim_response = claim_donation(
                            token,
                            donation["id"]
                        )
                        if claim_response.status_code == 200:
                            st.success("Donation claimed successfully.")
                            st.rerun()
                        else:
                            try:
                                st.error(
                                    claim_response.json()["detail"]
                                )
                            except:
                                st.error("Unable to claim donation.")
    else:
        st.error("Failed to load donations.")
    #my claims
    st.divider()
    st.subheader("My Claims")
    response = get_my_claims(token)
    if response.status_code == 200:
        claims = response.json()
        if len(claims) == 0:
            st.info("You haven't claimed any donations yet.")
        else:
            for donation in claims:
                with st.container(border=True):
                    st.write(f"Food Name: {donation['food_name']}")
                    st.write(f"Quantity: {donation['quantity']}")
                    st.write(f"Expiry Time: {donation['expiry_time']}")
                    st.write(f"Pickup Address: {donation['pickup_address']}")
                    st.write(f"Status: {donation['status']}")
    else:
        st.error("Failed to load claimed donations.")