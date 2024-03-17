import csv
import random
from faker import Faker
import openai

faker = Faker()


with open('users.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['UserID', 'Username', 'Password', 'Email', 'UserType', 'CreationDate'])
    for i in range(1, 101): 
        creation_date = faker.date_time_this_decade()
        formatted_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")  
        writer.writerow([
            i,
            faker.user_name(),
            faker.password(),
            faker.email(),
            random.choice(['Customer', 'Driver', 'RestaurantAdmin', 'PlatformAdmin']),
            formatted_date  
        ])




with open('restaurants.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RestaurantID', 'Name', 'Address', 'Rating', 'IsActive', 'OwnerID'])
    for i in range(1, 51):
        writer.writerow([
            i,
            faker.company(),
            faker.address().replace('\n', ', '),
            round(random.uniform(1, 5), 2),
            random.choice([1, 0]),
            random.randint(1, 100)
        ])


with open('orders.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['OrderID', 'UserID', 'DriverID', 'RestaurantID', 'OrderStatus', 'OrderTime', 'TotalPrice'])
    for i in range(1, 201):
        writer.writerow([
            i,
            random.randint(1, 100),
            random.randint(1, 100),
            random.randint(1, 50),
            random.choice(['Placed', 'Preparing', 'Ready for Pickup', 'En Route', 'Delivered', 'Cancelled']),
            faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            round(random.uniform(10, 500), 2)
        ])



restaurant_ids = range(1, 51)
user_ids = range(1, 101)




def generate_text(prompt, tokens):
    openai.api_key = "OPENAI_API_KEY"
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=tokens,
        temperature=1,
    )
    
    return response.choices[0].message.content



with open('menuitems.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MenuItemID', 'RestaurantID', 'Name', 'Description', 'Price'])
    for i in range(1, 501): 
        food_prompt = "Generate a unique food item name e.g. 'Chicken Alfredo' or 'Vegan Burger'"
        food_item = generate_text(food_prompt, 5)
        description_prompt = f"Generate a simple concise description for {food_item} menu item in the form of a sentence simple e.g. 'Italian dish with a creamy sauce and tender chicken' or 'Vegan burger with fresh vegetables and a special sauce'. Make sure it makes grammatical sense."
        description = generate_text(description_prompt, 15)
        writer.writerow([
            i,
            random.choice(restaurant_ids),
            food_item,
            description,
            round(random.uniform(5, 50), 2)
        ])


with open('drivers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['DriverID', 'LicenseNumber', 'VehicleType', 'IsActive'])
    for i in range(6, 100, random.randint(1, 10)): 
        writer.writerow([
            i,
            faker.license_plate(),
            random.choice(['Car', 'Bike', 'Scooter']),
            random.choice([1, 0])  
        ])

def generate_unique_tags(file_name, num_tags):
    unique_tags = set() 

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['TagID', 'TagName'])

        while len(unique_tags) < num_tags:
            tag_prompt = "Generate a tag name corresponding to a restaurant feature or cuisine type e.g. 'Outdoor Seating', 'Vegan', 'Italian', 'Family Friendly', etc. This should be a single word or short phrase that can be used as a"
            tag_name = generate_text(tag_prompt, 3).strip()
            
            if tag_name not in unique_tags:
                unique_tags.add(tag_name)
                writer.writerow([len(unique_tags), tag_name])

generate_unique_tags('tags.csv', 50)

def generate_restaurant_tags(file_name, restaurant_ids, num_tags):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['RestaurantID', 'TagID'])

        for restaurant_id in restaurant_ids:
            tag_ids = random.sample(range(1, num_tags + 1), random.randint(1, 3))
            for tag_id in tag_ids:
                writer.writerow([restaurant_id, tag_id])

generate_restaurant_tags('restauranttags.csv', range(1, 51), 50)

def generate_ratings(file_name, num_ratings, user_ids, restaurant_ids, order_ids):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['RatingID', 'UserID', 'RestaurantID', 'DriverID', 'OrderID', 'Score', 'Comment', 'RatingDate'])

        for i in range(1, num_ratings + 1):
            rating_prompt = "Generate a short review comment for a restaurant experience"
            comment = generate_text(rating_prompt, 15)
            rating_date = faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                i,
                random.choice(user_ids),
                random.choice(restaurant_ids),
                random.choice(user_ids),  
                random.choice(order_ids),
                random.randint(1, 5),
                comment,
                rating_date
            ])

generate_ratings('ratings.csv', 300, range(1, 101), range(1, 51), range(1, 201))