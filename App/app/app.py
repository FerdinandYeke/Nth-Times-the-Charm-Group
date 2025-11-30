import requests
from flask import Flask, jsonify, render_template
from db import get_db_connection

app = Flask(__name__)

def import_meal_from_mealdb(id_meal: str) -> int:
    """
    Checks if recipe already exists in our DB, call TheMealDB, inserts into our DB
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    #Check if recipe already imported
    cur.execute(
        """
        SELECT recipe_id FROM list_recipes
        WHERE source_type = 'THEMEALDB' and source_external_id = %s
        """,
        (id_meal,)
    )
    row = cur.fetchone()
    if row:
        recipe_id = row["recipe_id"]
        cur.close()
        conn.close()
        return recipe_id

    #Fetch from TheMealDB
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_meal}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    meals = data.get("meals")
    if not meals:
        cur.close()
        conn.close()
        raise ValueError("Meal not found in TheMealDB")
    
    meal = meals[0]

    #Cache raw JSON into external_recipe_cache
    try:
        cur.execute(
            """
            INSERT INTO external_recipe_cache (source_type, source_external_id, raw_jason)
            VALUES ('THEMEALDB', %s, %s)
            ON DUPLICATE KEY UPDATE raw_json = VALUES(raw_json), fetched_at = NOW()
            """,
            (id_meal, resp.text)
        )
    except Exception:
        #If table doesn't exist yet, just skip caching
        pass

    #Insert into recipes
    cur.execute(
        """
        INSERT INTO recipes
            (user_id, title, description, total_time_min, servings, difficulty, is_public, source_type, source_external_id,
            source_url, thumbnail_url, youtube_url)
        VALUES
            (NULL, %s, %s, NULL, NULL, 'EASY', 1, 'THEMEALDB', %s, %s, %s, %s)
        """,
            (
                meal.get("strMeal"),
                meal.get("strInstructions"),
                meal.get("idMeal"),
                meal.get("strSource"),
                meal.get("strMealThumb"),
                meal.get("strYoutube"),
            )
    )
    recipe_id = cur.lastrowid

    #Ingredients 1 through 20
    for i in range (1, 21):
        ing_name = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if not ing_name:
            continue

        # look up ingredient, insert if not listed
        cur.execute(
            "SELECT ingredient_id FROM ingredients WHERE name = %s",
            (ing_name,)
        )
        row = cur.fetchone()
        if row:
            ingredient_id = row["ingredient_id"]
        else:
            cur.execute(
                "INSERT INTO ingredients (name, default_unit) VALES (%s, NULL)",
                (ing_name,)
            )
            ingredient_id = cur.lastrowid

        #Storing quanitity as 1 with actual measure in note, WILL NEED TO FIX
        cur.execute(
            """
            INSERT INTO recipe_ingredients
                (recipe_id, ingredient_id, quantity, unit, note)
            VALUES
                (%s, %s, %s, %s, %s)
            """,
            (recipe_id, ingredient_id, 1, None, measure or None)
        )

    conn.commit()
    cur.close()
    conn.close()
    return recipe_id

@app.route("/api/health")
def health():
    """
    Simple health check endpoint.
    Tries a small DB query to make sure MySQL is reachable.
    """
    db_status = "unknown"

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    return jsonify({
        "status": "ok",
        "database": db_status
    })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/recipes", methods=["GET"])
def list_recipes():
    """
    Return a simple list of recipes with id, title, and basic info.
    Powers main "recipe list" UI.
    """
    conn = get_db_connection()
    # dictionary=True makes rows come back as dicts (for jsonify)
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
          recipe_id,
          title,
          description,
          total_time_min,
          servings,
          source_type
        FROM recipes
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)

@app.route("/api/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # ==========================
    # Fetch the recipe itself
    # ==========================
    cur.execute("""
        SELECT
            recipe_id,
            user_id,
            title,
            description,
            total_time_min,
            servings,
            difficulty,
            source_type,
            source_external_id
        FROM recipes
        WHERE recipe_id = %s
    """, (recipe_id,))
    
    recipe = cur.fetchone()

    if not recipe:
        conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    # ==========================================
    # Fetch ingredients linked to the recipe
    # ==========================================
    cur.execute("""
        SELECT
            ri.ingredient_id,
            i.name AS ingredient_name,
            ri.quantity,
            ri.unit,
            ri.note
        FROM recipe_ingredients ri
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE ri.recipe_id = %s
    """, (recipe_id,))

    ingredients = cur.fetchall()

    # ==========================
    # Fetch recipe steps
    # ==========================
    try:
        cur.execute("""
            SELECT
                step_number,
                instruction
            FROM recipe_steps
            WHERE recipe_id = %s
            ORDER BY step_number ASC
        """, (recipe_id,))

        steps = cur.fetchall()

    except Exception:
        # If your DB doesn't yet have recipe_steps, steps can be optional
        steps = []

    cur.close()
    conn.close()

    # ==========================
    # Build the response JSON
    # ==========================
    recipe["ingredients"] = ingredients
    recipe["steps"] = steps

    return jsonify(recipe)

if __name__ == "__main__":
    # For local debugging (not used inside Docker, but handy if you run python app.py directly)
    app.run(host="0.0.0.0", port=5000, debug=True)
