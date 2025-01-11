import json

def load_foods_from_file(file_path="foods.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data



def find_food_by_name(data, food_name):
    for food in data["foods"]:
        if food["name"].lower() == food_name.lower():
            return food
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


def add_review():
    data = load_foods_from_file("foods.json")
    target_food_name = input("Enter in the name of the food: ")
    food = find_food_by_name(data, target_food_name)

    if food is None:
        print("Food not found")
    else:
        print(food)
        user_input = input("Enter name: ")
        rating_input = int(input("Enter rating: "))
        comment_input = input("Enter comment: ")
        add_review_to_food(food, user=user_input, rating=rating_input, comment=comment_input)
        save_foods_to_file(data, "foods.json")

def view_review():
    data = load_foods_from_file("foods.json")
    target_food_name = input("Enter in the name of the food: ")
    food = find_food_by_name(data, target_food_name)
    if food is None:
        print("Food not found")
        return
    
    if "reviews" in food:
        for review in food["reviews"]:
            user = review.get("user")
            rating = review.get("rating")
            comment = review.get("comment")
            print(f"User: {user}, Rating: {rating}, Comment: {comment}")
    else:
        print("No reviews as of now, check back later!")
    

def get_average_rating(food):
    sum = 0
    if "reviews" in food:
        for review in food["reviews"]:
            sum += reviews.get("rating")
    else:
        print("No reviews found not found")


# add_review()

view_review()
