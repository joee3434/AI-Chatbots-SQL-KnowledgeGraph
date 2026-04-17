from fastapi import FastAPI
from pydantic import BaseModel

from sql_bot.state_graph import build_graph
from memory.memory_manager import MemoryManager
from kg_bot.graph_store import GraphStore

app = FastAPI(title="AI Chatbots API", version="1.0.0")

graph = build_graph()
memory = MemoryManager()
kg_store = GraphStore()

class SQLChatRequest(BaseModel):
    session_id: str
    message: str
class KGChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AI Chatbots API is running"}


@app.post("/sql-chat")
def sql_chat(request: SQLChatRequest):
    session_id = request.session_id
    message = request.message.strip()

    memory.add_message(session_id, "user", message)
    history = memory.get_short_history(session_id)

    state = {
        "question": message,
        "attempts": 0,
        "history": history
    }

    out = graph.invoke(state)

    sql_text = out.get("sql", "")
    answer = out.get("answer", "No answer.")

    memory.add_message(session_id, "assistant", answer)

    return {
        "session_id": session_id,
        "question": message,
        "sql": sql_text,
        "answer": answer
    }
@app.get("/history/{session_id}")
def get_history(session_id: str):
    return {
        "session_id": session_id,
        "short_term": memory.get_short_history(session_id),
        "long_term": memory.get_long_history(session_id)
    }
@app.post("/kg-chat")
def kg_chat(request: KGChatRequest):
    message = request.message.strip()
    parts = message.split()

    if not parts:
        return {"answer": "Empty message."}

    cmd = parts[0].lower()

    if cmd == "add" and len(parts) >= 4:
        entity = parts[1]
        relation = parts[2]
        value = " ".join(parts[3:])
        answer = kg_store.add_fact(entity, relation, value)
        return {"answer": answer}

    elif cmd in {"update", "edit"} and len(parts) >= 4:
        entity = parts[1]
        relation = parts[2]
        value = " ".join(parts[3:])
        answer = kg_store.update_fact(entity, relation, value)
        return {"answer": answer}

    elif cmd in {"delete", "remove"} and len(parts) >= 3:
        entity = parts[1]
        relation = parts[2]
        answer = kg_store.delete_fact(entity, relation)
        return {"answer": answer}

    elif cmd == "inquire":
        if len(parts) == 1:
            answer = kg_store.inquire()
        elif len(parts) == 2:
            answer = kg_store.inquire(entity=parts[1])
        elif len(parts) >= 3:
            answer = kg_store.inquire(entity=parts[1], relation=parts[2])
        return {"answer": answer}

    else:
        return {"answer": "Invalid KG command. Use add, update, delete, or inquire."}
