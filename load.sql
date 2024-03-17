SET GLOBAL local_infile = 'ON';

DELIMITER !

-- Function to generate a salt
CREATE FUNCTION make_salt(num_chars INT) RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';
    SET num_chars = LEAST(20, num_chars);
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;
    RETURN salt;
END !
DELIMITER ;

-- Load Users data
LOAD DATA LOCAL INFILE 'users.csv' INTO TABLE Users
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(UserID, Username, Password, Email, UserType, @CreationDate)
SET CreationDate = STR_TO_DATE(@CreationDate, '%Y-%m-%d %H:%i:%s');
SHOW WARNINGS;

-- Load Restaurants data
LOAD DATA LOCAL INFILE 'restaurants.csv' INTO TABLE Restaurants
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(RestaurantID, Name, Address, Rating, @IsActive, OwnerID)
SET IsActive = (@IsActive = 1);
SHOW WARNINGS;

-- Load Drivers data
LOAD DATA LOCAL INFILE 'drivers.csv' INTO TABLE Drivers
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(DriverID, LicenseNumber, VehicleType, @IsActive)
SET IsActive = (@IsActive = 1);
SHOW WARNINGS;

-- Load MenuItems data
LOAD DATA LOCAL INFILE 'menuitems.csv' INTO TABLE MenuItems
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
SHOW WARNINGS;

-- Load Orders data
LOAD DATA LOCAL INFILE 'orders.csv' INTO TABLE Orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
SHOW WARNINGS;

-- Load OrderDetails data
LOAD DATA LOCAL INFILE 'orderdetails.csv' INTO TABLE OrderDetails
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
SHOW WARNINGS;

-- Load Payments data
LOAD DATA LOCAL INFILE 'payments.csv' INTO TABLE Payments
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(PaymentID, OrderID, Amount, PaymentMethod, PaymentStatus, @PaymentDate)
SET PaymentDate = STR_TO_DATE(@PaymentDate, '%Y-%m-%d %H:%i:%s');
SHOW WARNINGS;

-- Load Ratings data
LOAD DATA LOCAL INFILE 'ratings.csv' INTO TABLE Ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(RatingID, UserID, RestaurantID, DriverID, OrderID, Score, Comment, @RatingDate)
SET RatingDate = STR_TO_DATE(@RatingDate, '%Y-%m-%d %H:%i:%s');
SHOW WARNINGS;

-- Load Tags data
LOAD DATA LOCAL INFILE 'tags.csv' INTO TABLE Tags
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
SHOW WARNINGS;

-- Load RestaurantTags data
LOAD DATA LOCAL INFILE 'restauranttags.csv' INTO TABLE RestaurantTags
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (RestaurantID, TagID);

SHOW WARNINGS;

LOAD DATA LOCAL INFILE 'user_info.csv' INTO TABLE user_info
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(username, @plain_password, @UserType)
SET
  salt = make_salt(8),
  password_hash = SHA2(CONCAT(salt, @plain_password), 256),
  UserType = IF(@UserType IN ('Customer', 'Driver', 'RestaurantAdmin', 'PlatformAdmin'), @UserType, 'Customer');
SHOW WARNINGS;