import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "recipete"),
        password=os.getenv("DB_PASSWORD", "recipete_pw"),
        database=os.getenv("DB_NAME", "recipete_db"),
    )
