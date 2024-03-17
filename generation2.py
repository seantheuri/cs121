import csv
import random
from faker import Faker

faker = Faker()


with open('orders.csv', newline='') as file:
    reader = csv.DictReader(file)
    orders = [row for row in reader]

with open('menuitems.csv', newline='') as file:
    reader = csv.DictReader(file)
    menu_items = [row for row in reader]


with open('orderdetails.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['OrderDetailID', 'OrderID', 'MenuItemID', 'Quantity'])
    order_detail_id = 1
    for order in orders:

        for _ in range(random.randint(1, 5)):
            writer.writerow([
                order_detail_id,
                order['OrderID'],
                random.choice(menu_items)['MenuItemID'],
                random.randint(1, 3) 
            ])
            order_detail_id += 1
        

with open('payments.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['PaymentID', 'OrderID', 'Amount', 'PaymentMethod', 'PaymentStatus', 'PaymentDate'])
    payment_id = 1
    for order in orders:
        payment_date = faker.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')

        writer.writerow([
            payment_id,
            order['OrderID'],
            order['TotalPrice'], 
            random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
            random.choice(['Completed', 'Pending', 'Failed']),
            payment_date
        ])
        payment_id += 1