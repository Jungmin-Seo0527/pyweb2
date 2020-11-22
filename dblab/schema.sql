DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS restaurant;

CREATE TABLE restaurant (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(250) NOT NULL
);

CREATE TABLE menu_item (
  name VARCHAR(80) NOT NULL,
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description VARCHAR(250), 
  price VARCHAR(8), 
  course VARCHAR(80),
  restaurant_id INTEGER,
  FOREIGN KEY(restaurant_id) REFERENCES restaurant(id)
);
