-- It creates the MySQL server with:
--   The database hbnb_dev_db.
--   The user hbnb_dev with the password hbnb_dev_pwd in a localhost.
--   It grants all the privileges for hbnb_dev on hbnb_dev_db.
--   It grants SELECT privilege for hbnb_dev on performance_schema.

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER
    IF NOT EXISTS 'hbnb_dev'@'localhost'
    IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES
   ON `hbnb_dev_db`.*
   TO 'hbnb_dev'@'localhost'
   IDENTIFIED BY 'hbnb_dev_pwd';
GRANT SELECT
   ON `performance_schema`.*
   TO 'hbnb_dev'@'localhost'
   IDENTIFIED BY 'hbnb_dev_pwd';
FLUSH PRIVILEGES;
