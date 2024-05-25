-- Drop the databse if it already exists
DROP DATABASE IF EXISTS `zeamed-depot`;

-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS `zeamed-depot`;

-- Create the user if it doesn't already exist
CREATE USER IF NOT EXISTS 'zealina'@'localhost' IDENTIFIED BY 'zealina';

-- Grant all privileges on the zeamed-depot database to the zealina user
GRANT ALL PRIVILEGES ON `zeamed-depot`.* TO 'zealina'@'localhost';

-- Flush privileges to ensure that all changes take effect immediately
FLUSH PRIVILEGES;

