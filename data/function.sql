CREATE OR REPLACE VIEW all_products_view AS
  SELECT * FROM product;




CREATE OR REPLACE VIEW all_category_view AS
  SELECT * FROM category;




CREATE OR REPLACE VIEW all_brand_view AS
  SELECT * FROM brand;




CREATE OR REPLACE FUNCTION insert_product(
    product_title TEXT,
    category_id INTEGER,
    brand_id INTEGER,
    product_price NUMERIC,
    description TEXT
)
RETURNS VOID
AS $$
INSERT INTO product (title, category_id, brand_id, price, product_description)
VALUES (product_title, category_id, brand_id, product_price, description);
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION GetLatestProducts()
RETURNS TABLE (product_id INT, title TEXT, price NUMERIC, product_description TEXT)
AS $$
    SELECT product_id, title, price, product_description
    FROM product
    ORDER BY product_id DESC
    LIMIT 10;
$$ LANGUAGE sql;




CREATE OR REPLACE FUNCTION delete_product_by_uuid(
    product_uuid UUID
)
RETURNS VOID
AS $$
DELETE FROM product WHERE product_uuid = delete_product_by_uuid.product_uuid;
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION select_product_by_uuid(
    product_uuid UUID
)
RETURNS SETOF product
AS $$
SELECT * FROM product WHERE product_uuid = select_product_by_uuid.product_uuid;
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION update_product_by_uuid(
    product_title TEXT,
    category_id INTEGER,
    brand_id INTEGER,
    product_price NUMERIC,
    product_description TEXT,
    product_uuid UUID
)
RETURNS VOID
AS $$
UPDATE product
SET
    title = update_product_by_uuid.product_title,
    category_id = update_product_by_uuid.category_id,
    brand_id = update_product_by_uuid.brand_id,
    price = update_product_by_uuid.product_price,
    product_description = update_product_by_uuid.product_description
WHERE product_uuid = update_product_by_uuid.product_uuid;
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION get_product_info_by_uuid(
    product_uuid UUID
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand_id = brand.brand_id
JOIN category ON product.category_id = category.category_id
WHERE product_uuid = get_product_info_by_uuid.product_uuid;
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION get_products_by_category_id(
    category_id INTEGER
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand_id = brand.brand_id
JOIN category ON product.category_id = category.category_id
WHERE product.category_id = get_products_by_category_id.category_id;
$$ LANGUAGE SQL;




CREATE OR REPLACE FUNCTION get_products_by_brand_id(
    brand_id INTEGER
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand_id = brand.brand_id
JOIN category ON product.category_id = category.category_id
WHERE product.brand_id = get_products_by_brand_id.brand_id;
$$ LANGUAGE SQL;




CREATE OR REPLACE VIEW client_username_view AS
  SELECT username FROM client;


-- index
CREATE INDEX category_title_index
ON category (title);


CREATE INDEX brand_title_index
ON brand (title);


CREATE INDEX idx_product_id
ON product (product_id);


CREATE INDEX idx_category_id
ON product (category_id);


CREATE INDEX idx_brand_id
ON product (brand_id);
