DELIMITER !

-- Procedure to add a new user
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20), user_type ENUM('Customer', 'Driver', 'RestaurantAdmin', 'PlatformAdmin'))
BEGIN
    DECLARE new_salt CHAR(8);
    DECLARE hashed_password BINARY(64);
    SET new_salt = make_salt(8);
    SET hashed_password = SHA2(CONCAT(new_salt, password), 256);
    INSERT INTO user_info (username, salt, password_hash, UserType) VALUES (new_username, new_salt, hashed_password, user_type);
END !
DELIMITER ;

DELIMITER !

CREATE PROCEDURE sp_authenticate(username_a VARCHAR(20), password VARCHAR(20))
BEGIN
    DECLARE user_salt CHAR(8);
    DECLARE user_password_hash BINARY(64);
    

    SELECT salt, password_hash INTO user_salt, user_password_hash 
    FROM user_info 
    WHERE username = username_a;
    
    SELECT username, UserType
    FROM user_info
    WHERE username = username_a
    AND password_hash = SHA2(CONCAT(user_salt, password), 256);
END !
DELIMITER ;

DELIMITER !

-- Procedure to change a user's password
CREATE PROCEDURE sp_change_password(username_a VARCHAR(20), new_password VARCHAR(20))
BEGIN
    DECLARE new_salt CHAR(8);
    DECLARE new_hashed_password BINARY(64);
    SET new_salt = make_salt(8);
    SET new_hashed_password = SHA2(CONCAT(new_salt, new_password), 256);
    UPDATE user_info SET salt = new_salt, password_hash = new_hashed_password WHERE username = username_a;
END !
DELIMITER ;
