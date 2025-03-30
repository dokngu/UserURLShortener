DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id 	int NOT NULL AUTO_INCREMENT,
  username 	varchar(32),
  pw_hash 	varchar(64),
  email 	varchar(32),
  is_admin 	bit,
  PRIMARY KEY (user_id)
);

CREATE TABLE urls (
  url_id 	varchar(8) NOT NULL,
  original_url 	varchar(256) NOT NULL,
  user_id 	int,
  PRIMARY KEY (url_id)
);

CREATE TABLE cookies(
  user_id 	int,
  cookie 	varchar(64),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

