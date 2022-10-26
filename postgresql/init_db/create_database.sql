CREATE TABLE product (
  product_id smallint NOT NULL GENERATED ALWAYS AS IDENTITY (start 1 increment 1 minvalue 1),
  dev_date date NOT NULL,
  nicotine smallint NOT NULL,
  vg_pg varchar(8) NOT NULL,
  amount_items smallint NOT NULL,
  is_demo boolean NOT NULL,
  is_active boolean NOT NULL,
  product_name varchar(32) NOT NULL,
  description varchar(3072) NOT NULL,
  logo_file varchar(32) NOT NULL,
  price smallint NOT NULL,
  volume smallint NOT NULL,
  rating smallint NOT NULL,
  PRIMARY KEY (product_id)
);

CREATE TABLE "user" (
  user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (start 1 increment 1 minvalue 1),
  name varchar(32) NOT NULL,
  total_purchased integer NOT NULL,
  is_active bool NOT NULL,
  hashed_password varchar(64) NOT NULL,
  is_banned bool NOT NULL,
  ban_description varchar(64) DEFAULT NULL,
  reg_date date NOT NULL,
  last_reservation_date date DEFAULT NULL,
  promo_codes json NOT NULL,
  reservations json NOT NULL,
  email varchar(64) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE item (
  item_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (start 1 increment 1 minvalue 1),
  product_id smallint NOT NULL,
  manufacture_date date NOT NULL,
  is_reserved bool NOT NULL,
  is_sales bool NOT NULL,
  PRIMARY KEY (item_id),
  CONSTRAINT item_product_id_product_logo_file_foreign FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE reservation (
  reservation_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (start 1 increment 1 minvalue 1),
  reservation_date date NOT NULL,
  user_id integer NOT NULL,
  reservation_name varchar(32) NOT NULL,
  product_id smallint NOT NULL,
  amount smallint NOT NULL,
  is_completed bool NOT NULL,
  total smallint NOT NULL,
  sale smallint NOT NULL,
  items_reserved json NOT NULL,
  PRIMARY KEY (reservation_id),
  CONSTRAINT reservation_product_id_product_product_id_foreign FOREIGN KEY (product_id) REFERENCES product (product_id),
  CONSTRAINT reservation_user_id_user_user_id_foreign FOREIGN KEY (user_id) REFERENCES "user" (user_id)
);