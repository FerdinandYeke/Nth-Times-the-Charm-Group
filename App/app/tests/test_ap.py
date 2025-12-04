import pytest
from app import app, import_meal_from_mealdb
from app.db import get_db_connection

# API tests
def test_recipe_list_route():
    """
    /api/recipes should return HTTP 200 (OK)
    Response body should be a JSON list
    """
    client = app.test_client()
    resp = client.get("/api/recipes")

    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)