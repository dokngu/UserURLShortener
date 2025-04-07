DELIMITER //

-- IMPORTANT: This assumes the password has already been encrypted
--
-- Create a new user (not an admin)
-- This procedure adds a new user to the 'users' table. The user will have non-admin privileges by default (is_admin = 0).
DROP PROCEDURE IF EXISTS createUser//
CREATE PROCEDURE createUser(IN p_username VARCHAR(32), IN p_pw_hash VARCHAR(64), IN p_email VARCHAR(32))
BEGIN
    -- Insert the new user with username, hashed password, and email
    INSERT INTO users (username, pw_hash, email, is_admin)
    VALUES (p_username, p_pw_hash, p_email, 0);  -- Default 'is_admin' is 0 (non-admin user).
    SELECT LAST_INSERT_ID();
END//

-- Get the stored hash pw of a user for comparison
DROP PROCEDURE IF EXISTS verifyCreds//
CREATE PROCEDURE verifyCreds(IN u_username VARCHAR(32))
BEGIN
  SELECT pw_hash FROM users 
  WHERE username = u_username
  LIMIT 1;
END//

-- Get the user_id of the current user
DROP PROCEDURE IF EXISTS getUserID//
CREATE PROCEDURE getUserID(IN u_username VARCHAR(32))
BEGIN
  SELECT user_id FROM users 
  WHERE username = u_username
  LIMIT 1;
END//

-- add short url to DB
DROP PROCEDURE IF EXISTS createShort//
CREATE PROCEDURE createShort(
    IN p_url_id VARCHAR(8),
    IN p_original_url VARCHAR(256),
    IN p_user_id INT
)
BEGIN
    INSERT INTO urls (url_id, original_url, user_id)
    VALUES (p_url_id, p_original_url, p_user_id);
    SELECT LAST_INSERT_ID();
END //

-- gets long url from short url
DROP PROCEDURE IF EXISTS getLink//
CREATE PROCEDURE getLink(
    IN p_url_id VARCHAR(8)
)
BEGIN
    SELECT original_url FROM urls 
    WHERE url_id = p_url_id
    LIMIT 1;
END //


DELIMITER ;
