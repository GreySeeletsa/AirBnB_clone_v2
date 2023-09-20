-- the script prepare the MySQL server for a project
-- creates the project testing database with a name : hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- creats the new user named : hbnb_test with all the privileges on a db hbnb_test_db
-- with a password : hbnb_test_pwd if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- grants the SELECT privilege for user hbnb_test on a db performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
-- grants all the privileges to a new user on the hbnb_test_db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
