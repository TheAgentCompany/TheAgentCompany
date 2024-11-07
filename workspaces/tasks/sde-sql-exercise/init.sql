DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY, 
    product_name TEXT,               
    unit_price REAL,                 
    category TEXT,
    sub_category TEXT,
    stock_quantity INTEGER,
    manufacturer TEXT
);


INSERT INTO products VALUES 
(1, 'Professional Laptop T1', 1299.99, 'Electronics', 'Laptops', 100, 'Dell'),
(2, 'Business Monitor M1', 499.99, 'Electronics', 'Monitors', 150, 'LG'),
(3, 'Wireless Mouse G1', 29.99, 'Electronics', 'Accessories', 200, 'Logitech'),
(4, 'Ergonomic Chair C1', 299.99, 'Furniture', 'Chairs', 50, 'Herman Miller'),
(5, 'Standing Desk D1', 699.99, 'Furniture', 'Desks', 30, 'Steelcase'),
(6, 'Filing Cabinet F1', 199.99, 'Furniture', 'Storage', 40, 'IKEA'),
(7, 'Color Printer P1', 399.99, 'Office Equipment', 'Printers', 80, 'HP'),
(8, 'HD Projector PJ1', 899.99, 'Office Equipment', 'Projectors', 25, 'Epson'),
(9, 'Document Scanner S1', 249.99, 'Office Equipment', 'Scanners', 60, 'Canon'),
(10, 'Gaming Laptop G1', 1799.99, 'Electronics', 'Laptops', 75, 'Dell'),
(11, 'Ultra Monitor M2', 599.99, 'Electronics', 'Monitors', 100, 'LG'),
(12, 'Mechanical Keyboard K1', 129.99, 'Electronics', 'Accessories', 150, 'Logitech'),
(13, 'Executive Chair C2', 499.99, 'Furniture', 'Chairs', 40, 'Herman Miller'),
(14, 'Conference Table T1', 999.99, 'Furniture', 'Desks', 20, 'Steelcase'),
(15, 'Storage Cabinet S1', 299.99, 'Furniture', 'Storage', 35, 'IKEA'),
(16, 'Laser Printer P2', 599.99, 'Office Equipment', 'Printers', 45, 'HP'),
(17, 'Mini Projector PJ2', 499.99, 'Office Equipment', 'Projectors', 30, 'Epson'),
(18, 'Portable Scanner S2', 179.99, 'Office Equipment', 'Scanners', 70, 'Canon'),
(19, 'Tablet Pro T1', 899.99, 'Electronics', 'Accessories', 90, 'Dell'),
(20, 'LED Monitor M3', 399.99, 'Electronics', 'Monitors', 120, 'LG');

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,      
    product_id INTEGER,
    sale_date DATE,                   
    quantity INTEGER,
    actual_price REAL,                
    region TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO sales (sale_id, product_id, sale_date, quantity, actual_price, region) VALUES 
(1, 10, '2024-01-15', 3, 1699.99, 'North'),
(2, 10, '2024-01-16', 2, 1699.99, 'South'),
(3, 1, '2024-01-15', 2, 1199.99, 'East'),
(4, 1, '2024-01-17', 1, 1199.99, 'West'),
(5, 19, '2024-01-18', 3, 849.99, 'North'),
(6, 2, '2024-01-19', 2, 479.99, 'South'),
(7, 11, '2024-01-20', 4, 549.99, 'East'),
(8, 3, '2024-01-21', 5, 27.99, 'West'),
(9, 12, '2024-01-22', 3, 119.99, 'North'),
(10, 20, '2024-01-23', 2, 379.99, 'South'),
(11, 4, '2024-01-24', 2, 289.99, 'North'),
(12, 5, '2024-01-25', 1, 679.99, 'South'),
(13, 6, '2024-01-26', 3, 189.99, 'East'),
(14, 7, '2024-01-27', 2, 389.99, 'West'),
(15, 8, '2024-01-28', 1, 879.99, 'North'),
(16, 9, '2024-01-29', 4, 239.99, 'South'),
(17, 13, '2024-01-30', 1, 479.99, 'East'),
(18, 14, '2024-01-31', 2, 959.99, 'West'),
(19, 15, '2024-02-01', 3, 289.99, 'North'),
(20, 16, '2024-02-02', 2, 579.99, 'South');