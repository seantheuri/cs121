import csv


with open('users.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    users = [row for row in reader]


with open('user_info.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['username', 'password', 'usertype'])

    for user in users:
        writer.writerow([user['Username'], user['Password'], user['UserType']])
