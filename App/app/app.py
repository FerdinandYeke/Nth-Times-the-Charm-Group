from flask import Flask, jsonify
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


if __name__ == "__main__":
    # For local debugging (not used inside Docker, but handy if you run python app.py directly)
    app.run(host="0.0.0.0", port=5000, debug=True)
