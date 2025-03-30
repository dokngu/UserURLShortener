DELIMITER //
-- IMPORTANT: This assumes the password has already been encrypted
-- as there is no way to do encryption at this point.
--
-- Create a new user (not an admin)
-- This procedure adds a new user to the 'users' table. The user will have non-admin privileges by default (is_admin = 0).
CREATE PROCEDURE createUser(IN p_username VARCHAR(32), IN p_pw_hash VARCHAR(64), IN p_email VARCHAR(32))
BEGIN
    -- Insert the new user with username, hashed password, and email
    INSERT INTO users (username, pw_hash, email, is_admin)
    VALUES (p_username, p_pw_hash, p_email, 0);  -- Default 'is_admin' is 0 (non-admin user).
END//
DELIMITER ;
