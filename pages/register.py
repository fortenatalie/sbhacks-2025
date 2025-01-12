import streamlit as st
import yaml
from yaml import SafeLoader
from pathlib import Path

st.set_page_config(initial_sidebar_state="collapsed", page_title = "UCSB Dining Hall Reviews")

# ---------------------------
# Configuration and Utilities
# ---------------------------

# Path to the credentials file
CREDENTIALS_PATH = Path("config.yaml")

# Load existing credentials or initialize
def load_credentials(path):
    if path.exists():
        with open(path) as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        return {"credentials": {"usernames": {}}}

# Save credentials to the YAML file
def save_credentials(credentials, path):
    with open(path, "w") as file:
        yaml.dump(credentials, file, default_flow_style=False)

# ---------------------------
# Streamlit Sign-Up Page
# ---------------------------

def signup():
    st.title("📋 Sign Up")

    # Load existing credentials
    credentials = load_credentials(CREDENTIALS_PATH)

    # Sign-Up Form
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign Up")

        if submit:
            # Input validation
            if not email or not password or not username:
                st.error("❗ Please fill in all fields.")
            else:
                # Check if email already exists
                existing_users = credentials["credentials"]["usernames"]
                if any(user_info["email"] == email for user_info in existing_users.values()):
                    st.error("Email is already registered.")
                if any(user_info["name"] == username for user_info in existing_users.values()):
                    st.error("Username is already registered.")
                else:
                    # Generate a unique username (e.g., part before @)
                    # Add the new user to credentials
                    credentials["credentials"]["usernames"][username] = {
                        "email": email,
                        "name": username,
                        "password": password  # Storing password in plain text (Not secure)
                    }

                    # Save the updated credentials
                    save_credentials(credentials, CREDENTIALS_PATH)

                    st.success(f"User `{username}` registered successfully!")




# ---------------------------
# Navigation
# ---------------------------

#def app():
 #   st.sidebar.title("Navigation")
  #  app_mode = st.sidebar.selectbox("Choose Page", ["Sign Up", "Login"])
#
 #   if app_mode == "Sign Up":
  #      signup()


if __name__ == "__main__":
    #app()
    signup()
