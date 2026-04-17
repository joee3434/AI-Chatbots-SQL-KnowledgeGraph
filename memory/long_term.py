import sqlite3
from pathlib import Path


class LongTermMemory:
    def __init__(self, db_path="memory/memory_store.db"):
        self.db_path = Path(db_path)
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

    def add_message(self, session_id, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO memory_log (session_id, role, content)
        VALUES (?, ?, ?)
        """, (session_id, role, content))

        conn.commit()
        conn.close()

    def get_history(self, session_id, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT role, content, timestamp
        FROM memory_log
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """, (session_id, limit))

        rows = cursor.fetchall()
        conn.close()

        rows.reverse()

        return [
            {"role": row[0], "content": row[1], "timestamp": row[2]}
            for row in rows
        ]

    def clear_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM memory_log
        WHERE session_id = ?
        """, (session_id,))

        conn.commit()
        conn.close()
