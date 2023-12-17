CREATE DATABASE grocerystore;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE category(
    category_id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL
);

CREATE TABLE brand(
    brand_id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL
);

CREATE TABLE product(
    product_id SERIAL PRIMARY KEY,
    product_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    title VARCHAR(250) NOT NULL,
    category_id INT REFERENCES category(category_id) ON DELETE CASCADE ON UPDATE CASCADE,
    brand_id INT REFERENCES brand(brand_id) ON DELETE CASCADE ON UPDATE CASCADE,
    price INT NOT NULL,
    product_description TEXT
);

CREATE TABLE client(
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(250) NOT NULL,
    phone VARCHAR(70) NOT NULL,
    email VARCHAR(250) NOT NULL,
    client_address VARCHAR(500) NOT NULL,
    username VARCHAR(250) NULL
);













