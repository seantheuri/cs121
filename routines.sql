
-- Function: CalculateTotalOrderPrice
DELIMITER !
CREATE FUNCTION CalculateTotalOrderPrice(order_id INT) RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total_price DECIMAL(10, 2);

    SELECT SUM(od.Quantity * mi.Price) INTO total_price
    FROM OrderDetails od
    JOIN MenuItems mi ON od.MenuItemID = mi.MenuItemID
    WHERE od.OrderID = order_id;

    RETURN IFNULL(total_price, 0);
END!
DELIMITER ;



-- PROCEDURE
  DELIMITER !
 
  CREATE PROCEDURE AddItemToOrder(IN order_id INT, IN menu_item_id INT, IN quantity INT)
  BEGIN
 
      START TRANSACTION;
      
      INSERT INTO OrderDetails (OrderID, MenuItemID, Quantity)
      VALUES (order_id, menu_item_id, quantity);
      
      UPDATE Orders
      SET TotalPrice = CalculateTotalOrderPrice(order_id)
      WHERE OrderID = order_id;
      
      COMMIT; 
  END!
 
  DELIMITER ;


-- FUNCTION
DELIMITER !

CREATE FUNCTION GetRestaurantTagNames(restaurant_id INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE tag_name VARCHAR(50);
    DECLARE tag_names VARCHAR(255) DEFAULT '';
    
    DECLARE cur CURSOR FOR
        SELECT t.TagName
        FROM Tags t
        JOIN RestaurantTags rt ON t.TagID = rt.TagID
        WHERE rt.RestaurantID = restaurant_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN cur;
    
    WHILE done = 0 DO
        FETCH cur INTO tag_name;
        
        IF done = 0 THEN
            SET tag_names = CONCAT(tag_names, IF(LENGTH(tag_names) = 0, '', ', '), tag_name);
        END IF;
    END WHILE;
    
    CLOSE cur;
    
    RETURN tag_names;
END!

DELIMITER ;


DELIMITER !
CREATE PROCEDURE GetBestSellingItems(IN rest_id INT)
BEGIN
    SELECT mi.Name, SUM(od.Quantity) AS TotalQuantity
    FROM OrderDetails od
    JOIN MenuItems mi ON od.MenuItemID = mi.MenuItemID
    JOIN Orders o ON od.OrderID = o.OrderID
    WHERE o.RestaurantID = rest_id AND o.OrderStatus = 'Delivered'
    GROUP BY mi.Name
    ORDER BY TotalQuantity DESC
    LIMIT 5;
END !
DELIMITER ;


DELIMITER !
CREATE PROCEDURE GetPoorestSellingItems(IN rest_id INT)
BEGIN
    SELECT mi.Name, IFNULL(SUM(od.Quantity), 0) AS TotalQuantity
    FROM MenuItems mi
    LEFT JOIN OrderDetails od ON mi.MenuItemID = od.MenuItemID AND od.OrderID IN (
        SELECT OrderID FROM Orders WHERE RestaurantID = rest_id AND OrderStatus = 'Delivered'
    )
    WHERE mi.RestaurantID = rest_id
    GROUP BY mi.Name
    ORDER BY TotalQuantity ASC
    LIMIT 5;
END !
DELIMITER ;


DELIMITER !

CREATE TRIGGER OrderDetailInsert AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET TotalPrice = CalculateTotalOrderPrice(NEW.OrderID)
    WHERE OrderID = NEW.OrderID;
END!

DELIMITER ;



DELIMITER !

CREATE TRIGGER OrderDetailDelete AFTER DELETE ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET TotalPrice = CalculateTotalOrderPrice(OLD.OrderID)
    WHERE OrderID = OLD.OrderID;
END!

DELIMITER ;


DELIMITER !

CREATE TRIGGER AfterRatingInsert
AFTER INSERT ON Ratings
FOR EACH ROW
BEGIN
    UPDATE Restaurants
    SET Rating = (
        SELECT AVG(Score)
        FROM Ratings
        WHERE RestaurantID = NEW.RestaurantID
    )
    WHERE RestaurantID = NEW.RestaurantID;
END!
DELIMITER ;
