#libraries used: streamlit authenticator, streamlit extras
import streamlit as st
import streamlit_authenticator as stauth
from datetime import date
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
from todays_food_copy import food_map
import reviews

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

                #TODO: capitalize meal choices later
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
                            #TODO: Keep duplicate reviews from being submitted
                            elif (submit):
                                starRating = starRating + 1
                                reviews.find_food(diningHallChoice,mealChoice, stationChoice, dishChoice)
                                reviews.add_review(diningHallChoice, mealChoice, stationChoice, dishChoice, st.session_state["username"], starRating, reviewText )
                                st.markdown("Review added!")
                        if (reviews.get_amount() == 1):
                            st.subheader(str(reviews.get_amount()) + " User Review", divider = "gray")
                        elif(reviews.get_amount() == 0):
                            st.subheader("No User Reviews", divider = "gray")
                        else:
                            st.subheader(str(reviews.get_amount()) + " User Reviews", divider = "gray")

                        foodReviews = reviews.view_review(dishChoice, diningHallChoice)
                        #displays items in newest - oldest order
                        if (foodReviews is not None):
                            foodReviews = foodReviews["reviews"]

                            for item in reversed(foodReviews):
                                if (item is not None):
                                    container = st.container(border=True)
                                    #TODO: make the username bold later
                                    container.write(f"**{item["user"]}**")
                                    container.write(item["date"])
                           
                                    #star rating
                                    if (item["rating"] == 5):
                                        container.markdown(":star2: :star2: :star2: :star2: :star2:")
                                    elif(item["rating"] == 4):
                                        container.markdown(":star2: :star2: :star2: :star2:")
                                    elif(item["rating"] == 3):
                                        container.markdown(":star2: :star2: :star2:")
                                    elif(item["rating"] == 2):
                                        container.markdown(":star2: :star2:")
                                    elif(item["rating"] == 1):
                                        container.markdown(":star2:")

                                    container.write(item["comment"])
                        else:
                            st.markdown("Be the first to leave a review!")
                        
                    
    
     
            #displays if the dining hall is closed for the day
            else:
                st.markdown("Nothing is being served here today.")
except Exception as e:
    st.error(e)



