import os

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASS = os.getenv("PG_PASS", "postgres")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_DB = os.getenv("PG_DB", "flask-app-template")
ENVIRONMENT = os.getenv("FLASK_ENVIRONMENT", "Development")
