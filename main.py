import streamlit as st
import requests

BASE_URL = "https://api-298313983231.us-central1.run.app/api"  # Replace with your Django server URL

# Set up session state for tokens
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Function to register users
def register():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = requests.post(f"{BASE_URL}/register/", json=payload)
        if response.status_code == 201:
            st.success("User registered successfully!")
        else:
            st.error(response.json().get("error", "Registration failed"))

# Function to log in users
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {
            "username": username,
            "password": password,
        }
        response = requests.post(f"{BASE_URL}/login/", json=payload)
        if response.status_code == 200:
            tokens = response.json()
            st.session_state.access_token = tokens["access"]
            st.success("Login successful!")
        else:
            st.error(response.json().get("error", "Login failed"))

# Function to save a place
def save_place():
    st.title("Save a Place")
    if st.session_state.access_token is None:
        st.warning("Please log in first.")
        return

    name = st.text_input("Place Name")
    address = st.text_input("Address")
    latitude = st.text_input("Latitude")
    longitude = st.text_input("Longitude")
    photo_reference = st.text_input("Photo Reference")

    if st.button("Save Place"):
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        payload = {
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "photo_reference": photo_reference,
        }
        response = requests.post(f"{BASE_URL}/save-place/", json=payload, headers=headers)
        if response.status_code == 201:
            st.success("Place saved successfully!")
        else:
            st.error(response.json().get("error", "Failed to save place"))

# Function to search places
def search_places():
    # Placeholder for user input
    st.title("Search Places")
    query = st.text_input("Enter a query to search places:")

    # Check if the user entered a query
    if st.button("Search"):
        if not query.strip():
            st.error("Please enter a valid query.")
            return

        # Perform the API request
        try:
            response = requests.get(f"{BASE_URL}/search-place?q={query}")
            # Check HTTP status code
            if response.status_code == 200:
                try:
                    # Attempt to parse JSON
                    data = response.json()
                    st.success("Search results:")
                    st.write(data)
                except requests.exceptions.JSONDecodeError:
                    st.error("Received an unexpected response format. Please try again later.")
                    st.write(f"Response content: {response.text}")
            else:
                st.error(f"API request failed with status code {response.status_code}.")
                st.write(f"Response content: {response.text}")
        except requests.RequestException as e:
            st.error("An error occurred while connecting to the API.")
            st.write(f"Error details: {e}")

# Main Streamlit app
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Go to", ["Register", "Login", "Save Place", "Search Places"])

    if choice == "Register":
        register()
    elif choice == "Login":
        login()
    elif choice == "Save Place":
        save_place()
    elif choice == "Search Places":
        search_places()

if __name__ == "__main__":
    main()
