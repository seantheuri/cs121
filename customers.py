import db
import restaurants 
import orders
import llm_integration

def customer_interface(user_session):
    print("\nCustomer Menu:")
    print("Tell me what you would like to do, for example, 'View restaurants', 'Place an order', 'View menu', 'Check order status', 'Filter restaurants', 'View previous orders', or 'Return to main menu'.")

    while True:
        user_input = input("Your request: ")
        response_text = llm_integration.process_natural_language_query(user_input, user_session)
        print("LLM Response:", response_text)

        if "view_restaurants" in response_text:
            restaurants.view_restaurants()
        elif "view_menu" in response_text:
            restaurants.view_restaurants()
            restaurant_id = input("Please enter the ID of the restaurant to view its menu: ")
            if restaurant_id.isdigit():
                restaurants.view_menu(int(restaurant_id))
            else:
                print("Invalid restaurant ID. Please try again.")
        elif "place_order" in response_text:
            restaurants.view_restaurants()
            restaurant_id = input("Please enter the ID of the restaurant you want to order from: ")
            if restaurant_id.isdigit():
                orders.place_order_flow(user_session['UserID'], int(restaurant_id))
            else:
                print("Invalid restaurant ID. Please try again.")
        elif "check_order_status" in response_text:
            orders.view_order_status(user_session['UserID'])
        elif "filter_restaurants" in response_text:
            filter_criteria = input("Enter filter type (tag/rating): ")
            if filter_criteria == "tag":
                print("Available tags:")
                restaurants.show_available_tags()
                tag_name = input("Enter the tag name: ")
                restaurants.filter_restaurants_by_tag(tag_name)
            elif filter_criteria == "rating":
                rating = float(input("Enter the minimum rating: "))
                restaurants.filter_restaurants_by_rating(rating)
            else:
                print("Invalid filter type.")
        elif "view_previous_orders" in response_text:
            orders.view_previous_orders(user_session['UserID'])
        elif "view_current_orders" in response_text:
            orders.view_current_orders(user_session['UserID'])
        elif "rate_restaurant" in response_text:
            restaurants.rate_restaurant(user_session['UserID'])
        elif "search_restaurants" in response_text:
            search_query = input("Enter restaurant name or keyword to search: ")
            restaurants.search_restaurants(search_query)
        elif "return_to_main_menu" in response_text:
            break
        else:
            print("I didn't understand that. Can you please rephrase or specify your request?")