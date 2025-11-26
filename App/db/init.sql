-- Create and use the database
CREATE DATABASE IF NOT EXISTS recipete_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE recipete_db;

-- USERS
CREATE TABLE users (
  user_id       INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name     VARCHAR(255),
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- INGREDIENTS
CREATE TABLE ingredients (
  ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL,
  default_unit  VARCHAR(50),
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_ingredient_name (name)
) ENGINE=InnoDB;

-- RECIPES
CREATE TABLE recipes (
  recipe_id        INT AUTO_INCREMENT PRIMARY KEY,
  user_id          INT,
  title            VARCHAR(255) NOT NULL,
  description      TEXT,
  total_time_min   INT,
  servings         INT,
  source_type      ENUM('USER','THEMEALDB','OTHER') NOT NULL DEFAULT 'USER',
  source_external_id VARCHAR(100),
  created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  INDEX idx_source (source_type, source_external_id)
) ENGINE=InnoDB;

-- RECIPE_INGREDIENTS
CREATE TABLE recipe_ingredients (
  recipe_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id            INT NOT NULL,
  ingredient_id        INT NOT NULL,
  quantity             DECIMAL(10,2) NOT NULL,
  unit                 VARCHAR(50),
  note                 VARCHAR(255),
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;
