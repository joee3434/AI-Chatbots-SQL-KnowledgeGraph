import re

FORBIDDEN = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "ATTACH", "DETACH"
]

ALLOWED_TABLES = {"assets", "vendors", "locations"}


def is_select_only(sql: str) -> bool:
    s = sql.strip().strip(";")
    return s.upper().startswith("SELECT")


def contains_forbidden(sql: str) -> bool:
    u = sql.upper()
    return any(word in u for word in FORBIDDEN)


def touches_only_allowed_tables(sql: str) -> bool:
    # Simple table detection for FROM/JOIN
    matches = re.findall(r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)|\bJOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)",
                         sql, flags=re.IGNORECASE)
    tables = set()
    for a, b in matches:
        if a:
            tables.add(a.lower())
        if b:
            tables.add(b.lower())
    return not tables or tables.issubset(ALLOWED_TABLES)


def validate_sql(sql: str) -> tuple[bool, str]:
    if not is_select_only(sql):
        return False, "Only SELECT queries are allowed."
    if contains_forbidden(sql):
        return False, "Forbidden SQL operation detected."
    if not touches_only_allowed_tables(sql):
        return False, "Query touches non-allowed tables."
    return True, "ok"


def apply_default_business_rules(question: str, sql: str) -> str:
    """
    Default rules:
    - Only Active records
    - Exclude Disposed/Retired assets from general queries
    Unless user explicitly asks otherwise.
    Also: do NOT break queries that already include WHERE (append with AND).
    """
    q = question.lower()
    s = sql.strip().rstrip(";")
    upper = s.upper()

    # If user explicitly asks, do not apply default filters
    allow_phrases = (
        "include inactive", "show inactive", "inactive",
        "include disposed", "show disposed", "disposed",
        "include retired", "show retired", "retired",
    )
    if any(p in q for p in allow_phrases):
        return s + ";"

    # Only apply rules when query touches assets
    if " FROM assets" not in upper and " JOIN assets" not in upper:
        return s + ";"

    default_filter = "assets.is_active = 1 AND assets.status NOT IN ('Disposed','Retired')"

    if " WHERE " in upper:
        s = s + " AND " + default_filter
    else:
        s = s + " WHERE " + default_filter

    return s + ";"
