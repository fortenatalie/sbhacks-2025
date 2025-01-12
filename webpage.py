#libraries used: streamlit authenticator, streamlit extras
import streamlit as st
import streamlit_authenticator as stauth
from datetime import date
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page
import reviews
st.set_page_config(initial_sidebar_state="collapsed", page_title = "UCSB Dining Hall Reviews")

with open('config.yaml') as file:
    config = yaml.load(file, Loader = SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials']
)

col1, col2, col3, col4, col5 = st.columns(5)

import get_menu

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    food_map = get_menu.get_menu()



try:
    authenticator.login()
    
    if (not st.session_state['authentication_status'] ):
        with (st.form("register_form")):
            st.markdown("New to UCSB Dining Hall Reviews?")
            submitButton = st.form_submit_button("Sign up now.")
        
            if (submitButton):
                switch_page("register")
    if st.session_state['authentication_status']:
        with col5:
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
                        reviews.find_food(diningHallChoice,mealChoice, stationChoice, dishChoice)
                        
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
                            elif (submit):
                                starRating = starRating + 1
                                
                                status = reviews.add_review(diningHallChoice, mealChoice, stationChoice, dishChoice, st.session_state["username"], starRating, reviewText )
                                
                                
                                if (status == "newReview"):
                                    st.markdown("Review added!")
                                elif (status == "updatedReview"):
                                    st.markdown("Review updated!")
                                elif (status == "duplicateReview"):
                                    st.markdown("No duplicate reviews.")

                        
                        foodReviews = reviews.view_review(dishChoice, diningHallChoice)
                        #displays items in newest - oldest order
                        if (foodReviews is not None):
                            
                            tempCount = 0
                            tempSum = 0
                            averageRating = 0
                            for item in foodReviews["reviews"]:
                                tempSum = tempSum + item["rating"]
                                tempCount = tempCount + 1
                            if (tempCount != 0):
                                averageRating = round(tempSum/tempCount, 1)
                            if (int(reviews.get_amount(foodReviews)) == 1):
                                st.subheader(str(reviews.get_amount(foodReviews)) + " User Review", divider = "gray")
                            elif(int(reviews.get_amount(foodReviews)) == 0):
                                st.subheader("No User Reviews", divider = "gray")
                            else:
                                st.subheader(str(reviews.get_amount(foodReviews)) + " User Reviews - " + str(averageRating) + ":star2:", divider = "gray")

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



