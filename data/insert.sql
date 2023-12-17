INSERT INTO category (title) VALUES
    ('Fruits'),
    ('Vegetables'),
    ('Dairy products'),
    ('Bakery'),
    ('Meat and Poultry'),
    ('Beverages'),
    ('Snacks');


INSERT INTO brand (title) VALUES
    ('Apple'),
    ('Banana'),
    ('Carrots Inc.'),
    ('Wonder Bread'),
    ('Tyson Foods'),
    ('Coca-Cola'),
    ('Lays');


INSERT INTO product (title, category_id, brand_id, price, product_description) VALUES
    ('Red Apple', 1, 1, 10000, 'Fresh and delicious'),
    ('Green Apple', 1, 1, 12000, 'Crisp and juicy'),
    ('Banana', 1, 2, 7000, 'Yellow and ripe'),
    ('Carrots', 2, 3, 5000, 'Sweet and crunchy'),
    ('Whole Milk', 3, 3, 8000, 'Rich and creamy'),
    ('White Bread', 4, 4, 3000, 'Soft and fluffy bread'),
    ('Chicken Breast', 5, 5, 15000, 'Boneless and skinless chicken breast'),
    ('Coca-Cola', 6, 6, 9000, 'Sparkling cola beverage'),
    ('Potato Chips', 7, 7, 7000, 'Crunchy and savory potato chips');
