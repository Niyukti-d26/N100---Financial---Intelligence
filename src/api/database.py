import sqlite3

from src.config.settings import DATABASE_PATH


def get_connection():
    """
    Create SQLite database connection.
    """

    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    conn.row_factory = sqlite3.Row

    return conn
