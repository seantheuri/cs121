import db  
import users
import restaurants
import orders
import drivers
import ratings
import admin
import customers

user_session = None

def main_menu():
    global user_session  
    while True:
        print("\nWelcome to the Food Delivery App")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user_session = users.sign_in() 
            if user_session:
                if user_session['UserType'] == 'Customer':
                    customers.customer_interface(user_session)
                elif user_session['UserType'] == 'Driver':
                    drivers.driver_interface(user_session)
                elif user_session['UserType'] == 'RestaurantAdmin':
                    restaurants.restaurant_interface(user_session)
                elif user_session['UserType'] == 'PlatformAdmin':
                    admin.admin_interface(user_session)
        elif choice == '2':
            user_session = users.sign_up()  
            if user_session:
                if user_session['UserType'] == 'Customer':
                    customers.customer_interface(user_session)
                elif user_session['UserType'] == 'Driver':
                    drivers.driver_interface(user_session)
                elif user_session['UserType'] == 'RestaurantAdmin':
                    restaurants.restaurant_interface(user_session)
                elif user_session['UserType'] == 'PlatformAdmin':
                    admin.admin_interface(user_session)
        elif choice == '3':
            print("Thank you for using the Food Delivery App. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
        

if __name__ == "__main__":
    main_menu()