-- It creates a MySQL server with:
--   The database hbnb_test_db.
--   The user hbnb_test with the password hbnb_test_pwd in a localhost.
--   It grants all the privileges for the hbnb_test on hbnb_test_db.
--   It grants SELECT privilege for hbnb_test on performance_schema.

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER
    IF NOT EXISTS 'hbnb_test'@'localhost'
    IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES
   ON `hbnb_test_db`.*
   TO 'hbnb_test'@'localhost'
   IDENTIFIED BY 'hbnb_test_pwd';
GRANT SELECT
   ON `performance_schema`.*
   TO 'hbnb_test'@'localhost'
   IDENTIFIED BY 'hbnb_test_pwd';
FLUSH PRIVILEGES;
