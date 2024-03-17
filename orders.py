# orders.py
import db

def view_previous_orders(user_id):
    print("\n--- View Previous Orders ---")
    query = """
    SELECT OrderID, RestaurantID, OrderStatus, TotalPrice, OrderTime
    FROM Orders
    WHERE UserID = %s AND OrderStatus IN ('Delivered', 'Cancelled')
    ORDER BY OrderTime DESC
    """
    conn = db.create_connection()
    if conn is not None:
        orders = db.execute_read_query(conn, query, (user_id,))
        if orders:
            for order in orders:
                print(f"OrderID: {order['OrderID']}, RestaurantID: {order['RestaurantID']}, Status: {order['OrderStatus']}, Total Price: {order['TotalPrice']}, Order Time: {order['OrderTime']}")
        else:
            print("No previous orders found.")
    else:
        print("Failed to connect to the database.")

def view_current_orders(user_id):
    print("\n--- View Current Orders ---")
    query = """
    SELECT OrderID, RestaurantID, OrderStatus, TotalPrice, OrderTime
    FROM Orders
    WHERE UserID = %s AND OrderStatus NOT IN ('Delivered', 'Cancelled')
    ORDER BY OrderTime DESC
    """
    conn = db.create_connection()
    if conn is not None:
        orders = db.execute_read_query(conn, query, (user_id,))
        if orders:
            for order in orders:
                print(f"OrderID: {order['OrderID']}, RestaurantID: {order['RestaurantID']}, Status: {order['OrderStatus']}, Total Price: {order['TotalPrice']}, Order Time: {order['OrderTime']}")
        else:
            print("No current orders found.")
    else:
        print("Failed to connect to the database.")

def view_order_status(user_id):
    print("\n--- Order Status ---")
    query = """
    SELECT OrderID, RestaurantID, OrderStatus, TotalPrice, OrderTime
    FROM Orders
    WHERE UserID = %s
    ORDER BY OrderTime DESC
    """
    conn = db.create_connection()
    if conn is not None:
        orders = db.execute_read_query(conn, query, (user_id,))
        if orders:
            print(f"Order history for user {user_id}:")
            for order in orders:
                print(f"OrderID: {order['OrderID']}, RestaurantID: {order['RestaurantID']}, Status: {order['OrderStatus']}, Total Price: {order['TotalPrice']}, Order Time: {order['OrderTime']}")
        else:
            print("No orders found for this user.")
    else:
        print("Failed to connect to the database.")

def view_menu(restaurant_id):
    print(f"\n--- Menu for Restaurant ID {restaurant_id} ---")
    menu_items = db.execute_read_query(db.create_connection(), "SELECT MenuItemID, Name, Price FROM MenuItems WHERE RestaurantID = %s", (restaurant_id,))
    for item in menu_items:
        print(f"{item['MenuItemID']}: {item['Name']} - ${item['Price']}")
        
def place_order_flow(user_id, restaurant_id):
    view_menu(restaurant_id)

    print("\nPlease select items to order. Enter 'done' when finished.")
    order_id = create_order(user_id, restaurant_id) 

    if order_id is None:
        print("Failed to create order.")
        return

    while True:
        item_id = input("Enter menu item ID to order (or 'done' to finish): ")
        if item_id.lower() == 'done':
            break

        quantity = int(input("Quantity: "))
        add_item_to_order(order_id, item_id, quantity)

    total_price = calculate_total_order_price(order_id)
    if total_price > 0:
        print(f"Your order total is: ${total_price}")


        payment_method = input("Please choose a payment method (Credit Card, Debit Card, PayPal): ")
        while payment_method.lower() not in ['credit card', 'debit card', 'paypal', 'cash']:
            print("Invalid payment method. Please try again.")
            payment_method = input("Please choose a payment method (Credit Card, Debit Card, PayPal): ")


        process_payment(order_id, total_price, payment_method)
        print("Payment successful. Your order has been placed.")
    else:
        print("No items selected. Order not placed.")
        
def process_payment(order_id, total_price, payment_method):

    conn = db.create_connection()
    query = """
    INSERT INTO Payments (OrderID, Amount, PaymentMethod, PaymentStatus) 
    VALUES (%s, %s, %s, 'Completed');
    """
    db.execute_query(conn, query, (order_id, total_price, payment_method))

    update_query = "UPDATE Orders SET TotalPrice = %s WHERE OrderID = %s;"
    db.execute_query(conn, update_query, (total_price, order_id))

def create_order(user_id, restaurant_id):
    conn = db.create_connection()
    query = """
        INSERT INTO Orders (UserID, RestaurantID, OrderStatus, TotalPrice) 
        VALUES (%s, %s, 'Placed', 0.00);
    """
    order_id = db.execute_query(conn, query, (user_id, restaurant_id), return_id=True)
    return order_id

def add_item_to_order(order_id, item_id, quantity):
    conn = db.create_connection()
    query = "CALL AddItemToOrder(%s, %s, %s);"
    db.execute_query(conn, query, (order_id, item_id, quantity))

def calculate_total_order_price(order_id):
    conn = db.create_connection()
    query = "SELECT CalculateTotalOrderPrice(%s) AS TotalPrice;"
    result = db.execute_read_query(conn, query, (order_id,))
    if result:
        return result[0]['TotalPrice']
    return 0
          
        
        
   


        

