CREATE TABLE categories
(
  id          INT AUTO_INCREMENT
    PRIMARY KEY,
  name        VARCHAR(150) NOT NULL,
  link_http   VARCHAR(250) NOT NULL,
  id_category VARCHAR(150) NULL
)
  ENGINE = InnoDB;

CREATE TABLE link_category_product
(
  category_id INT NOT NULL,
  product_id  INT NOT NULL,
  PRIMARY KEY (category_id, product_id),
  CONSTRAINT link_category_product_ibfk_1
  FOREIGN KEY (category_id) REFERENCES categories (id)
)
  ENGINE = InnoDB;

CREATE INDEX product_id
  ON link_category_product (product_id);

CREATE TABLE products
(
  id              INT AUTO_INCREMENT
    PRIMARY KEY,
  name            VARCHAR(150) NOT NULL,
  description     TEXT         NOT NULL,
  nutrition_grade CHAR         NOT NULL,
  shop            VARCHAR(100) NULL,
  link_http       VARCHAR(250) NOT NULL
)
  ENGINE = InnoDB;

ALTER TABLE link_category_product
  ADD CONSTRAINT link_category_product_ibfk_2
FOREIGN KEY (product_id) REFERENCES products (id);

CREATE TABLE save_products
(
  id         INT AUTO_INCREMENT
    PRIMARY KEY,
  id_product INT      NOT NULL,
  date       DATETIME NULL,
  CONSTRAINT save_products_ibfk_1
  FOREIGN KEY (id_product) REFERENCES products (id)
)
  ENGINE = InnoDB;

CREATE INDEX id_product
  ON save_products (id_product);


