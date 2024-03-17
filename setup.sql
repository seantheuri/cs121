DROP TABLE IF EXISTS OrderDetails, Payments, Ratings, Orders, MenuItems, Restaurants, Drivers, RestaurantTags, Tags, Users, User_info CASCADE;

-- Users Table
-- Stores information about users
CREATE TABLE Users (
    UserID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    UserType ENUM('Customer', 'Driver', 'RestaurantAdmin', 'PlatformAdmin') NOT NULL,
    CreationDate DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- UserInfo Table for storing user credentials and salts
CREATE TABLE user_info (
    username VARCHAR(255) NOT NULL UNIQUE,
    salt CHAR(8) NOT NULL,
    password_hash BINARY(64) NOT NULL,
    UserType ENUM('Customer', 'Driver', 'RestaurantAdmin', 'PlatformAdmin') NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES Users(Username) ON DELETE CASCADE
);

-- Restaurants Table
-- Stores information about restaurants
CREATE TABLE Restaurants (
    RestaurantID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Rating DECIMAL(3, 2),
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    OwnerID BIGINT UNSIGNED,
    FOREIGN KEY (OwnerID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- MenuItems Table
-- Stores information about menu items offered by restaurants
CREATE TABLE MenuItems (
    MenuItemID INT AUTO_INCREMENT PRIMARY KEY,
    RestaurantID INT NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) ON DELETE CASCADE
);

-- Orders Table
-- Stores information about orders placed by users
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID BIGINT UNSIGNED NOT NULL,
    DriverID BIGINT UNSIGNED,
    RestaurantID INT NOT NULL,
    OrderStatus ENUM('Placed', 'Preparing', 'Ready for Pickup', 'En Route', 'Delivered', 'Cancelled') NOT NULL,
    OrderTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (DriverID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) ON DELETE CASCADE
);

-- OrderDetails Table
-- Stores detailed information about each item in an order
CREATE TABLE OrderDetails (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    MenuItemID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (MenuItemID) REFERENCES MenuItems(MenuItemID) ON DELETE CASCADE
);

-- Payments Table
-- Stores information about payments for orders
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentMethod ENUM('Credit Card', 'Debit Card', 'PayPal', 'Cash') NOT NULL,
    PaymentStatus ENUM('Completed', 'Pending', 'Failed') NOT NULL,
    PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE
);

-- Ratings Table
-- Stores ratings and comments given by users to restaurants or drivers
CREATE TABLE Ratings (
    RatingID INT AUTO_INCREMENT PRIMARY KEY,
    UserID BIGINT UNSIGNED NOT NULL,
    RestaurantID INT,
    DriverID BIGINT UNSIGNED,
    OrderID INT NOT NULL,
    Score INT NOT NULL,
    Comment TEXT,
    RatingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) ON DELETE CASCADE,
    FOREIGN KEY (DriverID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE
);

-- Drivers Table
-- Stores information about drivers
CREATE TABLE Drivers (
    DriverID BIGINT UNSIGNED PRIMARY KEY,
    LicenseNumber VARCHAR(255) NOT NULL,
    VehicleType VARCHAR(255) NOT NULL,
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (DriverID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Tags Table
-- Stores tags that can be associated with restaurants
CREATE TABLE Tags (
    TagID INT AUTO_INCREMENT PRIMARY KEY,
    TagName VARCHAR(50) NOT NULL UNIQUE
);

-- RestaurantTags Table
-- Associates tags with restaurants
CREATE TABLE RestaurantTags (
    RestaurantTagID INT AUTO_INCREMENT PRIMARY KEY,
    RestaurantID INT,
    TagID INT,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) ON DELETE CASCADE,
    FOREIGN KEY (TagID) REFERENCES Tags(TagID) ON DELETE CASCADE,
    UNIQUE (RestaurantID, TagID)
);

-- Index on Orders table
CREATE INDEX idx_order_status ON Orders (OrderStatus);

