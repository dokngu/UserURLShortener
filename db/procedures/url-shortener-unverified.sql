DELIMITER $$

-- Store a new user session (cookie)
-- This procedure inserts a new session cookie for a user or updates the cookie if it already exists for that user.
CREATE PROCEDURE createCookie(IN p_user_id INT, IN p_cookie VARCHAR(64))
BEGIN
    -- Insert or update the cookie for the user identified by p_user_id
    INSERT INTO cookies (user_id, cookie)
    VALUES (p_user_id, p_cookie)
    ON DUPLICATE KEY UPDATE cookie = p_cookie;  -- If the user already has a cookie, it is updated.
END$$

-- Delete a user session (cookie)
-- This procedure deletes the session cookie for a specific user by their user_id.
CREATE PROCEDURE deleteCookie(IN p_user_id INT)
BEGIN
    -- Delete the cookie associated with the user
    DELETE FROM cookies WHERE user_id = p_user_id;
END$$

-- Create a new user (not an admin)
-- This procedure adds a new user to the 'users' table. The user will have non-admin privileges by default (is_admin = 0).
CREATE PROCEDURE createUser(IN p_username VARCHAR(32), IN p_pw_hash VARCHAR(64), IN p_email VARCHAR(32))
BEGIN
    -- Insert the new user with username, hashed password, and email
    INSERT INTO users (username, pw_hash, email, is_admin)
    VALUES (p_username, p_pw_hash, p_email, 0);  -- Default 'is_admin' is 0 (non-admin user).
END$$

-- Admin-only: Update user information
-- This procedure allows an admin to update the details (username, password hash, email) of an existing user.
CREATE PROCEDURE updateUser(IN p_user_id INT, IN p_username VARCHAR(32), IN p_pw_hash VARCHAR(64), IN p_email VARCHAR(32))
BEGIN
    -- Only update user information if the user is non-admin (is_admin = 0) and the user_id matches.
    UPDATE users
    SET username = p_username, pw_hash = p_pw_hash, email = p_email
    WHERE user_id = p_user_id AND is_admin = 0;  -- Ensures only non-admin users can be updated.
END$$

-- Admin-only: Delete a user
-- This procedure allows an admin to delete a non-admin user by their user_id.
CREATE PROCEDURE deleteUser(IN p_user_id INT)
BEGIN
    -- Delete the user with the provided user_id, ensuring the user is non-admin.
    DELETE FROM users WHERE user_id = p_user_id AND is_admin = 0;  -- Prevents admins from being deleted.
END$$

-- Create a new shortened URL
-- This procedure generates a random 8-character ID for a new shortened URL and stores it with the original URL and user_id.
CREATE PROCEDURE createURL(IN p_original_url VARCHAR(256), IN p_user_id INT)
BEGIN
    DECLARE new_url_id VARCHAR(8);
    
    -- Generate a random 8-character ID using a UUID, removing the hyphens and taking the first 8 characters
    SET new_url_id = SUBSTRING(REPLACE(UUID(), '-', ''), 1, 8);

    -- Insert the new shortened URL along with the user_id
    INSERT INTO urls (url_id, original_url, user_id)
    VALUES (new_url_id, p_original_url, p_user_id);
    
    -- Return the generated URL ID to the caller
    SELECT new_url_id AS url_id;
END$$

-- Admin-only: Update an existing shortened URL
-- This procedure allows an admin to update the original URL of an existing shortened URL identified by its URL ID.
CREATE PROCEDURE updateURL(IN p_url_id VARCHAR(8), IN p_new_original_url VARCHAR(256))
BEGIN
    -- Update the original URL for the provided shortened URL ID
    UPDATE urls
    SET original_url = p_new_original_url
    WHERE url_id = p_url_id;
END$$

-- Admin-only: Delete a shortened URL
-- This procedure allows an admin to delete a shortened URL from the system by its URL ID.
CREATE PROCEDURE deleteURL(IN p_url_id VARCHAR(8))
BEGIN
    -- Delete the shortened URL corresponding to the given URL ID
    DELETE FROM urls WHERE url_id = p_url_id;
END$$

DELIMITER ;
