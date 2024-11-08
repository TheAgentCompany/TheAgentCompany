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