#libraries used: streamlit authenticator, streamlit extras
import streamlit as st
import streamlit_authenticator as stauth
from datetime import date
from todays_food_copy import food_map
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

with open('config.yaml') as file:
    config = yaml.load(file, Loader = SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials']
)

try:
    authenticator.login()
    
    with (st.form("register_form")):
        st.markdown("New to UCSB Dining Hall Reviews?")
        submitButton = st.form_submit_button("Sign up now.")
        
        if (submitButton):
                switch_page("register")
    if st.session_state['authentication_status']:
        authenticator.logout()

        #Ex: 1/11/2025 would be 2025-01-11
        todaydate = date.today().isoformat()

        st.title("UCSB Dining Hall Reviews")


        #handles dining hall selection
        diningHalls = ["Carrillo", "De La Guerra", "Ortega", "Portola"]
        diningHallChoice = st.segmented_control("Dining Hall", diningHalls, selection_mode="single")
        if (diningHallChoice is not None):
            diningHallChoice = diningHallChoice.lower()

            #"De La Guerra" is how DLG will be displayed, "de-la-guerra" is how it is referred to internally
            if (diningHallChoice == "de la guerra"):
                diningHallChoice = "de-la-guerra"
    
            meal = {}
            if (diningHallChoice in food_map):
                meal = food_map[diningHallChoice]
    
            #if meal has been chosen, displays other options    
            if (len(meal) > 0):
                mealChoice = st.segmented_control("Meal",meal,selection_mode="single")
                if (mealChoice is not None):
                    station = food_map[diningHallChoice][mealChoice]

                    #doesn't make sense to call ortega's food options stations, so they're called categories instead
                    category = "Station"
                    if (diningHallChoice == "ortega"):
                        category = "Category"
                    stationChoice = st.segmented_control(category, station, selection_mode="single")

                    if (stationChoice is not None):
                        dish = food_map[diningHallChoice][mealChoice][stationChoice]

                        dishChoice = st.selectbox("Dish", dish, index = 0)
                
                        #Later: add users, when user submits another review on the same day for the same item, update the review
                        with st.form("review_form"):
                            message = "How do you feel about " + dishChoice + "?"

                            st.markdown(message)

                            #default value is None
                            starRating = st.feedback("stars")

                            reviewText = st.text_area("Write your review here!")

                            submit = st.form_submit_button("Submit my review")

                            #if review does not have a star rating after submission, tells user to submit a star rating
                            if (submit and starRating is None):
                                st.markdown("Please submit a star rating!")
                    
    
    
        #displays if the dining hall is closed for the day
        else:
            st.markdown("Nothing is being served here today.")
except Exception as e:
    st.error(e)



