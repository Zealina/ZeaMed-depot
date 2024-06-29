-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS zeamed_dev_db;
CREATE USER IF NOT EXISTS 'zeamed_dev'@'localhost' IDENTIFIED BY 'zeamed_dev_pwd';
GRANT ALL PRIVILEGES ON `zeamed_dev_db`.* TO 'zeamed_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'zeamed_dev'@'localhost';
FLUSH PRIVILEGES;
