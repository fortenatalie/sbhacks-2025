import requests
import json
from datetime import datetime, timezone, timedelta

def is_weekend(date):
    return date.weekday() in [5, 6]

def get_menu():
    current_time = datetime.now(timezone(timedelta(hours=-8)))
    formatted_time = current_time.isoformat()
    formatted_time = formatted_time[0:10]
    headers = {
        'accept': 'application/json',
        'ucsb-api-key': 'lr0DEL5lWLVzXJ9D8HmCxZ5gRZ20ieme',
    }

    dining_halls = ['de-la-guerra', 'carrillo', 'portola', 'ortega']
    
    if is_weekend(current_time):
        meals = ['Brunch', 'Dinner']
    else:
        meals = ['Breakfast', 'Lunch', 'Dinner']

    todays_meals = {}

    for location in dining_halls:
        for meal in meals:
            response = requests.get(f'https://api.ucsb.edu/dining/menu/v1/{formatted_time}/{location}/{meal}', headers=headers)
            if response.status_code == 200: 
                if location not in todays_meals:
                    todays_meals[location] = {}
                data = response.json()
                
                station_food_map = {}
                
                for item in data:
                    station = item['station']
                    food_name = item['name']
                    
                    if station not in station_food_map:
                        station_food_map[station] = []
                    
                    station_food_map[station].append(food_name)
                
                todays_meals[location][meal] = station_food_map
    print(todays_meals)
    
    return todays_meals
get_menu()

def adjust_menu_vegetarian(meals_map):
    veg_map = {}
    for location, meals in meals_map.items():
        for meal, stations in meals.items():
            for station, foods in stations.items():
                for food in foods:
                    if "(v)" in food or "(vgn)" in food:
                        if location not in veg_map:
                            veg_map[location] = {}
                        if meal not in veg_map[location]:
                            veg_map[location][meal] = {}
                        if station not in veg_map[location][meal]:
                            veg_map[location][meal][station] = []
                        veg_map[location][meal][station].append(food)
    return veg_map

def adjust_menu_vegan(meals_map): 
    vgn_map = {}
    for location, meals in meals_map.items():
        for meal, stations in meals.items():
            for station, foods in stations.items():
                for food in foods:
                    if "(vgn)" in food:
                        if location not in vgn_map:
                            vgn_map[location] = {}
                        if meal not in vgn_map[location]:
                            vgn_map[location][meal] = {}
                        if station not in vgn_map[location][meal]:
                            vgn_map[location][meal][station] = []
                        vgn_map[location][meal][station].append(food)
    return vgn_map
