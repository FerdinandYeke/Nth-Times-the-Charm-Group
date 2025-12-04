import os
import sys
import time

import pytest
import mysql.connector

# --- Ensure /app (where app.py & db.py live) is on sys.path ---

CURRENT_DIR = os.path.dirname(__file__)            # /app/tests
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, os.pardir)           # -> /app
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
from db import get_db_connection


def wait_for_db(timeout: float = 30.0, poll_interval: float = 1.0):
    """
    Wait until:
      1. MySQL is accepting connections AND
      2. The 'recipes' table exists (init.sql has finished).
    """
    start = time.time()

    host = os.environ.get("DB_HOST", "db")
    port = int(os.environ.get("DB_PORT", "3306"))
    user = os.environ.get("DB_USER", "recipete")
    password = os.environ.get("DB_PASSWORD", "recipete_pw")
    database = os.environ.get("DB_NAME", "recipete_db")

    while True:
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )
            cur = conn.cursor()
            # Ensure schema is initialized
            cur.execute("SHOW TABLES LIKE 'recipes';")
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                # DB is ready and recipes table exists
                return
        except mysql.connector.Error:
            # DB not ready yet
            pass

        if time.time() - start > timeout:
            raise TimeoutError("Database did not become ready in time.")

        time.sleep(poll_interval)


# API test
def test_recipe_list_route():
    """
    /api/recipes should return HTTP 200 (OK)
    Response body should be a JSON list
    """
    # Make sure DB and schema are ready before hitting the endpoint
    wait_for_db()

    client = app.test_client()
    resp = client.get("/api/recipes")

    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
