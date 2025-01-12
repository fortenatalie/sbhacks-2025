#libraries used: streamlit authenticator, streamlit extras
import streamlit as st
import streamlit_authenticator as stauth
from datetime import date
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
from todays_food_copy import food_map
import reviews
import json

st.set_page_config(initial_sidebar_state="collapsed", page_title = "UCSB Dining Hall Reviews")

with open('config.yaml') as file:
    config = yaml.load(file, Loader = SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials']
)

col1, col2, col3, col4, col5 = st.columns(5)


try:
    authenticator.login()
    
    if st.session_state['authentication_status']:
        switch_page("reviewpage")
    if (not st.session_state['authentication_status'] ):
        with (st.form("register_form")):
            st.markdown("New to UCSB Dining Hall Reviews?")
            submitButton = st.form_submit_button("Sign up now.")
        
            if (submitButton):
                switch_page("register")

except Exception as e:
    st.error(e)
