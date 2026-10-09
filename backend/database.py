import sqlite3
import os

DB_PATH = "forensics.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    ''')
    # Initialize counters if they don't exist
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_visits', 0)")
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_scanned', 0)")
    conn.commit()
    conn.close()

def increment_stat(key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE stats SET value = value + 1 WHERE key = ?", (key,))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM stats")
    results = dict(cursor.fetchall())
    conn.close()
    return results
