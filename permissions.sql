-- Drop the administrative user if it already exists
DROP USER IF EXISTS 'admin_user'@'localhost';
-- Create the administrative user
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin_password';

-- Drop the client user if it already exists
DROP USER IF EXISTS 'client_user'@'localhost';

-- Create the client user
CREATE USER 'client_user'@'localhost' IDENTIFIED BY 'client_password';

-- Grant all privileges to the admin user on your database
GRANT ALL PRIVILEGES ON cs121.* TO 'admin_user'@'localhost';

-- Grant only select privileges to the client user on your database
GRANT SELECT ON cs121.* TO 'client_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
