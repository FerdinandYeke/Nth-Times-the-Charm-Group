from flask import Flask, jsonify, render_template
from db import get_db_connection

app = Flask(__name__)

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
