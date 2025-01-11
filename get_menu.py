# THIS ONLY NEEDS TO BE RUN ONCE PER DAY, SEE TODAYS_FOOD_COPY.TXT FOR TESTING PURPOSES

import requests
import json
from datetime import datetime, timezone, timedelta

current_time = datetime.now(timezone(timedelta(hours=-8)))
formatted_time = current_time.isoformat()

headers = {
    'accept': 'application/json',
    'ucsb-api-key': 'lr0DEL5lWLVzXJ9D8HmCxZ5gRZ20ieme',
}

dining_halls = ['de-la-guerra', 'carrillo', 'portola', 'ortega']
meals = ['breakfast', 'brunch', 'lunch', 'dinner']
todays_meals = {}

for location in dining_halls:
    for meal in meals:
        response = requests.get(f'https://api.ucsb.edu/dining/menu/v1/{formatted_time}/{location}/{meal}', headers=headers)
        if response.status_code == 200: 
            if location not in todays_meals:
                todays_meals[location] = {}
            data = response.json()
            
            # Create a dictionary to store stations and their food items for this meal
            station_food_map = {}
            
            for item in data:
                station = item['station']
                food_name = item['name']
                
                # Add the station to the dictionary if it doesn't exist
                if station not in station_food_map:
                    station_food_map[station] = []
                
                # Append the food item to the station's list
                station_food_map[station].append(food_name)
            
            # Store the station_food_map for the current meal in todays_meals
            todays_meals[location][meal] = station_food_map

print(json.dumps(todays_meals, indent=4))