# drivers.py
import db
import llm_integration
 

def driver_interface(user_session):
    print("\nDriver Menu:")
    print("Tell me what you would like to do, for example, 'View available orders', 'Accept an order', 'Update delivery status', 'Update my status', 'Update vehicle details', 'View completed orders' or 'Return to main menu'.")

    accepted_orders = [] 

    while True:
        user_input = input("Your request: ")
        response_text = llm_integration.process_natural_language_query(user_input, user_session)
        print("LLM Response:", response_text)

        if "view_available_orders" in response_text:
            view_available_orders()
        elif "accept_order" in response_text:
            available_orders = view_available_orders()
            if not available_orders:
                continue

            order_id = input("Enter Order ID to accept: ")
            if order_id.isdigit() and int(order_id) in available_orders:
                accept_order(user_session['UserID'], int(order_id))
            else:
                print("Invalid Order ID. Please try again.")
        elif "update_delivery_status" in response_text:
            if not accepted_orders:
                print("You have no accepted orders to update.")
                continue
            order_id = input("Enter Order ID to update status: ")
            if order_id.isdigit() and int(order_id) in accepted_orders:
                new_status = input("Enter new status ('Delivered' or 'Cancelled'): ")
                if new_status in ['Delivered', 'Cancelled']:
                    update_delivery_status(int(order_id), new_status)
                else:
                    print("Invalid status. Please enter 'Delivered' or 'Cancelled'.")
            else:
                print("Invalid Order ID or you have not accepted this order. Please try again.")
        elif "view_completed_orders" in response_text:
            view_completed_orders(user_session['UserID'])
        elif "update_driver_status" in response_text:
            new_status = input("Are you active? (yes/no): ")
            update_driver_status(user_session['UserID'], new_status == 'yes')
        elif "update_vehicle_info" in response_text:
            license_number = input("Enter new license number: ")
            vehicle_type = input("Enter new vehicle type: ")
            update_vehicle_details(user_session['UserID'], license_number, vehicle_type)
        elif "view_my_details" in response_text:
            view_driver_details(user_session['UserID'])
        elif "return_to_main_menu" in response_text:
            break
        else:
            print("I didn't understand that. Can you please rephrase or specify your request?")
            
def view_driver_details(driver_id):
    query = """
    SELECT LicenseNumber, VehicleType, IsActive
    FROM Drivers
    WHERE DriverID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        driver_details = db.execute_read_query(conn, query, (driver_id,))
        if driver_details:
            details = driver_details[0]
            print(f"\nDriver Details:\nLicense Number: {details['LicenseNumber']}\nVehicle Type: {details['VehicleType']}\nStatus: {'Active' if details['IsActive'] else 'Inactive'}")
        else:
            print("Driver details not found.")
    else:
        print("Failed to connect to the database.")        
            
def update_driver_status(driver_id, is_active):
    query = "UPDATE Drivers SET IsActive = %s WHERE DriverID = %s"
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (is_active, driver_id))
        status = "active" if is_active else "inactive"
        print(f"Driver status updated to {status}.")
    else:
        print("Failed to connect to the database.")

def update_vehicle_details(driver_id, license_number, vehicle_type):
    query = """
    UPDATE Drivers 
    SET LicenseNumber = %s, VehicleType = %s 
    WHERE DriverID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (license_number, vehicle_type, driver_id))
        print("Vehicle details updated successfully.")
    else:
        print("Failed to connect to the database.")


def view_completed_orders(driver_id):
    print("\n--- View Completed Orders ---")
    query = """
    SELECT OrderID, RestaurantID, OrderStatus, TotalPrice
    FROM Orders
    WHERE DriverID = %s AND OrderStatus IN ('Delivered', 'Cancelled')
    """
    conn = db.create_connection()

    if conn is not None:
        orders = db.execute_read_query(conn, query, (driver_id,))
        if orders:
            for order in orders:
                print(f"OrderID: {order['OrderID']}, RestaurantID: {order['RestaurantID']}, Status: {order['OrderStatus']}, Total Price: {order['TotalPrice']}")
        else:
            print("No completed orders found.")
    else:
        print("Failed to connect to the database.")


def view_available_orders():
    print("\n--- View Available Orders ---")
    query = "SELECT OrderID, RestaurantID, OrderStatus FROM Orders WHERE OrderStatus = 'Ready for Pickup'"
    conn = db.create_connection()
    available_orders = []

    if conn is not None:
        orders = db.execute_read_query(conn, query)
        if orders:
            for order in orders:
                print(f"OrderID: {order['OrderID']}, RestaurantID: {order['RestaurantID']}, Status: {order['OrderStatus']}")
                available_orders.append(order['OrderID'])
        else:
            print("No available orders found.")
    else:
        print("Failed to connect to the database.")

    return available_orders

def accept_order(driver_id, order_id):
    print("\n--- Accept Order ---")
    query = "UPDATE Orders SET DriverID = %s, OrderStatus = 'En Route' WHERE OrderID = %s"
    conn = db.create_connection()

    if conn is not None:
        db.execute_query(conn, query, (driver_id, order_id))
        print(f"Order {order_id} accepted by driver {driver_id}.")
    else:
        print("Failed to connect to the database.")

def update_delivery_status(order_id, new_status):
    print("\n--- Update Delivery Status ---")
    query = "UPDATE Orders SET OrderStatus = %s WHERE OrderID = %s"
    conn = db.create_connection()

    if conn is not None:
        db.execute_query(conn, query, (new_status, order_id))
        print(f"Order {order_id} status updated to {new_status}.")
    else:
        print("Failed to connect to the database.")