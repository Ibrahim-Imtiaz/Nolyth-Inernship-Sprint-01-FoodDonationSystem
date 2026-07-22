import requests
BASE_URL = "https://nolyth-inernship-sprint-01.onrender.com"

def login(email, password):
    return requests.post(
        f"{BASE_URL}/login",
        json={
            "email": email,
            "password": password
        }
    )


def register(user_data):
    return requests.post(
        f"{BASE_URL}/register",
        json=user_data
    )


def get_me(token):
    return requests.get(
        f"{BASE_URL}/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def create_donation(token, donation_data):
    return requests.post(
        f"{BASE_URL}/donations",
        json=donation_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_my_donations(token):
    return requests.get(
        f"{BASE_URL}/my-donations",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def update_donation(token, donation_id, donation_data):
    return requests.put(
        f"{BASE_URL}/donations/{donation_id}",
        json=donation_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_donation(token, donation_id):
    return requests.delete(
        f"{BASE_URL}/donations/{donation_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_available_donations(token):
    return requests.get(
        f"{BASE_URL}/available-donations",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def claim_donation(token, donation_id):
    return requests.post(
        f"{BASE_URL}/claim/{donation_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_my_claims(token):
    return requests.get(
        f"{BASE_URL}/my-claims",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )