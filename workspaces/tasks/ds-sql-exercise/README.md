SQL reference and expected result:


Task 1:

SQL:
SELECT COUNT(*) FROM products;

Expected result:
20

Task 2:

SQL:
SELECT COUNT(DISTINCT category) FROM products;

Expected result:
3

Task 3:

SQL:
SELECT product_name, unit_price 
FROM products 
WHERE category = 'Electronics' 
ORDER BY unit_price DESC 
LIMIT 3;

Expected result:
("Gaming Laptop G1", 1799.99),
("Professional Laptop T1", 1299.99),
("Tablet Pro T1", 899.99)