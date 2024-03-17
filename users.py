import db

def sign_up():
    print("\n--- Sign Up ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    user_type = ''
    while user_type not in ['Customer', 'Driver', 'RestaurantAdmin']:
        user_type = input("Enter user type (Customer, Driver, RestaurantAdmin): ")
        if user_type.lower() not in ['customer', 'driver', 'restaurantadmin']:
            print("Invalid user type. Please choose from Customer, Driver, or RestaurantAdmin.")

    conn = db.create_connection()
    if conn is not None:
        try:
            conn.start_transaction()
            query_users = "INSERT INTO Users (Username, Password, Email, UserType) VALUES (%s, %s, %s, %s)"
            db.execute_query(conn, query_users, (username, password, email, user_type))
            db.execute_stored_procedure(conn, 'sp_add_user', (username, password, user_type))
            conn.commit()
            print(f"User {username} signed up successfully.")
            return {
                'Username': username,
                'UserType': user_type,
                'Email': email
            }
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
    else:
        print("Failed to connect to the database.")

def sign_in():
    print("\n--- Sign In ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = db.create_connection()
    if conn is not None:
        cursor = conn.cursor()


        cursor.callproc('sp_authenticate', [username, password])

   
        auth_result = None

     
        for result in cursor.stored_results():
            result_row = result.fetchone() 
            if result_row:
                auth_result = result_row[0]  

        if auth_result:
            fetch_query = "SELECT UserID, Username, UserType, Email FROM Users WHERE Username = %s"
            user_details = db.execute_read_query(conn, fetch_query, [username])
            
            if user_details:
                user_session = user_details[0]
                print(f"User {user_session['Username']} signed in successfully.")
                return user_session
            else:
                print("Failed to retrieve user details.")
        else:
            print("Invalid username or password.")
            return None
    else:
        print("Failed to connect to the database.")
        return None

def update_user_info(user_id):
    print("\n--- Update User Information ---")
    email = input("Enter new email (leave blank to keep current): ")
    user_type = input("Enter new user type (Customer, Driver, RestaurantAdmin, PlatformAdmin) (leave blank to keep current): ")
    
    query = """
    UPDATE Users SET Email = IF(LENGTH(%s) = 0, Email, %s), 
                      UserType = IF(LENGTH(%s) = 0, UserType, %s)
    WHERE UserID = %s
    """
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (email, email, user_type, user_type, user_id))
        print("User information updated successfully.")
    else:
        print("Failed to connect to the database.")

