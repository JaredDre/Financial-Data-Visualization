-- Description: This SQL script sets up the database and tables for our finance app

-- Create the main database if it doesn't exist
CREATE DATABASE IF NOT EXISTS finance_db;
USE finance_db;

-- Create a table to store users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY, -- unique ID for each user
    name VARCHAR(100) NOT NULL              -- user's full name
);

-- Create a table for storing each user's monthly financial data
CREATE TABLE IF NOT EXISTS financial_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY, -- unique ID for each record
    user_id INT NOT NULL,                     -- links to users table
    year INT,                                 -- year of the record
    month VARCHAR(20),                        -- month of the record
    amount DECIMAL(10,2),                     -- money amount
    FOREIGN KEY (user_id) REFERENCES users(user_id) -- relationship
);

-- Insert sample users only if they don't already exist
INSERT IGNORE INTO users (name)
VALUES ('Jane Doe'),
       ('Chloe Farrel');

-- Insert some sample financial records (basic examples)
INSERT IGNORE INTO financial_records (user_id, year, month, amount)
VALUES 
(1, 2025, 'January', 1200.50),
(1, 2025, 'February', 1300.75),
(1, 2025, 'March', 1250.00),
(2, 2025, 'January', 980.25),
(2, 2025, 'February', 1025.50);

-- Quick check: show all tables in the database
SHOW TABLES;

-- Quick check: see all users
SELECT * FROM users;

-- Quick check: see all financial records
SELECT * FROM financial_records;

-- Combined view: see which user each record belongs to
SELECT u.user_id, u.name, f.year, f.month, f.amount
FROM financial_records f
JOIN users u ON f.user_id = u.user_id
ORDER BY u.user_id, f.year, f.month;










