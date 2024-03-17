# admin.py
import db
import llm_integration

def admin_interface(user_session):
    print("\nAdmin Menu:")
    print("Tell me what you would like to do, for example, 'List users', 'List drivers', 'List restaurants', 'List menus', 'Delete a user', 'Update user type', 'View order statistics', 'Add a restaurant', 'Calculate restaurant revenue', 'View average order time', or 'Return to main menu'.")

    while True:
        user_input = input("Your request: ")
        response_text = llm_integration.process_natural_language_query(user_input, user_session)
        print("LLM Response:", response_text)

        if "list_users" in response_text:
            list_users()
        elif "list_drivers" in response_text:
            list_drivers()
        elif "list_restaurants" in response_text:
            list_restaurants()
        elif "list_menus" in response_text:
            list_menus()
        elif "delete_user" in response_text:
            user_id = input("Enter User ID to delete: ")
            delete_user(user_id)
        elif "update_user_type" in response_text:
            user_id = input("Enter User ID to update type: ")
            new_type = input("Enter new user type: ")
            update_user_type(user_id, new_type)
        elif "view_order_statistics" in response_text:
            view_order_statistics()
        elif "add_restaurant" in response_text:
            add_restaurant()
        elif "calculate_revenue" in response_text:
            restaurant_id = input("Enter Restaurant ID for revenue calculation: ")
            calculate_revenue(restaurant_id)
        elif "view_average_order_time" in response_text:
            view_average_order_time()
        elif "return_to_main_menu" in response_text:
            break
        else:
            print("I didn't understand that. Can you please rephrase or specify your request?")

def list_users():
    print("\n--- List of Users ---")
    query = "SELECT UserID, Username, UserType, Email FROM Users"
    conn = db.create_connection()
    if conn is not None:
        users = db.execute_read_query(conn, query)
        if users:
            for user in users:
                print(f"UserID: {user['UserID']}, Username: {user['Username']}, Type: {user['UserType']}, Email: {user['Email']}")
        else:
            print("No users found.")
    else:
        print("Failed to connect to the database.")

def delete_user(user_id):
    print("\n--- Delete User ---")
    query = "DELETE FROM Users WHERE UserID = %s"
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (user_id,))
        print(f"User with ID {user_id} has been deleted.")
    else:
        print("Failed to connect to the database.")

def update_user_type(user_id, new_type):
    print("\n--- Update User Type ---")
    query = "UPDATE Users SET UserType = %s WHERE UserID = %s"
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (new_type, user_id))
        print(f"User with ID {user_id} has been updated to {new_type}.")
    else:
        print("Failed to connect to the database.")

def view_order_statistics():
    print("\n--- Order Statistics ---")
    query = "SELECT OrderStatus, COUNT(*) AS Count FROM Orders GROUP BY OrderStatus"
    conn = db.create_connection()
    if conn is not None:
        stats = db.execute_read_query(conn, query)
        if stats:
            for stat in stats:
                print(f"Status: {stat['OrderStatus']}, Count: {stat['Count']}")
        else:
            print("No order statistics found.")
    else:
        print("Failed to connect to the database.")

def add_restaurant():
    print("\n--- Add New Restaurant ---")
    name = input("Enter restaurant name: ")
    address = input("Enter restaurant address: ")
    query = "INSERT INTO Restaurants (Name, Address, IsActive) VALUES (%s, %s, TRUE)"
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (name, address))
        print(f"Restaurant {name} added successfully.")
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
            print("No revenue data found.")
    else:
        print("Failed to connect to the database.")

def view_average_order_time():
    print("\n--- Average Order Time ---")
    query = """
    SELECT RestaurantID, AVG(TIMESTAMPDIFF(MINUTE, OrderTime, NOW())) AS AvgTime
    FROM Orders
    WHERE OrderStatus = 'Delivered'
    GROUP BY RestaurantID
    """
    conn = db.create_connection()
    if conn is not None:
        avg_times = db.execute_read_query(conn, query)
        if avg_times:
            for avg_time in avg_times:
                print(f"Restaurant ID: {avg_time['RestaurantID']}, Average Time: {avg_time['AvgTime']} minutes")
        else:
            print("No average time data found.")
    else:
        print("Failed to connect to the database.")


def list_drivers():
    print("\n--- List of Drivers ---")
    query = """
    SELECT u.UserID, u.Username, u.Email, d.LicenseNumber, d.VehicleType
    FROM Users u
    JOIN Drivers d ON u.UserID = d.DriverID
    """
    conn = db.create_connection()
    if conn is not None:
        drivers = db.execute_read_query(conn, query)
        if drivers:
            for driver in drivers:
                print(f"UserID: {driver['UserID']}, Username: {driver['Username']}, Email: {driver['Email']}, License Number: {driver['LicenseNumber']}, Vehicle Type: {driver['VehicleType']}")
        else:
            print("No drivers found.")
    else:
        print("Failed to connect to the database.")
        

def list_restaurants():
    print("\n--- List of Restaurants ---")
    query = "SELECT RestaurantID, Name, Address, IsActive FROM Restaurants"
    conn = db.create_connection()
    if conn is not None:
        restaurants = db.execute_read_query(conn, query)
        if restaurants:
            for restaurant in restaurants:
                active_status = "Active" if restaurant['IsActive'] else "Inactive"
                print(f"RestaurantID: {restaurant['RestaurantID']}, Name: {restaurant['Name']}, Address: {restaurant['Address']}, Status: {active_status}")
        else:
            print("No restaurants found.")
    else:
        print("Failed to connect to the database.")
        
def list_menus():
    print("\n--- List of Menus ---")
    query = "SELECT m.MenuItemID, m.Name, m.Description, m.Price, r.Name AS RestaurantName FROM MenuItems m JOIN Restaurants r ON m.RestaurantID = r.RestaurantID"
    conn = db.create_connection()
    if conn is not None:
        menu_items = db.execute_read_query(conn, query)
        if menu_items:
            for item in menu_items:
                print(f"MenuItemID: {item['MenuItemID']}, Name: {item['Name']}, Description: {item['Description']}, Price: {item['Price']}, Restaurant: {item['RestaurantName']}")
        else:
            print("No menu items found.")
    else:
        print("Failed to connect to the database.")