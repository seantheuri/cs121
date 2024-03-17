# ratings.py
import db

def rate_restaurant(user_id, restaurant_id, score, comment=None):
    print("\n--- Rate Restaurant ---")
    query = """
    INSERT INTO Ratings (UserID, RestaurantID, Score, Comment, RatingDate) VALUES (%s, %s, %s, %s, NOW())
    """
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (user_id, restaurant_id, score, comment))
        print(f"Restaurant {restaurant_id} rated successfully.")
    else:
        print("Failed to connect to the database.")

def rate_driver(user_id, driver_id, order_id, score, comment=None):
    print("\n--- Rate Driver ---")
    query = """
    INSERT INTO Ratings (UserID, DriverID, OrderID, Score, Comment, RatingDate) VALUES (%s, %s, %s, %s, %s, NOW())
    """
    conn = db.create_connection()
    if conn is not None:
        db.execute_query(conn, query, (user_id, driver_id, order_id, score, comment))
        print(f"Driver {driver_id} rated successfully.")
    else:
        print("Failed to connect to the database.")

def view_ratings(target_id, rating_type):
    print("\n--- View Ratings ---")
    if rating_type == 'restaurant':
        query = """
        SELECT Score, Comment, RatingDate FROM Ratings WHERE RestaurantID = %s
        """
    elif rating_type == 'driver':
        query = """
        SELECT Score, Comment, RatingDate FROM Ratings WHERE DriverID = %s
        """
    else:
        print("Invalid rating type specified.")
        return
    
    conn = db.create_connection()
    if conn is not None:
        ratings = db.execute_read_query(conn, query, (target_id,))
        if ratings:
            for rating in ratings:
                print(f"Score: {rating[0]}, Comment: {rating[1] if rating[1] else 'N/A'}, Date: {rating[2]}")
        else:
            print(f"No ratings found for the specified {rating_type}.")
    else:
        print("Failed to connect to the database.")
        
def view_ratings_for_restaurant(restaurant_id):
    print("\n--- View Ratings for My Restaurant ---")
    query = """
    SELECT r.Score, r.Comment, r.RatingDate
    FROM Ratings r
    WHERE r.RestaurantID = %s
    ORDER BY r.RatingDate DESC
    """
    conn = db.create_connection()
    if conn is not None:
        ratings = db.execute_read_query(conn, query, (restaurant_id,))
        if ratings:
            for rating in ratings:
                score = rating['Score']
                comment = rating['Comment'] if rating['Comment'] else 'No comment provided'
                date = rating['RatingDate']
                print(f"Score: {score}, Comment: {comment}, Date: {date}")
        else:
            print("No ratings found for this restaurant.")
    else:
        print("Failed to connect to the database.")
