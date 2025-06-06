CREATE DATABASE YelpDB;
USE YelpDB;
CREATE TABLE Businesses (
    business_id VARCHAR(255) PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    stars FLOAT CHECK (stars >= 0 AND stars <= 5),
    review_count INT CHECK (review_count >= 0),
    latitude DECIMAL(9,6) CHECK (latitude BETWEEN -90.000000 AND 90.000000),
    longitude DECIMAL(10,6) CHECK (longitude BETWEEN -180.000000 AND 180.000000)
);

DROP TABLE IF EXISTS Categories;

CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL
);








SELECT COUNT(*) FROM Categories;
SELECT COUNT(*) FROM Businesses;
SELECT COUNT(*) FROM BusinessCategory;




CREATE TABLE BusinessCategory (
    business_id VARCHAR(255),
    category_id INT,
    PRIMARY KEY (business_id, category_id),
    FOREIGN KEY (business_id) REFERENCES Businesses(business_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);

SELECT * FROM Categories WHERE category_id = 100;


SELECT c.category_name
FROM BusinessCategory bc
JOIN Categories c ON bc.category_id = c.category_id
WHERE bc.business_id = '3pc7aRkKohVPRPlwDac3tQ';

describe businesses
Select * from BusinessCategory

