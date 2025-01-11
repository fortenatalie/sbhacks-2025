import json

#loads in json file, helper function
def load_foods_from_file(file_path="foods.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data




#search for food by name and hall
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


def add_review_to_food(food, user, rating, comment):
    new_review = {
        "user": user,
        "rating": rating,
        "comment": comment
    }
    food["reviews"].append(new_review)



def save_foods_to_file(data, file_path="foods.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)






def add_review(target_food_name, target_hall_name, user_input, rating_input, comment_input):
    data = load_foods_from_file("foods.json")
    food = find_food_by_name(data, target_food_name, target_hall_name)

    if food is None:
        print("Food not found")
    else:
        print(food)
        add_review_to_food(food, user=user_input, rating=rating_input, comment=comment_input)
        save_foods_to_file(data, "foods.json")

def view_review(target_food_name, target_hall_name):
    data = load_foods_from_file("foods.json")
    food = find_food_by_name(data, target_food_name, target_hall_name)
    if food is None:
        print("Food not found")
        return

    print(food["name"])
    
    if "reviews" in food:
        for review in food["reviews"]:
            user = review.get("user")
            rating = review.get("rating")
            comment = review.get("comment")
            print(f"User: {user}, Rating: {rating}, Comment: {comment}")
    else:
        print("No reviews as of now, check back later!")
    
    get_average_rating(food)
    

def get_average_rating(food):
    sum = 0
    count = 0
    if "reviews" in food:
        for review in food["reviews"]:
            sum += review.get("rating")
            count += 1
    else:
        print("No reviews found not found")
    
    print("Average rating: " + str(sum/count))




view_review("Basic Pizza", "de-la-guerra")
#add_review("Basic Pizza", "de-la-guerra", "Josh", 5, "Very very good")

