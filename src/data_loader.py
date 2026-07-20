import sqlite3
import yaml
from utils.helpers import format_schema_for_prompt


def load_config(config_path="configs/model_config.yaml"):
    """Load model and database settings from the YAML config file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def connect_db(db_path):
    """Connect to the Chinook SQLite database and return conn + cursor."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def get_schema(cursor):
    """Extract all table names and their columns/types from the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        schema[table] = [(col[1], col[2]) for col in columns]
    return schema


def get_schema_string(cursor):
    """Get the schema as a clean, prompt-ready string."""
    schema = get_schema(cursor)
    return format_schema_for_prompt(schema)
