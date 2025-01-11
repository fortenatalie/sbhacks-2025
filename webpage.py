import streamlit as st
from todays_food_copy import food_map

st.title("UCSB Dining Hall Reviews")


diningHalls = ["Carrillo", "De La Guerra", "Ortega", "Portola"]
diningHallChoice = st.segmented_control("Dining Hall", diningHalls, selection_mode="single")
if (diningHallChoice is not None):
    diningHallChoice = diningHallChoice.lower()

    if (diningHallChoice == "de la guerra"):
        diningHallChoice = "de-la-guerra"
    meal = {}
    if (diningHallChoice in food_map):
        meal = food_map[diningHallChoice]
    if (len(meal) > 0):
        mealChoice = st.segmented_control("Meal",meal,selection_mode="single")
        if (mealChoice is not None):
            station = food_map[diningHallChoice][mealChoice]

            #How does Ortega handle stations? Rewrite later when known
            stationChoice = st.segmented_control("Station", station, selection_mode="single")
            if (stationChoice is not None):
                dish = food_map[diningHallChoice][mealChoice][stationChoice]

                dishChoice = st.selectbox("Dish", dish, index = 0)

    else:
        st.markdown("Nothing is being served here today.")


