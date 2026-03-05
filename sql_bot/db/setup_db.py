import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "inventory.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"

def run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    conn.executescript(sql)

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        run_sql_file(conn, SCHEMA_PATH)
        # reset & seed
        conn.executescript("""
        DELETE FROM assets;
        DELETE FROM vendors;
        DELETE FROM locations;
        DELETE FROM sqlite_sequence;
        """)
        run_sql_file(conn, SEED_PATH)
        conn.commit()
        print(f"Database created/seeded at: {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
