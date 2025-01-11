import json
from datetime import datetime

#loads in json file, helper function
def load_data_from_file(file_path="foods.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data_to_file(data, file_path="foods.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)




#search for food by name and hall, helper function
def find_food_by_name(data, food_name, hall_name):
    if hall_name not in data:
        print("Hall not found")
        return None
    
    hall_data = data[hall_name]

    for meal_time, stations in hall_data.items():
        for station_name, food_list in stations.items():
            for food in food_list:
                if (food["name"].lower() ==  food_name.lower()):
                    return food
    
    print("Food not found")
    return None


#helper function
def get_average_rating(food):
    sum = 0
    count = 0
    if "reviews" in food:
        for review in food["reviews"]:
            sum += review.get("rating")
            count += 1

        return round(sum/count)
    else:
        return ("No reviews yet")






#return food dict, includes reviews
def view_review(target_food_name, target_hall_name):
    data = load_data_from_file("foods.json")
    food = find_food_by_name(data, target_food_name, target_hall_name)
    if food is None:
        print("Food not found")
        return

    return food

def find_food(location, meal, station, food):
    data = load_data_from_file("foods.json")

    if not (any(item.get("name") == food for item in data[location][meal][station])): # food doesn't exist
        data[location][meal][station].append({"name": food, "reviews": []})

    save_data_to_file(data)

def exists_reviews(location, meal, station, food):
    data = load_data_from_file("foods.json")
    for food_item in data[location][meal][station]:
        if food_item["name"] == food:
            if food_item["reviews"] == []:
                return False
            else:
                return True

def add_review(location, meal, station, food, username, rating, comment):
    formatted_date = datetime.now().strftime("%m/%d/%Y")
    data = load_data_from_file("foods.json")
    for food_item in data[location][meal][station]:
        if food_item["name"] == food:
            food_item["reviews"].append({"user": username, "rating": rating, "comment": comment, "date": formatted_date})
    save_data_to_file(data)






#print(view_review("Basic Pizza", "de-la-guerra"))
#print(add_review("Basic Pizza", "de-la-guerra", "Tim", 5, "Very very good"))

