0. Assumptions
You have a folder with:
docker-compose.yml
db/init.sql

Docker Desktop is running, and MySQL is started with:
docker compose up -d

MySQL credentials (from the compose file):
Host:     localhost
Port:     3306
User:     recipete
Password: recipete_pw
Database: recipete_db


1. VS Code: how to connect to MySQL
Install an extension:
MySQL: Database Management for MySQL/MariaDB, PostgreSQL, Redis and ElasticSearch. By Database Client

In VS Code:
Left sidebar → Extensions (square icon)
Search "MySQL" → Install

Create a connection:
You’ll see a new Database icon / panel on the left.
Click + or New Connection.
Use:
Type: MySQL
Host: localhost
Port: 3306
User: recipete
Password: recipete_pw
Database: recipete_db (optional – you can also pick after connecting)
Save / Connect.
You should now see recipete_db with tables under it.

2. Basic navigation queries
Open a New Query window from the DB panel.

--- Show all databases: ---
SHOW DATABASES;

--- Use the Recipeté DB ---
USE recipete_db;

--- List all tables ---
SHOW TABLES;

--- Describe a table ---
DESCRIBE recipes;
-- or
SHOW COLUMNS FROM recipes;

3. Inserts for quick test data
You can paste this directly and run it to get something to play with.

--- Insert a test user ---
INSERT INTO users (email, password_hash, full_name)
VALUES ('test@example.com', 'fakehash', 'Test User');

--- Insert a couple of ingredients ---
INSERT INTO ingredients (name, default_unit)
VALUES
  ('Chicken Breast', 'g'),
  ('Olive Oil', 'tbsp'),
  ('Garlic', 'clove');

--- Insert a simple recipe (USER source) ---
INSERT INTO recipes (user_id, title, description, total_time_min, servings, source_type)
VALUES
  (1, 'Garlic Chicken', 'Simple garlic chicken.', 30, 4, 'USER');

--- Link ingredients to that recipe ---
-- assume recipe_id = 1 from above
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, note)
VALUES
  (1, 1, 500, 'g', 'sliced'),         -- Chicken Breast
  (1, 2, 2,   'tbsp', 'for cooking'), -- Olive Oil
  (1, 3, 3,   'clove', 'minced');     -- Garlic

4. Common SELECT queries for your schema
--- Get all recipes ---
SELECT recipe_id, title, total_time_min, servings
FROM recipes
ORDER BY created_at DESC;

--- Get one recipe by ID ---
SELECT *
FROM recipes
WHERE recipe_id = 1;

--- Get recipe + ingredients (joined) ---
SELECT
  r.recipe_id,
  r.title,
  i.name AS ingredient,
  ri.quantity,
  COALESCE(ri.unit, i.default_unit) AS unit,
  ri.note
FROM recipes r
JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
WHERE r.recipe_id = 1;

--- All recipes imported from TheMealDB ---
SELECT recipe_id, title, source_external_id
FROM recipes
WHERE source_type = 'THEMEALDB';

5. Meal plans & grocery lists (starter queries)
--- Create a simple meal plan ---
INSERT INTO meal_plans (user_id, name, start_date, end_date)
VALUES (1, 'Weeknight Dinners', '2025-11-24', '2025-11-26');

--- Check its ID: ---
SELECT * FROM meal_plans;
Assume meal_plan_id = 1.

--- Add items (meals) to the plan ---
INSERT INTO meal_plan_items (meal_plan_id, plan_date, meal_type, recipe_id)
VALUES
  (1, '2025-11-24', 'DINNER', 1),
  (1, '2025-11-25', 'DINNER', 1);

--- Create a grocery list for that plan ---
INSERT INTO grocery_lists (user_id, meal_plan_id, name)
VALUES (1, 1, 'Groceries for Weeknight Dinners');

--- Check id: ---
SELECT * FROM grocery_lists;

Assume grocery_list_id = 1.
Example: aggregated grocery list query (no insert yet)

--- To see what you’d need to buy for a meal plan: ---
SELECT
  i.ingredient_id,
  i.name,
  SUM(ri.quantity) AS total_quantity,
  COALESCE(ri.unit, i.default_unit) AS unit
FROM meal_plan_items mpi
JOIN recipes r ON mpi.recipe_id = r.recipe_id
JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
WHERE mpi.meal_plan_id = 1
GROUP BY i.ingredient_id, i.name, unit;

Later, your backend could take this result and insert rows into grocery_list_items.

6. Updating & deleting
Update recipe title

--- UPDATE recipes ---
SET title = 'Garlic Chicken (Easy)'
WHERE recipe_id = 1;

--- Delete a recipe (cascades ingredients/steps/tags) ---
DELETE FROM recipes
WHERE recipe_id = 1;

Because of ON DELETE CASCADE, its recipe_ingredients and recipe_steps will be deleted automatically.

7. Handy MySQL + VS Code patterns
Re-run init from scratch (after editing schema):
docker compose down -v
docker compose up -d

Quick sanity check:
USE recipete_db;
SHOW TABLES;
SELECT COUNT(*) FROM recipes;

Comment out lines in SQL:-- this is a comment
/* block
   comment */

In most VS Code DB extensions:
Highlight a query and press the “Run” button (or keyboard shortcut), and it runs just that selection, not the whole file.
