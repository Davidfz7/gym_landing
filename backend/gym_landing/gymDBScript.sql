DROP DATABASE IF EXISTS GymDB;
CREATE database GymDB;
GRANT ALL PRIVILEGES ON GymDB.* TO 'david'@'localhost';
FLUSH PRIVILEGES;
use GymDB;

DROP TABLE IF EXISTS product;
CREATE TABLE product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pname VARCHAR(255) UNIQUE NOT NULL,
    pdescription TEXT,
    pstatus ENUM('available', 'out of stock', 'coming soon') NOT NULL,
    pprice DECIMAL(10, 2) NOT NULL,
    pstock INT NOT NULL,
    pimgspath  VARCHAR(100) UNIQUE
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    uname VARCHAR(255) NOT NULL,
    uphone VARCHAR(20) NOT NULL,
    uemail VARCHAR(255) UNIQUE NOT NULL,
    udate DATE NOT NULL
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


INSERT INTO product (pname, pdescription, pstatus, pprice, pstock) VALUES
    ('Treadmill', 'Powerful motorized treadmill for home use', 'available', 999.99, 20);


-- INSERT INTO user (uname, uphone, uemail, udate) VALUES 
--     ('John Doe', '123-456-7890', 'john@example.com', '2022-03-21'),
--     ('Alice Smith', '987-654-3210', 'alice@example.com', '2022-03-21'),
--     ('Bob Johnson', '555-123-4567', 'bob@example.com', '2022-03-21'),
--     ('Emily Davis', '444-555-6666', 'emily@example.com', '2022-03-21'),
--     ('Michael Brown', '999-888-7777', 'michael@example.com', '2022-03-21');
 