-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS zeamed_test_db;
CREATE USER IF NOT EXISTS 'zeamed_test'@'localhost' IDENTIFIED BY 'zeamed_test_pwd';
GRANT ALL PRIVILEGES ON `zeamed_test_db`.* TO 'zeamed_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'zeamed_test'@'localhost';
FLUSH PRIVILEGES;
