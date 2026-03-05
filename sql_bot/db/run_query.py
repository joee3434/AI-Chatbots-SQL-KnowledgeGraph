import sqlite3
from pathlib import Path
from typing import Any, List, Tuple

DB_PATH = Path(__file__).resolve().parent / "inventory.db"

def _should_apply_default_filters(user_question: str) -> bool:
    t = user_question.lower()
    allow = ("include inactive", "include disposed", "include retired", "show inactive", "show disposed", "show retired")
    return not any(x in t for x in allow)

def _apply_default_filters(sql: str) -> str:
    s = sql.strip().rstrip(";")
    upper = s.upper()

    if not upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    if " FROM assets" in upper or " JOIN assets" in upper:
        if " WHERE " in upper:
            s += " AND assets.is_active = 1 AND assets.status NOT IN ('Disposed','Retired')"
        else:
            s += " WHERE assets.is_active = 1 AND assets.status NOT IN ('Disposed','Retired')"
    return s + ";"

def execute_select(sql: str) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return cols, rows
    finally:
        conn.close()

def format_rows(cols: List[str], rows: List[Tuple[Any, ...]]) -> str:
    if not rows:
        return "No results."
    header = " | ".join(cols)
    lines = [header, "-" * len(header)]
    for r in rows:
        lines.append(" | ".join(str(x) for x in r))
    return "\n".join(lines)

def run(user_question: str, sql: str) -> str:
    final_sql = _apply_default_filters(sql) if _should_apply_default_filters(user_question) else (sql.strip().rstrip(";") + ";")
    cols, rows = execute_select(final_sql)
    return format_rows(cols, rows)
