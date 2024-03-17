# restaurants.py
import db
import llm_integration

def restaurant_interface(user_session):
    print("\nRestaurant Menu:")
    print("Tell me what you would like to do, for example, 'View my restaurant', 'Update my restaurant', 'Manage menu', 'View orders', 'View ratings', 'Add tags', 'Remove tags', 'View available tags' or 'Return to main menu'.")

    while True:
        user_input = input("Your request: ")
        response_text = llm_integration.process_natural_language_query(user_input, user_session)
        print("LLM Response:", response_text)
        restaurant_id = get_restaurant_id_by_owner(user_session['UserID'])

        if "view_my_restaurant" in response_text:
            view_my_restaurant(user_session['UserID'])
        elif "update_my_restaurant" in response_text:
            update_my_restaurant(user_session['UserID'])
        elif "manage_menu" in response_text:
            if restaurant_id:
                manage_menu(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "view_orders" in response_text:
            if restaurant_id:
                view_orders_for_restaurant(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "view_ratings" in response_text:
            if restaurant_id:
                view_ratings_for_restaurant(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "add_new_tag" in response_text:
            tag_name = input("Enter the tag name to add: ")
            if restaurant_id:
                add_new_tag(restaurant_id, tag_name)
            else:
                print("Restaurant not found.")
        elif "remove_tag" in response_text:
            tag_name = input("Enter the tag name to remove: ")
            if restaurant_id:
                remove_tag(restaurant_id, tag_name)
            else:
                print("Restaurant not found.")
        elif "show_available_tags" in response_text:
            show_available_tags()
        elif "calculate_revenue" in response_text:
            if restaurant_id:
                calculate_revenue(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "view_best_selling_items" in response_text:
            if restaurant_id:
                view_best_selling_items(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "view_poorest_selling_items" in response_text:
            if restaurant_id:
                view_poorest_selling_items(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "update_order_status" in response_text:
            if restaurant_id:
                update_order_status(restaurant_id)
            else:
                print("Restaurant not found.")
        elif "return_to_main_menu" in response_text:
            break
        else:
            print("I didn't understand that. Can you please rephrase or specify your request?")
            
def search_restaurants(query):
    print(f"\n--- Searching for '{query}' ---")
    conn = db.create_connection()
    if conn is not None:
        query = f"""
        SELECT RestaurantID, Name, Address, Rating 
        FROM Restaurants 
        WHERE Name LIKE '%{query}%' OR Address LIKE '%{query}%'
        """
        restaurants = db.execute_read_query(conn, query)
        if restaurants:
            for restaurant in restaurants:
                print(f"RestaurantID: {restaurant['RestaurantID']}, Name: {restaurant['Name']}, Address: {restaurant['Address']}, Rating: {restaurant['Rating']}")
        else:
            print("No matching restaurants found.")
    else:
        print("Failed to connect to the database.")
            
def rate_restaurant(user_id):
    print("\n--- Rate a Restaurant ---")
    order_id = input("Enter the order ID you want to rate: ")
    if order_id.isdigit():
        conn = db.create_connection()
        if conn:
            query = "SELECT OrderID, RestaurantID FROM Orders WHERE UserID = %s AND OrderID = %s AND OrderStatus = 'Delivered'"
            order = db.execute_read_query(conn, query, (user_id, order_id))
            if order:
                rating = input("Enter your rating (1-5): ")
                comment = input("Enter your comment (optional): ")
                query = "INSERT INTO Ratings (UserID, RestaurantID, OrderID, Score, Comment) VALUES (%s, %s, %s, %s, %s)"
                db.execute_query(conn, query, (user_id, order[0]['RestaurantID'], order_id, rating, comment))
                print("Thank you for your feedback!")
            else:
                print("Order not found or not eligible for rating.")
        else:
            print("Failed to connect to the database.")
    else:
        print("Invalid order ID. Please try again.")
            
def update_order_status(restaurant_id):
    print("\n--- Update Order Status ---")
    print("Orders that can be updated to 'Ready for Pickup':")
    conn = db.create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    query = """
    SELECT OrderID, UserID, TotalPrice
    FROM Orders
    WHERE RestaurantID = %s AND OrderStatus = 'Preparing'
    """
    orders = db.execute_read_query(conn, query, (restaurant_id,))
    if not orders:
        print("No orders are currently being prepared.")
        return

    for order in orders:
        print(f"OrderID: {order['OrderID']}, UserID: {order['UserID']}, TotalPrice: ${order['TotalPrice']}")

    order_id = input("Enter Order ID to mark as 'Ready for Pickup': ")
    if not order_id.isdigit() or int(order_id) not in [order['OrderID'] for order in orders]:
        print("Invalid Order ID.")
        return

    update_query = """
    UPDATE Orders
    SET OrderStatus = 'Ready for Pickup'
    WHERE OrderID = %s AND RestaurantID = %s
    """
    db.execute_query(conn, update_query, (order_id, restaurant_id))
    print(f"Order {order_id} has been marked as 'Ready for Pickup'.")
            

def view_best_selling_items(restaurant_id):
    print(f"\n--- Best Selling Items for Restaurant ID {restaurant_id} ---")
    procedure_name = "GetBestSellingItems" 
    conn = db.create_connection()
    if conn is not None:
        best_selling_items = db.execute_stored_procedure(conn, procedure_name, [restaurant_id])
        if best_selling_items:
            for item in best_selling_items:
                print(f"{item[0]} - Quantity Sold: {item[1]}")  
        else:
            print("No sales data found.")
    else:
        print("Failed to connect to the database.")

def view_poorest_selling_items(restaurant_id):
    print(f"\n--- Poorest Selling Items for Restaurant ID {restaurant_id} ---")
    procedure_name = "GetPoorestSellingItems"  
    conn = db.create_connection()
    if conn is not None:
        poorest_selling_items = db.execute_stored_procedure(conn, procedure_name, [restaurant_id])
        if poorest_selling_items:
            for item in poorest_selling_items:
                print(f"{item[0]} - Quantity Sold: {item[1]}") 
        else:
            print("No sales data found.")
    else:
        print("Failed to connect to the database.")


def calculate_revenue(restaurant_id):
    print(f"\n--- Calculating Revenue for Restaurant ID {restaurant_id} ---")
    query = "SELECT SUM(TotalPrice) AS Revenue FROM Orders WHERE RestaurantID = %s AND OrderStatus = 'Delivered'"
    conn = db.create_connection()
    if conn is not None:
        revenue = db.execute_read_query(conn, query, (restaurant_id,))
        if revenue and revenue[0]['Revenue'] is not None:
            print(f"Total Revenue: ${revenue[0]['Revenue']}")
        else:
            print("No revenue found or no orders have been completed yet.")
    else:
        print("Failed to connect to the database.")            

def show_available_tags():
    print("\n--- Available Tags ---")
    query = "SELECT DISTINCT TagName FROM Tags ORDER BY TagName"
    conn = db.create_connection()
    if conn is not None:
        tags = db.execute_read_query(conn, query)
        if tags:
            for tag in tags:
                print(tag['TagName'])
        else:
            print("No tags found.")
    else:
        print("Failed to connect to the database.")

def get_restaurant_tags(restaurant_id):
    query = "SELECT GetRestaurantTagNames(%s) AS Tags"
    conn = db.create_connection()
    if conn is not None:
        tags = db.execute_read_query(conn, query, (restaurant_id,))
        if tags:
            return tags[0]['Tags']
        else:
            print("No tags found for this restaurant.")
    else:
        print("Failed to connect to the database.")


def filter_restaurants_by_rating(min_rating):
    print(f"\n--- Restaurants with rating {min_rating} and above ---")
    query = """
    SELECT RestaurantID, Name, Address, Rating
    FROM Restaurants
    WHERE Rating >= %s AND IsActive = TRUE
    """
    conn = db.create_connection()
    if conn is not None:
        restaurants = db.execute_read_query(conn, query, (min_rating,))
        if restaurants:
            for restaurant in restaurants:
                print(f"RestaurantID: {restaurant['RestaurantID']}, Name: {restaurant['Name']}, Address: {restaurant['Address']}, Rating: {restaurant['Rating']}")
        else:
            print(f"No restaurants found with rating {min_rating} and above.")
    else:
        print("Failed to connect to the database.")

def filter_restaurants_by_tag(tag_name):
    print(f"\n--- Restaurants with tag '{tag_name}' ---")
    query = """
    SELECT r.RestaurantID, r.Name, r.Address, r.Rating, GetRestaurantTagNames(r.RestaurantID) AS Tags
    FROM Restaurants r
    JOIN RestaurantTags rt ON r.RestaurantID = rt.RestaurantID
    JOIN Tags t ON rt.TagID = t.TagID
    WHERE t.TagName = %s AND r.IsActive = TRUE
    GROUP BY r.RestaurantID
    """
    conn = db.create_connection()
    if conn is not None:
        restaurants = db.execute_read_query(conn, query, (tag_name,))
        if restaurants:
            for restaurant in restaurants:
                print(f"RestaurantID: {restaurant['RestaurantID']}, Name: {restaurant['Name']}, Address: {restaurant['Address']}, Rating: {restaurant['Rating']}, Tags: {restaurant['Tags']}")
        else:
            print(f"No restaurants found with tag '{tag_name}'.")
    else:
        print("Failed to connect to the database.")


def view_menu(restaurant_id):
    print("\n--- Menu for Restaurant ID:", restaurant_id, "---")
    query = """
    SELECT MenuItemID, Name, Description, Price 
    FROM MenuItems 
    WHERE RestaurantID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        menu_items = db.execute_read_query(conn, query, (restaurant_id,))
        if menu_items:
            for item in menu_items:
                print(f"MenuItemID: {item['MenuItemID']}, Name: {item['Name']}, Description: {item['Description']}, Price: {item['Price']}")
        else:
            print("No menu items found for this restaurant.")
    else:
        print("Failed to connect to the database.")


def add_new_tag(restaurant_id, tag_name):
    
    conn = db.create_connection()
    tag_query = "SELECT TagID FROM Tags WHERE TagName = %s"
    tag_id = db.execute_read_query(conn, tag_query, (tag_name,))

    if not tag_id:
        insert_tag_query = "INSERT INTO Tags (TagName) VALUES (%s)"
        db.execute_query(conn, insert_tag_query, (tag_name,))
        tag_id = db.execute_read_query(conn, tag_query, (tag_name,))


    insert_restaurant_tag_query = "INSERT INTO RestaurantTags (RestaurantID, TagID) VALUES (%s, %s)"
    db.execute_query(conn, insert_restaurant_tag_query, (restaurant_id, tag_id[0]['TagID']))
    print(f"Tag '{tag_name}' added to restaurant ID {restaurant_id}.")


def remove_tag(restaurant_id, tag_name):
    conn = db.create_connection()
    tag_query = "SELECT TagID FROM Tags WHERE TagName = %s"
    tag_id = db.execute_read_query(conn, tag_query, (tag_name,))

    if tag_id:
        delete_restaurant_tag_query = "DELETE FROM RestaurantTags WHERE RestaurantID = %s AND TagID = %s"
        db.execute_query(conn, delete_restaurant_tag_query, (restaurant_id, tag_id[0]['TagID']))
        print(f"Tag '{tag_name}' removed from restaurant ID {restaurant_id}.")
    else:
        print(f"Tag '{tag_name}' not found.")


def show_available_tags():
    print("\n--- Available Tags ---")
    query = "SELECT TagName FROM Tags ORDER BY TagName"
    conn = db.create_connection()
    if conn is not None:
        tags = db.execute_read_query(conn, query)
        if tags:
            for tag in tags:
                print(tag['TagName'])
        else:
            print("No tags found.")
    else:
        print("Failed to connect to the database.")


def get_restaurant_id_by_owner(user_id):
    query = "SELECT RestaurantID FROM Restaurants WHERE OwnerID = %s"
    conn = db.create_connection()
    if conn is not None:
        result = db.execute_read_query(conn, query, (user_id,))
        if result:
            return result[0]['RestaurantID']
    return None



def view_restaurants():
    print("\n--- View Restaurants ---")
    query = "SELECT RestaurantID, Name, Address, Rating FROM Restaurants WHERE IsActive = TRUE"
    conn = db.create_connection()
    if conn is not None:
        restaurants = db.execute_read_query(conn, query)
        if restaurants:
            for restaurant in restaurants:
                print(f"RestaurantID: {restaurant['RestaurantID']}, Name: {restaurant['Name']}, Address: {restaurant['Address']}, Rating: {restaurant.get('Rating', 'N/A')}")
        else:
            print("No active restaurants found.")
    else:
        print("Failed to connect to the database.")
        
def update_my_restaurant(user_id):
    print("\n--- Update My Restaurant ---")
    restaurant_id = get_restaurant_id_by_owner(user_id)
    if not restaurant_id:
        print("No restaurant found for this owner.")
        return

    conn = db.create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    query = "SELECT Name, Address, IsActive FROM Restaurants WHERE RestaurantID = %s"
    restaurant = db.execute_read_query(conn, query, (restaurant_id,))
    
    if not restaurant:
        print("Restaurant not found.")
        return

    restaurant = restaurant[0]
    print(f"Current Details:\nName: {restaurant['Name']}\nAddress: {restaurant['Address']}\nActive: {'Yes' if restaurant['IsActive'] else 'No'}")
    new_name = input("Enter new name (press enter to keep current): ")
    new_address = input("Enter new address (press enter to keep current): ")
    new_status = input("Is restaurant active? (yes/no): ").lower() == 'yes'

    update_query = """
    UPDATE Restaurants
    SET Name = IF(LENGTH(%s) = 0, Name, %s), 
        Address = IF(LENGTH(%s) = 0, Address, %s),
        IsActive = %s
    WHERE RestaurantID = %s
    """
    db.execute_query(conn, update_query, (new_name, new_name, new_address, new_address, new_status, restaurant_id))
    print("Restaurant details updated successfully.")

def manage_menu(restaurant_id):
    print("\n--- Manage Menu for Restaurant ID:", restaurant_id, "---")
    while True:
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. Return")
        choice = input("Choose an action: ")
        
        if choice == '1':
            add_menu_item(restaurant_id)
        elif choice == '2':
            update_menu_item(restaurant_id)
        elif choice == '3':
            delete_menu_item(restaurant_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")
            
def add_menu_item(restaurant_id):
    name = input("Enter menu item name: ")
    description = input("Enter description: ")
    price = input("Enter price: ")
    query = "INSERT INTO MenuItems (RestaurantID, Name, Description, Price) VALUES (%s, %s, %s, %s)"
    db.execute_query(db.create_connection(), query, (restaurant_id, name, description, price))
    print("Menu item added successfully.")

def update_menu_item(restaurant_id):
    menu_item_id = input("Enter Menu Item ID to update: ")
    new_name = input("Enter new name (press enter to keep current): ")
    new_description = input("Enter new description (press enter to keep current): ")
    new_price = input("Enter new price (press enter to keep current): ")
    query = """
    UPDATE MenuItems
    SET Name = IF(LENGTH(%s) = 0, Name, %s),
        Description = IF(LENGTH(%s) = 0, Description, %s),
        Price = IF(LENGTH(%s) = 0, Price, %s)
    WHERE MenuItemID = %s AND RestaurantID = %s
    """
    db.execute_query(db.create_connection(), query, (new_name, new_name, new_description, new_description, new_price, new_price, menu_item_id, restaurant_id))
    print("Menu item updated successfully.")

def delete_menu_item(restaurant_id):
    menu_item_id = input("Enter Menu Item ID to delete: ")
    query = "DELETE FROM MenuItems WHERE MenuItemID = %s AND RestaurantID = %s"
    db.execute_query(db.create_connection(), query, (menu_item_id, restaurant_id))
    print("Menu item deleted successfully.")
    
def view_my_restaurant(user_id):
    print("\n--- View My Restaurant ---")
    query = """
    SELECT r.RestaurantID, r.Name, r.Address, r.Rating
    FROM Restaurants r
    INNER JOIN Users u ON r.OwnerID = u.UserID
    WHERE u.UserID = %s AND r.IsActive = TRUE
    """
    conn = db.create_connection()
    if conn is not None:
        restaurant = db.execute_read_query(conn, query, (user_id,))
        if restaurant:
            for r in restaurant:
                print(f"RestaurantID: {r['RestaurantID']}, Name: {r['Name']}, Address: {r['Address']}, Rating: {r.get('Rating', 'N/A')}")
        else:
            print("No restaurant found for this owner.")
    else:
        print("Failed to connect to the database.")
        
def view_orders_for_restaurant(restaurant_id):
    print("\n--- View Orders for My Restaurant ---")
    query = """
    SELECT OrderID, UserID, OrderStatus, TotalPrice
    FROM Orders
    WHERE RestaurantID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        orders = db.execute_read_query(conn, query, (restaurant_id,))
        if orders:
            for order in orders:
                print(f"OrderID: {order['OrderID']}, UserID: {order['UserID']}, Status: {order['OrderStatus']}, TotalPrice: ${order['TotalPrice']}")
        else:
            print("No orders found for this restaurant.")
    else:
        print("Failed to connect to the database.")
        
        
def view_ratings_for_restaurant(restaurant_id):
    print("\n--- View Ratings for My Restaurant ---")
    query = """
    SELECT Score, Comment, RatingDate
    FROM Ratings
    WHERE RestaurantID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        ratings = db.execute_read_query(conn, query, (restaurant_id,))
        if ratings:
            for rating in ratings:
                print(f"Score: {rating['Score']}, Comment: {rating.get('Comment', 'N/A')}, Date: {rating['RatingDate']}")
        else:
            print("No ratings found for this restaurant.")
    else:
        print("Failed to connect to the database.")

        
        
