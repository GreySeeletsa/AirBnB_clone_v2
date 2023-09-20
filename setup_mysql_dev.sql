-- the script prepare  MySQL server for the project
-- creates the project developement database with a name : hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- creats a new user named : hbnb_dev with all the privileges on a db hbnb_dev_db
-- with password : hbnb_dev_pwd if it does not exist 
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- grants all the privileges to a new user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
-- grants SELECT privilege for a user hbnb_dev in the db performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
