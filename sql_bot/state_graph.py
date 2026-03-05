from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from .prompts import SYSTEM_PROMPT, CORRECT_PROMPT, RESPOND_PROMPT
from .sql_guard import apply_default_business_rules, validate_sql
from .db.run_query import execute_select


class BotState(TypedDict, total=False):
    question: str
    sql: str
    error: str
    rows: Any
    answer: str
    attempts: int


def make_llm():
    return ChatOllama(model="llama3", temperature=0)


def auto_fix_common_sql(sql: str) -> str:
    """
    Fix common LLM mistakes that cause SQLite syntax errors.
    - Duplicate WHERE clauses
    - Incomplete trailing WHERE/AND/OR
    """
    s = sql.strip().rstrip(";")
    upper = s.upper()

    # Fix duplicated WHERE: keep first WHERE, convert later WHEREs to AND
    if upper.count(" WHERE ") > 1:
        parts = s.split("WHERE")
        first = parts[0] + "WHERE" + parts[1]
        rest = "WHERE".join(parts[2:]).strip()
        if rest:
            s = first + " AND " + rest
        else:
            s = first

    # Remove trailing incomplete tokens
    for bad_end in [" WHERE", " AND", " OR"]:
        if s.upper().endswith(bad_end):
            s = s[: -len(bad_end)].rstrip()

    return s + ";"


def generator_node(state: BotState) -> BotState:
    llm = make_llm()
    q = state["question"]

    sql = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
        ]
    ).content.strip()

    state["sql"] = sql
    state["attempts"] = state.get("attempts", 0) + 1
    return state


def executor_node(state: BotState) -> BotState:
    q = state["question"]
    raw_sql = state["sql"]

    # Auto-fix common SQL formatting issues before validation/execution
    raw_sql = auto_fix_common_sql(raw_sql)
    state["sql"] = raw_sql

    ok, msg = validate_sql(raw_sql)
    if not ok:
        state["error"] = msg
        return state

    sql = apply_default_business_rules(q, raw_sql)

    try:
        cols, rows = execute_select(sql)
        state["rows"] = [dict(zip(cols, r)) for r in rows]
        state["error"] = ""
        state["sql"] = sql
    except Exception as e:
        state["error"] = str(e)

    return state


def should_correct(state: BotState) -> str:
    if state.get("error"):
        if state.get("attempts", 0) >= 5:
            return "give_up"
        return "correct"
    return "respond"


def corrector_node(state: BotState) -> BotState:
    llm = make_llm()
    fixed = llm.invoke(
        [
            {"role": "system", "content": "You fix SQL queries."},
            {
                "role": "user",
                "content": CORRECT_PROMPT.format(
                    question=state["question"],
                    sql=state["sql"],
                    error=state["error"],
                ),
            },
        ]
    ).content.strip()

    state["sql"] = fixed
    state["attempts"] = state.get("attempts", 0) + 1
    return state


def responder_node(state: BotState) -> BotState:
    llm = make_llm()
    rows = state.get("rows", [])

    answer = llm.invoke(
        [
            {"role": "system", "content": "You summarize database results."},
            {
                "role": "user",
                "content": RESPOND_PROMPT.format(
                    question=state["question"],
                    sql=state["sql"],
                    rows=rows,
                ),
            },
        ]
    ).content.strip()

    state["answer"] = answer
    return state


def give_up_node(state: BotState) -> BotState:
    state["answer"] = (
        "I couldn't execute a valid query after multiple attempts. "
        f"Last error: {state.get('error','')}"
    )
    return state


def build_graph():
    g = StateGraph(BotState)

    g.add_node("generate", generator_node)
    g.add_node("execute", executor_node)
    g.add_node("correct", corrector_node)
    g.add_node("respond", responder_node)
    g.add_node("give_up", give_up_node)

    g.set_entry_point("generate")
    g.add_edge("generate", "execute")

    g.add_conditional_edges(
        "execute",
        should_correct,
        {
            "correct": "correct",
            "respond": "respond",
            "give_up": "give_up",
        },
    )

    g.add_edge("correct", "execute")
    g.add_edge("respond", END)
    g.add_edge("give_up", END)

    return g.compile()
