DROP DATABASE IF EXISTS GymDB;
CREATE database GymDB;
GRANT ALL PRIVILEGES ON GymDB.* TO 'david'@'localhost';
FLUSH PRIVILEGES;
use GymDB;

DROP TABLE IF EXISTS product;
CREATE TABLE product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pname VARCHAR(255) UNIQUE NOT NULL,
    pbrand VARCHAR(255),
    pdescription TEXT,
    pstatus ENUM("DISPONIBLE", "AGOTADO", "PROXIMAMENTE", "INACTIVO") NOT NULL,
    pcategory ENUM("MAQUINAS", "PESAS LIBRES", "EQUIPOS CARDIOVASCULARES") NOT NULL,
    pprice DECIMAL(10, 2) NOT NULL,
    pstock INT NOT NULL,
    pimgspath  VARCHAR(100) UNIQUE
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
    cid INT PRIMARY KEY AUTO_INCREMENT,
    cname VARCHAR(255) NOT NULL,
    cphone VARCHAR(20) NOT NULL,
    cemail VARCHAR(255) UNIQUE NOT NULL,
    cdate DATE NOT NULL
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    saleid INT PRIMARY KEY AUTO_INCREMENT, 
    productid INT NOT NULL, 
    quantity INT NOT NULL, 
    date DATE NOT NULL, 
    FOREIGN KEY (productid) REFERENCES product(id)
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS shoppingcart;
CREATE TABLE shoppingcart(
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer(cid),
    FOREIGN KEY (product_id) REFERENCES product(id)
)ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

INSERT INTO product (pname, pbrand, pdescription, pstatus, pcategory, pprice, pstock) VALUES
    ('Treadmill', 'Nike', 'Powerful motorized treadmill for home use', 'DISPONIBLE', 'MAQUINAS', 999.99, 20),
    ('Dumbells', 'Adidas', 'Powerful Dumbells', 'DISPONIBLE', 'MAQUINAS', 999.99, 20);
INSERT INTO sales (productid, quantity, date) VALUES
    (1, 5, '2024-05-07');
INSERT INTO customer(cname, cphone, cemail, cdate) VALUES
    ('Customer1', '8888-8888', 'customer1@gmail.com', '2022-03-21');

INSERT INTO shoppingcart(customer_id, product_id) VALUES
    (1, 1),
    (1, 2);
-- INSERT INTO user (uname, uphone, uemail, udate) VALUES 
--     ('John Doe', '123-456-7890', 'john@example.com', '2022-03-21'),
--     ('Alice Smith', '987-654-3210', 'alice@example.com', '2022-03-21'),
--     ('Bob Johnson', '555-123-4567', 'bob@example.com', '2022-03-21'),
--     ('Emily Davis', '444-555-6666', 'emily@example.com', '2022-03-21'),
--     ('Michael Brown', '999-888-7777', 'michael@example.com', '2022-03-21');
 