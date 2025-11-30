-- ============================================================
-- Recipeté Database Schema
-- ============================================================

-- 1. Create & select database
CREATE DATABASE IF NOT EXISTS recipete_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE recipete_db;

-- =========================================================
-- USERS
-- ============================================================
CREATE TABLE users (
  user_id       INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name     VARCHAR(255),
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- USER PREFERENCES  (1:1 with users)
-- ============================================================
CREATE TABLE user_preferences (
  user_id              INT PRIMARY KEY,
  dietary_preference   ENUM('NONE','VEGETARIAN','VEGAN','PESCETARIAN','GLUTEN_FREE','DAIRY_FREE')
                          NOT NULL DEFAULT 'NONE',
  max_prep_time_min    INT,
  weekly_budget_cents  INT,
  default_days_in_plan INT DEFAULT 3,
  defaults_executive_mode ENUM('NORMAL','LOW_SPOONS','LEFTOVERS_FOCUSED')
                          NOT NULL DEFAULT 'NORMAL',
  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- INGREDIENTS CATALOG
-- ============================================================
CREATE TABLE ingredients (
  ingredient_id     INT AUTO_INCREMENT PRIMARY KEY,
  name              VARCHAR(255) NOT NULL,
  default_unit      VARCHAR(50),
  kroger_product_id VARCHAR(100),
  kroger_location_id VARCHAR(50),
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_ingredient_name (name)
) ENGINE=InnoDB;

-- ============================================================
-- RECIPES (local OR imported from TheMealDB)
-- ============================================================
CREATE TABLE recipes (
  recipe_id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id            INT,
  title              VARCHAR(255) NOT NULL,
  description        TEXT,
  total_time_min     INT,
  servings           INT,
  difficulty         ENUM('EASY','MEDIUM','HARD') DEFAULT 'EASY',
  is_public          TINYINT(1) NOT NULL DEFAULT 1,

  -- external source info (TheMealDB)
  source_type        ENUM('USER','THEMEALDB','OTHER') NOT NULL DEFAULT 'USER',
  source_external_id VARCHAR(100),
  source_url         VARCHAR(500),
  thumbnail_url      VARCHAR(500),
  youtube_url        VARCHAR(500),

  created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  INDEX idx_source (source_type, source_external_id)
) ENGINE=InnoDB;

-- ============================================================
-- RECIPE STEPS
-- ============================================================
CREATE TABLE recipe_steps (
  step_id    INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id  INT NOT NULL,
  step_order INT NOT NULL,
  instruction TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  UNIQUE KEY uq_recipe_step (recipe_id, step_order)
) ENGINE=InnoDB;

-- ============================================================
-- RECIPE INGREDIENTS (junction table)
-- ============================================================
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
    ON UPDATE CASCADE,

  UNIQUE KEY uq_recipe_ingredient (recipe_id, ingredient_id, note)
) ENGINE=InnoDB;

-- ============================================================
-- TAGS
-- ============================================================
CREATE TABLE tags (
  tag_id    INT AUTO_INCREMENT PRIMARY KEY,
  name      VARCHAR(100) NOT NULL,
  category  ENUM('DIET','TIME','COST','OCCASION','OTHER') DEFAULT 'OTHER',
  UNIQUE KEY uq_tag_name (name)
) ENGINE=InnoDB;

-- LINK: recipes ↔ tags
CREATE TABLE recipe_tags (
  recipe_id INT NOT NULL,
  tag_id    INT NOT NULL,
  PRIMARY KEY (recipe_id, tag_id),
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- MEAL PLANS
-- ============================================================
CREATE TABLE meal_plans (
  meal_plan_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  name         VARCHAR(255) NOT NULL,
  start_date   DATE NOT NULL,
  end_date     DATE NOT NULL,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- MEAL PLAN ITEMS
-- ============================================================
CREATE TABLE meal_plan_items (
  meal_plan_item_id INT AUTO_INCREMENT PRIMARY KEY,
  meal_plan_id      INT NOT NULL,
  plan_date         DATE NOT NULL,
  meal_type         ENUM('BREAKFAST','LUNCH','DINNER','SNACK') NOT NULL DEFAULT 'DINNER',
  recipe_id         INT NOT NULL,
  notes             VARCHAR(255),

  FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(meal_plan_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

  INDEX idx_meal_plan_date (meal_plan_id, plan_date)
) ENGINE=InnoDB;

-- ============================================================
-- GROCERY LISTS
-- ============================================================
CREATE TABLE grocery_lists (
  grocery_list_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id         INT NOT NULL,
  meal_plan_id    INT,
  name            VARCHAR(255) NOT NULL,
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(meal_plan_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- GROCERY LIST ITEMS
-- ============================================================
CREATE TABLE grocery_list_items (
  grocery_list_item_id INT AUTO_INCREMENT PRIMARY KEY,
  grocery_list_id      INT NOT NULL,
  ingredient_id        INT NOT NULL,
  quantity             DECIMAL(10,2) NOT NULL,
  unit                 VARCHAR(50),
  is_purchased         TINYINT(1) NOT NULL DEFAULT 0,
  kroger_product_id    VARCHAR(100),

  FOREIGN KEY (grocery_list_id) REFERENCES grocery_lists(grocery_list_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

  INDEX idx_grocery_list (grocery_list_id)
) ENGINE=InnoDB;

-- ============================================================
-- EXTERNAL RECIPE CACHE (raw TheMealDB JSON, optional)
-- ============================================================
CREATE TABLE external_recipe_cache (
  cache_id          INT AUTO_INCREMENT PRIMARY KEY,
  source_type       ENUM('THEMEALDB') NOT NULL,
  source_external_id VARCHAR(100) NOT NULL,
  raw_json          JSON NOT NULL,
  fetched_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_source_recipe (source_type, source_external_id)
) ENGINE=InnoDB;

-- ============================================================
-- END OF SCHEMA
-- ============================================================
