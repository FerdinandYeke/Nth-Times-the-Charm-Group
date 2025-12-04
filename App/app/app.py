import requests
from flask import Flask, jsonify, render_template
from db import get_db_connection

app = Flask(__name__)

# ==================================================================
# IMPORT FROM THEMEALDB → stores into local DB
# ==================================================================
def import_meal_from_mealdb(id_meal: str) -> int:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT recipe_id FROM recipes
        WHERE source_type = 'THEMEALDB' and source_external_id = %s
    """, (id_meal,))
    row = cur.fetchone()
    if row:
        recipe_id = row["recipe_id"]
        cur.close()
        conn.close()
        return recipe_id

    # Fetch remote meal
    resp = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_meal}", timeout=10)
    resp.raise_for_status()
    data = resp.json()

    meal = data.get("meals")[0]

    # Insert recipe into DB
    cur.execute("""
        INSERT INTO recipes
            (user_id, title, description, total_time_min, servings, difficulty, 
             is_public, source_type, source_external_id, source_url, 
             thumbnail_url, youtube_url)
        VALUES (NULL, %s, %s, NULL, NULL,'EASY',1,'THEMEALDB',%s,%s,%s,%s)
    """, (
        meal.get("strMeal"),
        meal.get("strInstructions"),  # THIS stores instructions text
        meal.get("idMeal"),
        meal.get("strSource"),
        meal.get("strMealThumb"),
        meal.get("strYoutube"),
    ))
    recipe_id = cur.lastrowid

    # store ingredients
    for i in range(1, 21):
        ing = meal.get(f"strIngredient{i}") or ""
        measure = meal.get(f"strMeasure{i}") or ""
        ing = ing.strip()
        if not ing:
            continue
        
        cur.execute("SELECT ingredient_id FROM ingredients WHERE name=%s", (ing,))
        row = cur.fetchone()
        ingredient_id = row["ingredient_id"] if row else None
        
        if not ingredient_id:
            cur.execute("INSERT INTO ingredients (name) VALUES (%s)", (ing,))
            ingredient_id = cur.lastrowid
        
        cur.execute("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, note)
            VALUES (%s,%s,1,NULL,%s)
        """, (recipe_id, ingredient_id, measure))

    conn.commit()
    cur.close()
    conn.close()
    return recipe_id


# ==================================================================
# ROUTES
# ==================================================================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/recipes")
def recipe_list():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT recipe_id,title,description FROM recipes ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""SELECT recipe_id,title,description FROM recipes WHERE recipe_id=%s""",(recipe_id,))
    recipe = cur.fetchone()

    if not recipe:
        return jsonify({"error":"Recipe not found"}),404

    cur.execute("""
        SELECT i.name AS ingredient_name, ri.note
        FROM recipe_ingredients ri
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE ri.recipe_id=%s
    """,(recipe_id,))
    ingredients = cur.fetchall()

    cur.close()
    conn.close()

    recipe["ingredients"] = ingredients
    return jsonify(recipe)


@app.route("/api/external/themealdb/import/<id_meal>",methods=["POST"])
def import_external(id_meal):
    try:
        return jsonify({"recipe_id":import_meal_from_mealdb(id_meal)})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/health")
def health():
    """
    Simple health check to verify the API and DB are reachable.
    """
    db_status = "ok"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"error: {e}"

    return jsonify({
        "status": "ok",
        "database": db_status
    })


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
